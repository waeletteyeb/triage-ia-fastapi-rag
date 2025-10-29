# app/services/embeddings.py
from typing import List, Optional
import torch
from transformers import AutoTokenizer, AutoModel


class BioGPTEmbeddingFunction:
    def __init__(self, model_name: str = "microsoft/biogpt", device: Optional[str] = None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def __call__(self, input: List[str]) -> List[List[float]]:
        if not isinstance(input, list):
            input = [str(input)]
        with torch.no_grad():
            enc = self.tokenizer(
                input,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            ).to(self.device)
            # Mean-pool last hidden states
            out = self.model(**enc).last_hidden_state  # [B, T, H]
            emb = out.mean(dim=1)                      # [B, H]
            return emb.cpu().tolist()

    def name(self) -> str:
        return f"BioGPTEmbeddingFunction({self.model_name})"
