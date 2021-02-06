import os
import json
import sys
from random import shuffle

DOWNLOADS = "/home/dan/Downloads"
MAX_SENTENCE_LENGTH = 106
num_sentences_to_take_per_word = int(sys.argv[1])
print("Taking: ", num_sentences_to_take_per_word)
PREFIX = 'reverso'


def sanitize(s):
    return s.replace("@", "").replace("\n", "").replace("\r", "")


def italicize(sentence,word):
    # TODO: italicize -> need to lookup anki italicization syntax
    return sentence

def get_filename(lang):
    return f"{DOWNLOADS}/anki_importable_result_{lang}"

def handle_file(lines, data):
    sentences = data["sentences"][: num_sentences_to_take_per_word + 2]
    word = sentences[0]["word"]
    to_append = []
    for card in sentences:
        if len(card["front"]) < MAX_SENTENCE_LENGTH:
            line = sanitize(italicize(card["front"],word)) + "@" + sanitize(card["back"])
            to_append.append(line)
    to_append.sort(key=lambda x: len(x))
    lines += to_append[:num_sentences_to_take_per_word]


for dir, *_ in os.walk(DOWNLOADS):
    dir_name = dir.split("/")[-1]
    if dir_name.startswith(PREFIX):
        lang = dir_name.split("_")[-1]
        print(f"Processing {lang}")
        lines = []
        for filename in os.listdir(dir):
            if filename.startswith(PREFIX):
                with open(
                    os.path.join(dir, filename), "r"
                ) as f:
                    data = json.load(f)
                    handle_file(lines, data)

        shuffle(lines)
        with open(get_filename(lang), "w") as f:
            for line in lines:
                f.write(line + "\n")

