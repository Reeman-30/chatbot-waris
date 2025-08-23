import torch # type: ignore
import torch.nn.functional as F # type: ignore
import joblib
import json
import random
import os
import re

from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from tools.BertMultiClassifier import *
from tools.calculation import hitung_pembagian_khusus
from tools.penjelasan_fiqh import penjelasan_fiqh_waris

# === Inisialisasi Flask ===
app = Flask(__name__)
CORS(app)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Muat Model 1: Intent Classifier ---
INTENT_MODEL_PATH = "./saved_model/intent/"
intent_model = AutoModelForSequenceClassification.from_pretrained(INTENT_MODEL_PATH).to(device)
intent_tokenizer = AutoTokenizer.from_pretrained(INTENT_MODEL_PATH)
intent_label_encoder = joblib.load(os.path.join(INTENT_MODEL_PATH, "label_encoder.pkl"))

# --- Muat Model 2: Entity Extractor ---
ENTITY_MODEL_PATH = "./saved_model/bert_waris_multitask.pt" # Sesuaikan path ini
entity_model = BertMultiClassifier(num_custom_tokens=len(entity_tokenizer.get_added_vocab())).to(device)
entity_model.load_state_dict(torch.load(ENTITY_MODEL_PATH, map_location=device))
entity_model.eval() # Set ke mode evaluasi

# --- Siapkan data respon dari file JSON ---
with open("./utils/stable/datasets-intents.json", "r", encoding="utf-8") as f: # Ganti nama file jika perlu
    data_intent = json.load(f)
    
intent_responses = {item["intent"]: item.get("responses", []) for item in data_intent["intents"]}

# === Fungsi prediksi intent ===
threshold = 0.90
def predict_intent(text):
    inputs = entity_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = intent_model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        confidence, predicted = torch.max(probs, dim=1)

    if confidence.item() < threshold:
        return "unknown", float(confidence)

    intent = intent_label_encoder.inverse_transform([predicted.item()])[0]
    return intent, float(confidence)

# Fungsi hibrida untuk mengekstrak ahli waris (ML) dan harta/hutang (Rule-based)
def predict_entities_hybrid(text):
    # --- Sub-fungsi 1: Ekstraksi Ahli Waris (ML) ---
    def extract_ahli_waris(text, model, tokenizer):
        encoded = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        input_ids = encoded["input_ids"].to(device)
        attention_mask = encoded["attention_mask"].to(device)

        with torch.no_grad():
            output = model(input_ids, attention_mask)

        hasil = {
            "istri": torch.argmax(output["istri"], dim=1).item(),
            "anak_laki-laki": torch.argmax(output["anak_laki-laki"], dim=1).item(),
            "anak_perempuan": torch.argmax(output["anak_perempuan"], dim=1).item(),
            "ayah": torch.argmax(output["ayah"], dim=1).item(),
            "ibu": torch.argmax(output["ibu"], dim=1).item(),
            "kakek": torch.argmax(output["kakek"], dim=1).item(),
            "nenek": torch.argmax(output["nenek"], dim=1).item(),
        }
        return hasil

    # --- Sub-fungsi 2: Ekstraksi Harta & Hutang (Rule-based) ---
    def extract_harta_hutang(text):
        cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
        words = cleaned_text.split()
        result = {}
        harta_keywords = ['harta', 'warisan', 'aset', 'uang', 'tabungan', 'waris']
        hutang_keywords = ['hutang', 'utang']
        total_harta, total_hutang = 0, 0

        for i, word in enumerate(words):
            try:
                num = int(word)
                multiplier = 1
                if i + 1 < len(words):
                    if words[i+1] == 'juta': multiplier = 1_000_000
                    elif words[i+1] == 'miliar': multiplier = 1_000_000_000

                final_num = num * multiplier
                is_harta, is_hutang = False, False
                for j in range(max(0, i - 5), i):
                    if words[j] in harta_keywords: is_harta = True; break
                    if words[j] in hutang_keywords: is_hutang = True; break

                if is_harta: total_harta += final_num
                elif is_hutang: total_hutang += final_num
            except ValueError:
                continue

        if total_harta > 0: result['harta'] = total_harta
        if total_hutang > 0: result['hutang'] = total_hutang
        return result

    # --- Gabungkan hasil ---
    ahli_waris = extract_ahli_waris(text, entity_model, entity_tokenizer)
    harta_hutang = extract_harta_hutang(text)
    ahli_waris.update(harta_hutang)
    return ahli_waris

# === Endpoint utama ===
@app.route("/hitung_waris", methods=["POST"])
def hitung_waris():
    data = request.get_json()
    if not data or "teks" not in data:
        return jsonify({"error": "Harap kirim JSON dengan field 'teks'."}), 400

    teks = data["teks"]
    if teks == "":
        return jsonify({"error": "Harap isi kolom pertanyaan."}), 400

    intent, confidence = predict_intent(teks)

    responses = intent_responses.get(intent, ["Maaf, saya tidak mengerti apa yang Anda maksudkan."])
    response_text = random.choice(responses) if responses else "Maaf, saya belum bisa menjawab maksud Anda."

    entitas = predict_entities_hybrid(teks)
    hitung_waris = hitung_pembagian_khusus(entitas)
    penjelasan_fiqh = penjelasan_fiqh_waris(entitas)

    if hitung_waris:
        bagian_hitung = "\nRincian Pembagian Waris:\n"
        bagian_hitung += "\n".join([f"- {k}: {v:,} rupiah" for k, v in hitung_waris.items() if k not in ['total_harta', 'harta_bagian_waris']])
        penjelasan_fiqh_with_hitungan = f"{penjelasan_fiqh}{bagian_hitung}"
        penjelasan_fiqh_with_hitungan += "\n\nApakah sudah cukup terbantu dengan jawabannya?"
    else:
        penjelasan_fiqh_with_hitungan = penjelasan_fiqh
    
    if "harta" not in entitas and intent == "pertanyaan":
        return jsonify({
            "pertanyaan": teks,
            "intent": intent,
            "confidence": confidence,
            "responses": {
                "response": "Tolong kirim pertanyaannya yang lengkap dengan nominal harta atau hutang (jika ada)"
            },
            "entitas": entitas,
            "role": "amana"
        })

    if confidence < threshold:
        return jsonify({
            "pertanyaan": teks,
            "intent": intent,
            "confidence": confidence,
            "responses": {
                "response": response_text
            },
            "role": "amana"
        })
    
    if intent != "pertanyaan":
        return jsonify({
        "pertanyaan": teks,
        "intent": intent,
        "confidence": confidence,
        "responses": {
            "response": response_text
        },
        "role": "amana"
    })
    
    return jsonify({
        "pertanyaan": teks,
        "intent": intent,
        "confidence": confidence,
        "responses": {
            "response": response_text,
            "penjelasan_fiqh_with_hitungan": penjelasan_fiqh_with_hitungan
        },
        "entitas": entitas,
        "role": "amana"
    })

@app.route("/", methods=["GET"])
def index():
    return "<center><h3>API Waris</h3></center>"

# === Jalankan server ===
if __name__ == "__main__":
    app.run(debug=True)
