import os
from typing import Optional

from transformers import MarianMTModel, MarianTokenizer
import torch

MODEL_ENV = "MODEL_DIR"
MODEL_NAME_ENV = "MODEL_NAME"
DEFAULT_MODEL = "Helsinki-NLP/opus-mt-en-fr"

class Translator:
    def __init__(self, model_dir: Optional[str] = None, model_name: Optional[str] = None, device: Optional[str] = None):
        """Load the MarianMT model and tokenizer.

        model_dir: if provided, passed to from_pretrained as local directory.
        model_name: HF model name to use if no local model_dir.
        device: torch device string, e.g., 'cpu' or 'cuda'. If None, auto detect.
        """
        self.model_dir = model_dir or os.getenv(MODEL_ENV)
        self.model_name = model_name or os.getenv(MODEL_NAME_ENV) or DEFAULT_MODEL

        # choose local path or HF name
        repo = self.model_dir or self.model_name

        # device
        if device:
            self.device = torch.device(device)
        else:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # load
        self.tokenizer = MarianTokenizer.from_pretrained(repo)
        self.model = MarianMTModel.from_pretrained(repo)
        self.model.to(self.device)

    def translate(self, text: str, max_length: int = 256) -> str:
        if not isinstance(text, str):
            raise TypeError('text must be a string')
        if text.strip() == '':
            return ''

        batch = self.tokenizer([text], return_tensors='pt', padding=True)
        batch = {k: v.to(self.device) for k, v in batch.items()}
        translated = self.model.generate(**batch, max_length=max_length)
        tgt = [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated]
        return tgt[0]

# helper singleton
_translator: Optional[Translator] = None

def get_translator() -> Translator:
    global _translator
    if _translator is None:
        _translator = Translator()
    return _translator
