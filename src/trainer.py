from .model.logistic import Logistic
from .helper.getvec import getvec


with open("dataset/concat.csv") as f:
    lines = [line.replace("\n", "") for line in f.readlines()]

index = int(len(lines) * 0.9)
train = lines[:index]
test = lines[index:]

train = {t[2:]: t[:2] for t in train}
test = {t[2:]: t[:2] for t in test}

train_sents = [k for k in train.keys()]
train_signs = [int(v) for v in train.values()]
test_sents = [k for k in test.keys()]
test_signs = [int(v) for v in test.values()]
model = Logistic(train_sents, train_signs)

model.train()

count = 0
print("predict, answer")
for t, sign in zip(test_sents, test_signs):
    p = model.predict(t)
    print(p[0], sign, p[1])
    count += 1 if p[0] == sign else 0
print(count, len(test_signs))
print(count / len(test_signs))
print(model.t)
