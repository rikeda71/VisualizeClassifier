import numpy as np
from copy import deepcopy


class Model(object):

    def __init__(self, train_data: list, signs: list, theta: float=10e-3):
        """
        @param train_data <list> : 学習データのベクトル群
        @param signs <list> : 学習データのクラス（+1, -1）
        @param theta <float> : 学習の閾値
        """

        self.train_data = train_data
        self.signs = signs
        self.__theta = theta
        self.__n = len(self.train_data)
        self.__w = np.random.random(self.__n)
        self.__t = 0
        self.end = False

    def train(self, max_iteration: int=1000):
        """
        @param max_iteration <int> : 最大学習回数
        学習機の学習を行う
        """

        cnt = 0
        while not self.end and cnt < max_iteration:
            i = np.random.randint(0, self.__n)
            self.train_one_step(i)
            cnt += 1
        self.save_model()

    def train_one_step(self, i: int):
        pass

    def save_model(self, fname: str="model.npy"):
        """
        @param fname <str> : ファイル名
        学習したベクトルを保存
        """

        np.save("../result/" + fname)

    def load_model(self, fname: str="model.npy"):
        """
        @param fname <str> : ファイル名
        学習したモデルを読み込む
        """

        self.__w = np.load("../result/" + fname)
