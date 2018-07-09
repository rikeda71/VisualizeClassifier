import numpy as np
from . import Model


class Logistic(Model):

    def __init__(self):
        super().__init__()

    def train_one_step(self, i: int):
        """
        @param i <int> : 学習データの位置，インデックス
        学習を1ステップ進める
        確率的勾配降下法による実装
        """

        # 学習データをコピー
        w_old = deepcopy(self.__w)
        eta = 1.0 / np.sqrt(10 + self.__t)
        # 学習する値を取得
        y = sign[i]
        f = self.train_data[i]
        s = y * (1 - self.prob_val(y, f)) * f
        self.__w += eta * s
        self.__t += 1
        self.end = True if np.norm(self.__w, w_old) < self.__theta else False

    def prob_val(self, y: int=1, feature: np.array) -> float:
        """
        @param y <int> : クラス(-1 or 1)
        @param feature <list> : 素性
        @return <float> : ロジスティック回帰モデルにおける確率値(P(y|d))
        指定したクラスへの属する確率を返す(0 ~ 1 の間)
        """

        val = -1 * y * np.dot(self.__w, feature)
        return self.sigmoid(val)

    def sigmoid(self, t: float) -> float:
        """
        @param t <float> : -∞ ~ +∞までの範囲の値のいずれか
        @return <float> : -1 ~ +1までの値のいずれか
        sigmoid 関数の値を返す
        """

        return 1 / (1 + np.exp(-1 * t))
