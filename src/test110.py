import markovify
import nltk
import re
import pickle
import os

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

combined_model = None
for (dirpath, _, filenames) in os.walk("Data/story"):
    for filename in filenames:
        with open(os.path.join(dirpath, filename)) as f:
            model = POSifiedText(f, retain_original=False)
            if combined_model:
                combined_model = markovify.combine(models=[combined_model, model])
            else:
                combined_model = model
with open("story.pkl", "wb") as file:
    pickle.dump(combined_model, file)
t = ""
for i in range(6):
    t += combined_model.make_sentence()

print(t)
