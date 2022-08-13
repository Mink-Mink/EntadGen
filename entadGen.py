# Idea here is to have a simple script someone can use to generate entad ideas
# Entad ideas are by necessity incomplete and require human input
#
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
    print(f"limited due to {sampleRandomType(LIMITATION_KEY)} with vibe of ")


formatWordDictionary()
wordDictionary = loadWordDictionary()
sampleEntad(wordDictionary)
