from __future__ import annotations

import pickle

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.optimization.model import model_optimize


def optimize(
    n_candidate: int,
    alpha: float,
    gamma_mu: int,
    gamma_sigma: int,
    c_mu: float,
    c_sigma: float,
    N: int,
) -> None:
    """
    ユーザーごとに最適化問題を解く関数
    """
    # データの読み込み
    pred_rating_df = pd.read_csv("./pred_rating.csv")
    sigma_ar = np.load("./cov_matrix.npy")

    # ユーザーごとに最適化問題を解く
    items_recommended = dict()

    for user in tqdm(pred_rating_df["user_id"].unique()):
        # ユーザーごとにデータを抽出
        user_df = pred_rating_df[pred_rating_df["user_id"] == user].reset_index(drop=True)
        # 予測評価値
        mu = user_df["rating"].values
        # 学習データは除く
        user_ntrain_df = user_df[user_df["data_type"] != "train"].reset_index(drop=True)
        # Iはraring順に並び替えたitem_idの上位n_candidate個
        I = user_ntrain_df.sort_values("rating", ascending=False)["item_id"].values[:n_candidate]

        # 最適化問題を解く
        w_opt, obj_val = model_optimize(
            I, mu, sigma_ar, alpha, gamma_mu, gamma_sigma, c_mu, c_sigma, N
        )
        # 推薦したアイテムのid
        item_ids = I[w_opt == 1]
        # 結果を格納
        items_recommended[user] = item_ids

    # items_reccomendedを保存
    with open("./items_recommended.pkl", "wb") as f:
        pickle.dump(items_recommended, f)
