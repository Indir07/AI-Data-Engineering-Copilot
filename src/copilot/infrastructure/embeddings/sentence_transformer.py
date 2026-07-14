"""Sentence-Transformers embedder implementing ``EmbedderPort``.

The model is loaded lazily on first use so importing this module (and building the
container) stays cheap, and processes that never embed never pay the cost.
Embeddings are L2-normalised so cosine similarity is a dot product.
"""

from __future__ import annotations

from typing import Any


class SentenceTransformerEmbedder:
    def __init__(self, model_name: str, device: str = "cpu") -> None:
        self._model_name = model_name
        self._device = device
        self._model: Any | None = None

    @property
    def _st(self) -> Any:
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self._model_name, device=self._device)
        return self._model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        vectors = self._st.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
        return [[float(x) for x in row] for row in vectors]

    def embed_query(self, text: str) -> list[float]:
        vector = self._st.encode([text], normalize_embeddings=True, convert_to_numpy=True)[0]
        return [float(x) for x in vector]
