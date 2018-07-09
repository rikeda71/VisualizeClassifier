import MeCab
from gensim import corpora


neologd_path = "/usr/lib/mecab/dic/mecab-ipadic-neologd"
m = MeCab.Tagger("-d " + neologd_path)
m.parse("")


def tokenize(text: str) -> list:
    """
    @param text <str> : 1文
    @return <list> : 文中に含まれる形態素列
    文中に含まれる形態素群を返す
    """

    tokens = []
    node = m.parseToNode(text)
    while node:
        if node.feature.split(",")[0] in ["名詞", "動詞", "形容詞"]:
            tokens.append(node.surface)
        node = node.next
    return tokens


if __name__ == "__main__":
    with open("../dataset/concat.csv", "r") as f:
        words = [tokenize(line[2:]) for line in f.readlines()]
    dic = corpora.Dictionary(words)
    dic.filter_extremes()
    dic.save_as_text("../dataset/dic.txt")
