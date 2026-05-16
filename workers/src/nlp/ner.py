from typing import Any

import spacy
from loguru import logger


class NERExtractor:
    """Extrai entidades nomeadas com spaCy."""

    LABELS_PT = {
        "PER": "pessoa",
        "ORG": "organizacao",
        "LOC": "local",
        "MISC": "misc",
    }

    LABELS_EN = {
        "PERSON": "pessoa",
        "ORG": "organizacao",
        "GPE": "local",
        "LOC": "local",
        "EVENT": "evento",
        "PRODUCT": "produto",
    }

    def __init__(self, model_name: str):
        logger.info(f"🧠 Carregando modelo NER: {model_name}")
        try:
            self._nlp = spacy.load(model_name)
            logger.info(f"✅ Modelo NER carregado: {model_name}")
        except OSError:
            logger.warning(f"⚠️ Modelo {model_name} não encontrado. Baixando...")
            spacy.cli.download(model_name)
            self._nlp = spacy.load(model_name)

    def extract(self, text: str, language: str = "pt") -> list[dict[str, Any]]:
        if not text or not text.strip():
            return []

        label_map = self.LABELS_PT if language == "pt" else self.LABELS_EN

        doc = self._nlp(text[:5000])  # limita para performance
        entities = []
        seen = set()

        for ent in doc.ents:
            key = (ent.text.strip(), ent.label_)
            if key in seen:
                continue
            seen.add(key)

            entities.append({
                "text": ent.text.strip(),
                "label": ent.label_,
                "label_pt": label_map.get(ent.label_, ent.label_),
            })

        logger.debug(f"🔍 {len(entities)} entidades extraídas")
        return entities
