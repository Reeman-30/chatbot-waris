import torch # type: ignore
import torch.nn.functional as F # type: ignore
import joblib
import json
import random

from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from tools.calculation import hitung_pembagian_khusus
from tools.extract_entity import extract_entitas
from tools.penjelasan_fiqh import penjelasan_fiqh_waris

# === Inisialisasi Flask ===
app = Flask(__name__)
CORS(app)

# === Load model, tokenizer, dan label encoder ===
model_dir = "saved_model"
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)
label_encoder = joblib.load(f"{model_dir}/label_encoder.pkl")
model.eval()

# === Load response dari file datasets-intent.json ===
with open("./utils/datasets-intent.json", "r", encoding="utf-8") as f:
    data = json.load(f)

intent_responses = {
    item["intent"]: item.get("responses", [])
    for item in data["intents"]
}

# === Fungsi prediksi intent ===
threshold = 0.70

def predict_intent(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        confidence, predicted = torch.max(probs, dim=1)

    if confidence.item() < threshold:
        return "unknown", float(confidence)

    intent = label_encoder.inverse_transform([predicted.item()])[0]
    return intent, float(confidence)

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

    entitas = extract_entitas(teks)
    hitung_waris = hitung_pembagian_khusus(entitas)
    penjelasan_fiqh = penjelasan_fiqh_waris(entitas)

    if hitung_waris:
        bagian_hitung = "\nRincian Pembagian Waris:\n"
        bagian_hitung += "\n".join([f"- {k}: {v:,} rupiah" for k, v in hitung_waris.items() if k not in ['total_harta', 'harta_bagian_waris']])
        penjelasan_fiqh_with_hitungan = f"{penjelasan_fiqh}{bagian_hitung}"

        # Tambahan catatan pembagian
        if entitas.get("istri", 0) > 1 and entitas.get("anak_laki-laki", 0) > 1 and entitas.get("anak_perempuan", 0) > 1:
            penjelasan_fiqh_with_hitungan += "\n\nCatatan:"
            
            bagian_per_istri = hitung_waris["Istri"]
            bagian_per_anak_laki = hitung_waris["Anak Laki-Laki"]
            bagian_per_anak_perempuan = hitung_waris["Anak Perempuan"]
            jumlah_istri = entitas["istri"]

            penjelasan_fiqh_with_hitungan += f"\nIstri masing-masing mendapatkan {bagian_per_istri:,} : {jumlah_istri} = {round(bagian_per_istri / jumlah_istri):,} rupiah"
            penjelasan_fiqh_with_hitungan += f"\nAnak Laki-Laki masing-masing mendapatkan {bagian_per_anak_laki:,} rupiah"
            penjelasan_fiqh_with_hitungan += f"\nAnak Perempuan masing-masing mendapatkan {bagian_per_anak_perempuan:,} rupiah"

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
                "response": response_text,
                "penjelasan_fiqh_with_hitungan": None
            },
            "entitas": None,
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

# === Jalankan server ===
if __name__ == "__main__":
    app.run(debug=True)
