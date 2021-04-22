import os
import json
import sys
from random import shuffle
from collections import namedtuple

DOWNLOADS = "/home/dan/Downloads"
REVERSO_PREFIX = 'reverso'
MAX_SENTENCE_LENGTH = 106
MAX_SENTENCES_PER_WORD = 2

def get_filename(lang):
    return f"{DOWNLOADS}/anki_importable_result_{lang}"

Directory = namedtuple('Directory', ['full_path','base','lang'])

def get_reverso_dirs():

    ret = []

    for dir, *_ in os.walk(DOWNLOADS):
        base = os.path.basename(dir)
        if base.startswith(REVERSO_PREFIX):
            lang = base.split("_")[-1]
            ret.append(Directory(dir,base,lang))
    
    return ret

def get_jsons_in_dir(dir):

    ret = []

    for filename in os.listdir(dir.full_path):
        if filename.startswith(REVERSO_PREFIX):
            full_path =  os.path.join(dir.full_path, filename)
            with open(full_path, "r" ) as f:
                json_data = json.load(f)
                ret.append(json_data)

    return ret
    
def get_anki_contents(jsons):

    def create_lines_from_json(json):

        def sanitize(s):
            return s.replace("@", "").replace("\n", "").replace("\r", "")

        def line_from_sentence(s):
            sanitized_front = sanitize(s["front"])
            sanitized_back = sanitize(s["back"])
            return f"{sanitized_front}@{sanitized_back}"

        sentences = json["sentences"]
        short_sentences = [s for s in sentences if len(s["front"]) < MAX_SENTENCE_LENGTH]
        lines = [line_from_sentence(s) for s in short_sentences]
        shuffle(lines)
        ret = lines[:MAX_SENTENCES_PER_WORD]
        return ret

    lines = []

    for json in jsons:
        lines.extend(create_lines_from_json(json))

    ret = "\n".join(lines)
    return ret

def main():

    dirs = get_reverso_dirs()

    jsons = [get_jsons_in_dir(d) for d in dirs]

    anki_contents = [get_anki_contents(js) for js in jsons]

    filenames = [get_filename(d.lang) for d in dirs]

    for filename, content in zip(filenames,anki_contents):
        with open(filename, "w") as f:
            f.write(content)

if __name__=="__main__":
    main()