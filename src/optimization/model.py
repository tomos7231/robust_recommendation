from __future__ import annotations

import numpy as np
from gurobipy import GRB, GurobiError, Model, quicksum


def optimize(
    I: list[int],
    mu: np.ndarray,
    sigma: np.ndarray,
    alpha: float,
    gamma_mu: int,
    gamma_sigma: int,
    N: int,
):
    """
    最適化問題を解く関数
    """
    # モデルの定義
    model = Model("robust_optimization")

    # 変数の定義
    # 推薦アイテムの0-1変数
    w, p, q = dict(), dict(), dict(), dict(), dict()
    for i in I:
        w[i] = model.addVar(vtype=GRB.BINARY, name=f"w_{i}")
        p[i] = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name=f"p_{i}")
        for j in I:
            q[i, j] = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name=f"q_{i}_{j}")

    # 単一の変数を定義
    z = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="z")
    g = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="g")

    # 目的関数の定義
    objective = 0
    objective += (1 - alpha)(
        quicksum(mu[i] * w[i] for i in I) - z * gamma_mu - quicksum(p[i] for i in I)
    )
    objective -= alpha * (
        quicksum(sigma[i, j] * w[i] * w[j] for i in I for j in I)
        + g * gamma_sigma
        + quicksum(q[i, j] for i in I for j in I)
    )
    model.setObjective(objective, GRB.MAXIMIZE)

    # 制約条件の定義
    # wの和はN
    model.addConstr(quicksum(w[i] for i in I) == N, name="w_sum")

    #

    # 最適化の実行
    try:
        model.optimize()
    except GurobiError:
        print("Error reported during optimization")

    # 結果の取得
    w_opt = np.array([w[i].x for i in I])  # どのアイテムが推薦されるか
    obj_val = model.objVal  # 目的関数値

    return w_opt, obj_val