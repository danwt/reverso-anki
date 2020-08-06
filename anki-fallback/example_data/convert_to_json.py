import json


def to_obj(word, lines):
    cards = []
    for front in lines:
        cards.append({"word": word, "front": front[:-1], "back": ""})
    return cards


arr_of_arrs = []


with open("mined-sentences.txt", "r") as f:
    while True:
        try:
            word, freq, num = next(f).split()
            lines = [next(f) for _ in range(int(num))]
            arr_of_arrs.append(to_obj(word, lines))
            next(f)
        except:
            break


with open("harry_potter_sentences.json", "w") as f:
    f.write(
        json.dumps(
            {"sentences": [item for subarr in arr_of_arrs for item in subarr]},
            ensure_ascii=False,
        )
    )

