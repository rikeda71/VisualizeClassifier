import numpy as np
import MeCab
from copy import deepcopy


class Model(object):

    def __init__(self, train_data: list, signs: list, theta: float=10e-6):
        """
        @param train_data <list> : 学習データのベクトル群
        @param signs <list> : 学習データのクラス（+1, -1）
        @param theta <float> : 学習の閾値
        """

        neologd_path = "/usr/lib/mecab/dic/mecab-ipadic-neologd"
        self.m = MeCab.Tagger("-d" + neologd_path)
        self.m.parse("")
        self.dic = {}
        with open("models/dataset/pn_ja.dic", "r") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                s = line.split(":")
                self.dic[s[0]] = float(s[-1])
        self.train_data = [self.getvec(t) for t in train_data]
        self.signs = signs
        self.theta = theta
        self.n = len(self.train_data)
        self.w = np.random.random(len(self.train_data[0]))
        self.t = 0
        self.end = False

    def train(self, min_iter: int=100, max_iter: int=1000):
        """
        @param max_iteration <int> : 最大学習回数
        学習機の学習を行う
        """

        while self.t < max_iter and not self.end:
            N = np.random.randint(0, self.n, self.n)
            for i in N:
                self.train_one_step(i)
        self.save_model()

    def predict(self, text: str):
        pass

    def getvec(self, text: str) -> list:
        """
        @param text <str> : 1文
        @return <list> : 文の特徴ベクトル(BoW)
        文の特徴ベクトルを返す
        ex.) [0.0, 2.0, 1.0, 0.0, 0.0, 1.0, ...]
        """

        # 形態素解析
        tokens = []
        node = self.m.parseToNode(text)
        while node:
            tokens.append(node.surface)
            node = node.next
        # ベクトルに変換
        vec = [0, 0]
        for t in tokens:
            if t in self.dic:
                if self.dic[t] >= 0:
                    vec[0] += self.dic[t]
                else:
                    vec[1] -= self.dic[t]
        return np.array(vec)

    def train_one_step(self, i: int):
        pass

    def save_model(self, fname: str="model.npy"):
        """
        @param fname <str> : ファイル名
        学習したベクトルを保存
        """

        np.save("models/result/" + fname, self.w)

    def load_model(self, fname: str="model.npy"):
        """
        @param fname <str> : ファイル名
        学習したモデルを読み込む
        """

        self.w = np.load("models/result/" + fname)
