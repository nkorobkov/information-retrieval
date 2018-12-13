import ujson
from collections import defaultdict

import numpy as np
from natasha import NamesExtractor


class NERExtractor:
    extractor = NamesExtractor()

    def names(self, text):
        return [match.fact for match in self.extractor(text)]

    def names_by_id(self, id):
        try:
            with open("../data/{}.json".format(id)) as file:
                book = ujson.loads(file.read())
                names = [self.format_name(name) for name in self.names(book["text"])]

                result = defaultdict(int)
                for name in names:
                    result[name] += 1

                return self.most_freq(dict(result))
        except:
            raise KeyError

    @staticmethod
    def most_freq(names: dict):
        names = [(name, names[name]) for name in names.keys()]
        indices = np.array([k for name, k in names]).argsort()[-3:][::-1]
        return [names[i][0] for i in indices]

    @staticmethod
    def format_name(name):
        if name.first is not None and name.last is not None:
            return "{} {}".format(name.first, name.last)
        elif name.first is None:
            return name.last
        else:
            return name.first


if __name__ == "__main__":
    extractor = NERExtractor()
    result = extractor.names_by_id(101)
    print(result)
