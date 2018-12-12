import asyncio
import ujson
from collections import defaultdict

from natasha import NamesExtractor


class NERExtractor:
    extractor = NamesExtractor()

    def names(self, text):
        return [match.fact for match in self.extractor(text)]

    async def names_by_id(self, id):
        try:
            with open("../data/{}.json".format(id)) as file:
                book = ujson.loads(file.read())
                if book.get("text") is not None:
                    names = [
                        self.format_name(name) for name in self.names(book["text"])
                    ]
                    result = defaultdict(int)
                    for name in names:
                        result[name] += 1

                    return dict(result)
                else:
                    return None
        except:
            pass

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
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(extractor.names_by_id(101))
    print(result)
    loop.close()
