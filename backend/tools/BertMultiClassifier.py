import torch.nn as nn  # type: ignore
from transformers import BertTokenizerFast, BertModel

entity_tokenizer = BertTokenizerFast.from_pretrained("indolem/indobert-base-uncased")
entity_tokenizer.add_tokens(["<JUMLAH>", "<JUMLAH_M>"])

class BertMultiClassifier(nn.Module):
    def __init__(self, num_custom_tokens):
        super().__init__()
        self.bert = BertModel.from_pretrained("indolem/indobert-base-uncased")
        self.bert.resize_token_embeddings(len(entity_tokenizer)) # Sesuaikan ukuran embedding
        self.dropout = nn.Dropout(0.3)
        self.head_istri = nn.Linear(768, 5)
        self.head_anak_lk = nn.Linear(768, 6)
        self.head_anak_pr = nn.Linear(768, 6)
        self.head_ayah = nn.Linear(768, 2)
        self.head_ibu = nn.Linear(768, 2)
        self.head_kakek = nn.Linear(768, 2)
        self.head_nenek = nn.Linear(768, 2)

    def forward(self, input_ids, attention_mask):
        pooled = self.bert(input_ids=input_ids, attention_mask=attention_mask).pooler_output
        pooled = self.dropout(pooled)
        return {
            "istri": self.head_istri(pooled),
            "anak_laki-laki": self.head_anak_lk(pooled),
            "anak_perempuan": self.head_anak_pr(pooled),
            "ayah": self.head_ayah(pooled),
            "ibu": self.head_ibu(pooled),
            "kakek": self.head_kakek(pooled),
            "nenek": self.head_nenek(pooled),
        }