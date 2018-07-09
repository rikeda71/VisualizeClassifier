import random


data = []
# データの読み込み
for k in ["p", "n"]:
    tag = "+1" if k == "p" else "-1"
    with open("../dataset/" + k + ".csv", "r") as f:
        for line in f.readlines():
            data.append(tag + line)

# データのシャッフル
random.shuffle(data)

# データの結合
text = "".join(data)
with open("../dataset/concat.csv", "w") as f:
    f.write(text)
