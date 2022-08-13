from constants import *
from fileLoading import *
from samplingMethods import *


def sampleEntad(wordDictionary):
    def sampleRandomType(key):
        return sampleRecursively(wordDictionary[key], wordDictionary)

    print(f"ENTAD")
    print(
        f"shaped as {sampleRandomType(OBJECT_KEY)} that is {sampleRandomType(ADJ_KEY)}"
    )
    print(
        f"has {sampleRandomType(NATURE_KEY)} nature with magic of {sampleRandomType(MAGIC_KEY)}"
    )
    print(f"limited due to {sampleRandomType(LIMITATION_KEY)}")


formatWordDictionary()
wordDictionary = loadWordDictionary()
sampleEntad(wordDictionary)
