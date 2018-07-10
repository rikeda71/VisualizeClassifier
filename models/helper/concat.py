import random


def concat():
    data = []
    # データの読み込み
    for k in ["p", "n"]:
        tag = "+1" if k == "p" else "-1"
        with open("models/dataset/" + k + ".csv", "r") as f:
            for line in f.readlines():
                data.append(tag + line)

    # データのシャッフル
    random.shuffle(data)

    # データの結合
    text = "".join(data)
    with open("models/dataset/concat.csv", "w") as f:
        f.write(text)


if __name__ == "__main__":
    concat()
