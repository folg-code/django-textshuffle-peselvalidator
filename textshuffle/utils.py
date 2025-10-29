import random
import re

def shuffle_text(text):
    def shuffle_word(word):
        if len(word) <= 3:
            return word
        middle = list(word[1:-1])
        random.shuffle(middle)
        return word[0] + "".join(middle) + word[-1]

    return re.sub(r'\w+', lambda m: shuffle_word(m.group()), text)