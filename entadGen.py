# Idea here is to have a simple script someone can use to generate entad ideas
# Entad ideas are by necessity incomplete and require human input
#
from constants import *
from fileLoading import *
from samplingMethods import *


def sampleNRandomAdjectives(wordDictionary):
    return sampleUsingSamplingStrategy(
        wordDictionary[ADJ_KEY], wordDictionary[SAMPLING_STRATEGY_KEY]
    )


def sampleRandomObject(wordDictionary):
    return sampleUsingSamplingStrategy(
        wordDictionary[OBJECT_KEY], wordDictionary[SAMPLING_STRATEGY_KEY]
    )


def sampleRandomNature(wordDictionary):
    return sampleUsingSamplingStrategy(
        wordDictionary[NATURE_KEY], wordDictionary[SAMPLING_STRATEGY_KEY]
    )


def sampleRandomMagic(wordDictionary):
    return sampleUsingSamplingStrategy(
        wordDictionary[MAGIC_KEY], wordDictionary[SAMPLING_STRATEGY_KEY]
    )


def sampleEntad(wordDictionary):
    print(f"ENTAD")
    print(
        f"shaped as {sampleRandomObject(wordDictionary)} that is {sampleNRandomAdjectives(wordDictionary)}"
    )
    print(
        f"has {sampleRandomNature(wordDictionary)} nature with magic of {sampleRandomMagic(wordDictionary)}"
    )


formatWordDictionary()
wordDictionary = loadWordDictionary()
sampleEntad(wordDictionary)
