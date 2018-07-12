from .model.logistic import Logistic
from sklearn.manifold import TSNE
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import TruncatedSVD
import numpy as np
import matplotlib.pyplot as plt


with open("models/dataset/concat.csv") as f:
    lines = [line.replace("\n", "") for line in f.readlines()]

train = lines[:-100]
test = lines[-100:]

train = {t[2:]: t[:2] for t in train}
test = {t[2:]: t[:2] for t in test}

train_sents = [k for k in train.keys()]
train_signs = [int(v) for v in train.values()]
test_sents = [k for k in test.keys()]
test_signs = [int(v) for v in test.values()]
model = Logistic(train_sents, train_signs)

model.train()

count = 0
llr_true = []
llr_false = []
llb_true = []
llb_false = []
print("predict, answer")
for t, sign in zip(test_sents, test_signs):
    p = model.predict(t)
    print(p[0], sign, p[1])
    if p[0] == sign:
        count += 1
    if sign == 1 and p[0] == 1:
        llr_true.append(p[2])
    elif sign == 1 and p[0] == -1:
        llr_false.append(p[2])
    elif sign == -1 and p[0] == -1:
        llb_true.append(p[2])
    else:
        llb_false.append(p[2])
print(count, len(test_signs))
print(count / len(test_signs))
print(model.t)
print(len(llr_true))
print(len(llr_false))
print(len(llb_true))
print(len(llb_false))

tsne = TSNE(n_components=2, perplexity=20)

array = np.array(llr_true + llb_false + llb_true + llr_false)
colors = ["orange"] * (len(llr_true) + len(llr_false)) + ["blue"] * (len(llb_true) + len(llb_false))
markers = ["o"] * len(llr_true) + ["*"] * len(llr_false) + ["o"] * len(llb_true) + ["*"] * len(llb_false)
x_reduced = tsne.fit_transform(array.data)
for i in range(len(x_reduced)):
    plt.scatter(x_reduced[i, 0], x_reduced[i, 1], c=colors[i], marker=markers[i])
px = np.linspace(np.min(x_reduced[:, 0]), np.max(x_reduced[:, 0]), 100)
py = -(model.w[0] * px) / model.w[1]
plt.plot(px, py)
plt.savefig("a.png")
