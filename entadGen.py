from constants import *
from fileLoading import *
from samplingMethods import *


def sampleEntad(wordDictionary):
    def sampleRandomType(key):
        return sampleRecursively(wordDictionary[key], wordDictionary)

    adjectives = sampleRandomType(ADJ_KEY)
    limitation = sampleRandomType(LIMITATION_KEY)
    print(f"ENTAD")
    print(
        f"shaped as {sampleRandomType(OBJECT_KEY)}{'' if len(adjectives) == 0 else f' that is {adjectives}'}"
    )
    print(
        f"has {sampleRandomType(NATURE_KEY)} nature with magic of {sampleRandomType(MAGIC_KEY)}"
    )
    print(f"limited due to {limitation}" if len(limitation) != 0 else "")


formatWordDictionary()
wordDictionary = loadWordDictionary()
sampleEntad(wordDictionary)
