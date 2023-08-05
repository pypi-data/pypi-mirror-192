import json
import os

class js:
    def write(data, filename):
        data = json.dumps(data)
        data = json.loads(str(data))
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def read(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

class code:
    def decodeText(text, code):
        text.decode(code)
    def encodeText(text, code):
        return text.encode(code)
