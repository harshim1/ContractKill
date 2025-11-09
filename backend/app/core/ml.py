from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

from app.core.logger import get_logger


logger = get_logger(__name__)
MODEL_PATH = Path(__file__).resolve().parent / "waste_model.joblib"


@dataclass
class WasteFeatures:
    is_recurring: int
    dup_in_category: int
    low_usage: int
    overpay_pct: float
    owner_inactive: int

    def to_vector(self) -> np.ndarray:
        return np.array(
            [
                self.is_recurring,
                self.dup_in_category,
                self.low_usage,
                self.overpay_pct,
                self.owner_inactive,
            ]
        )


class WasteModel:
    def __init__(self) -> None:
        self.model = LogisticRegression()
        if MODEL_PATH.exists():
            try:
                self.model = joblib.load(MODEL_PATH)
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning("Failed to load WasteScore model: %s", exc)

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        if X.size == 0 or len(set(y.tolist())) < 2:
            logger.info("Insufficient variety to train WasteScore model")
            return
        self.model.fit(X, y)
        joblib.dump(self.model, MODEL_PATH)
        logger.info("WasteScore model trained with %d samples", len(X))

    def predict_proba(self, features: WasteFeatures) -> float:
        vec = features.to_vector().reshape(1, -1)
        try:
            proba = float(self.model.predict_proba(vec)[0, 1])
        except Exception:
            # If model is not trained yet, use a simple heuristic
            weights = np.array([0.2, 0.2, 0.25, 0.25, 0.1])
            norm_vec = vec.astype(float)
            norm_vec[0, 3] = min(1.0, max(0.0, norm_vec[0, 3]))
            proba = float(np.dot(norm_vec, weights.T))
        return proba


waste_model = WasteModel()
