import ujson

from flask import Flask
from flask import request

from ner_extractor import NERExtractor

app = Flask(__name__)
ner = NERExtractor()


@app.route("/names")
def names():
    try:
        id = request.args.get("id")
        result = ner.names_by_id(id)
        if result is not None:
            return ujson.dumps(result, ensure_ascii=False)
        else:
            return ''
    except:
        return ''


if __name__ == "__main__":
    app.run(port=9301, debug=True)
