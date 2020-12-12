import os
import json
from random import shuffle


import sys
DOWNLOADS = "/home/dan/Downloads"
TAKE = int(sys.argv[1])
print("Taking: ", TAKE)
MAX_SENTENCE_LENGTH = 106


def sanitize(s):
    return s.replace("@", "").replace("\n", "").replace("\r", "")


def italicize(sentence,word):
    # TODO: italicize -> need to lookup anki italicization syntax
    return sentence
    


def generate_filename(lang):
    return f"{DOWNLOADS}/anki_importable_result_{lang}"


def handle_file(lines, data):
    sentences = data["sentences"][: TAKE + 2]
    word = sentences[0]["word"]
    to_append = []
    for card in sentences:
        if len(card["front"]) < MAX_SENTENCE_LENGTH:
            line = sanitize(italicize(card["front"],word)) + "@" + sanitize(card["back"])
            to_append.append(line)
    to_append.sort(key=lambda x: len(x))
    lines += to_append[:TAKE]


for dir, *_ in os.walk(DOWNLOADS):
    dir_name = dir.split("/")[-1]
    if dir_name.startswith("reverso"):
        lang = dir_name.split("_")[-1]
        print(f"Processing {lang}")
        lines = []
        for filename in os.listdir(dir):
            if filename.startswith("reverso"):
                with open(
                    os.path.join(dir, filename), "r"
                ) as f:  # open in readonly mode
                    data = json.load(f)
                    handle_file(lines, data)

        shuffle(lines)
        with open(generate_filename(lang), "w") as f:
            for line in lines:
                f.write(line + "\n")

