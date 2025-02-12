import torch
from sentence_transformers import SentenceTransformer
from ..config import Configuration
from ..logger import Logger
import os
from typing import List

logger = Logger(__name__)


class EmbeddingService:
    def __init__(self):
        self.config = Configuration().get_config('embedding')
        self.model_names = [model for model in self.config['model_names']]
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        self.current_model = self.load_model(self.model_names[1])

    def set_model(self, model_name: str):
        if model_name in self.model_names:
            self.current_model = self.load_model(model_name)
        else:
            raise ValueError(f"Model {model_name} is not available. Choose from {list(self.model_names)}")

    def load_model(self, model_name: str):
        logger.info(f"Loading model: {model_name}")

        for model in os.listdir('./embedding_models'):
            if model == model_name:
                logger.info(f"Model already exists: {model_name}")
                model = SentenceTransformer(f"./embedding_models/{model_name}")
                return model.to(self.device)

        logger.info(f"Downloading model: {model_name}")
        model = SentenceTransformer(model_name)
        model.save(f"./embedding_models/{model_name}")
        return model.to(self.device)

    def get_available_models(self) -> List[str]:
        return list(self.model_names)

    def encode(self, text: str):
        logger.info(f"Encoding text: {text}")
        return self.current_model.encode(text, device=self.device)

    def encode_batch(self, texts: List[str]):
        logger.info(f"Encoding batch of {len(texts)} texts")
        return self.current_model.encode(texts, device=self.device).tolist()