from __future__ import annotations

import pickle
from typing import TypeVar

import pandas as pd

from src.evaluation.metric import calc_diversity, calc_precision, calc_recall

logger = TypeVar("logger")


def evaluate(logger: logger, test_df: pd.DataFrame, N: int, thres_rating: float) -> None:
    """
    評価指標を計算する関数
    """
    # データの読み込み
    with open("./items_recommended.pkl", "rb") as f:
        items_recommended = pickle.load(f)

    # Precisionの計算
    precision = calc_precision(items_recommended, test_df, N, thres_rating)
    logger.info(f"Precision: {precision:.5f}")

    # Recallの計算
    recall = calc_recall(items_recommended, test_df, thres_rating)
    logger.info(f"Recall: {recall:.5f}")

    # Diversityの計算
    diversity = calc_diversity(items_recommended)
    logger.info(f"Diversity: {diversity}")
