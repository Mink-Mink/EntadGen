# Idea here is to have a simple script someone can use to generate entad ideas
# Entad ideas are by necessity incomplete and require human input
#

import json
import secrets

WORD_LIST_FOLDER = "./WordLists/"
WORD_DICTIONARY_FILENAME = "wordDictionary.json"

OBJECT_KEY = "objects"
ADJ_KEY = "adjectives"
NATURE_KEY = "nature"

VAL_KEY = "value"
FREQ_KEY = "frequency"
LABEL_KEY = "label"


def sampleFromFrequencyList(frequencyList):
    totalFrequency = sum([W.frequency for W in frequencyList])
    randomPick = secrets.randbelow(totalFrequency)
    for W in frequencyList:
        if randomPick < W.frequency:
            return W
        else:
            randomPick -= W.frequency


class WordData:
    def __init__(self, value, frequency):
        self.value = value
        self.frequency = frequency

    @classmethod
    def fromObject(cls, dataObject):
        return WordData(dataObject[VAL_KEY], dataObject[FREQ_KEY])


class WordList:
    def __init__(self, value, frequency, label):
        self.value = value
        self.frequency = frequency
        self.label = label

    def sample(self):
        return sampleFromFrequencyList(self.value).value

    @classmethod
    def fromObject(cls, dataObject):
        wordArray = [WordData.fromObject(W) for W in dataObject[VAL_KEY]]
        return WordList(wordArray, dataObject[FREQ_KEY], dataObject[LABEL_KEY])


def formatWordDictionary():
    wordDictionary = loadWordDictionaryFile()
    with open(
        f"{WORD_LIST_FOLDER}{WORD_DICTIONARY_FILENAME}", "w"
    ) as wordDictionaryFile:
        json.dump(wordDictionary, wordDictionaryFile, sort_keys=True, indent=4)


def loadWordDictionary():
    wordDictionary = loadWordDictionaryFile()
    return preProcessWordDictionary(wordDictionary)


def loadWordDictionaryFile():
    with open(f"{WORD_LIST_FOLDER}{WORD_DICTIONARY_FILENAME}") as wordDictionaryFile:
        return json.load(wordDictionaryFile)


def preProcessWordDictionary(wordDictionary):
    wordDictionary[NATURE_KEY] = [
        WordData.fromObject(W) for W in wordDictionary[NATURE_KEY]
    ]

    for groupKey in [ADJ_KEY, OBJECT_KEY]:
        wordDictionary[groupKey] = [
            WordList.fromObject(W) for W in wordDictionary[groupKey]
        ]
    return wordDictionary


def sampleNWordsFromExclusiveGroupList(wordDictionary, groupKey, N=1, exclusive=False):
    groupFrequencyList = wordDictionary[groupKey]

    if exclusive:
        labelList = [G.label for G in groupFrequencyList]
        resultWordArray = []
        while N > 0 and len(labelList) > 0:
            sampledGroup = sampleFromFrequencyList(groupFrequencyList)
            resultWordArray.append(sampledGroup.sample())
            sampledGroupIndex = labelList.index(sampledGroup.label)
            labelList.pop(sampledGroupIndex)
            groupFrequencyList.pop(sampledGroupIndex)
            N -= 1
        return resultWordArray
    else:
        sampledGroup = sampleFromFrequencyList(groupFrequencyList)
        if isinstance(sampledGroup, WordData):
            return sampledGroup.value
        else:
            return sampledGroup.sample()


def sampleNRandomAdjectives(wordDictionary, N):
    return sampleNWordsFromExclusiveGroupList(wordDictionary, ADJ_KEY, N, True)


def sampleRandomNoun(wordDictionary):
    return sampleNWordsFromExclusiveGroupList(wordDictionary, OBJECT_KEY)


def sampleRandomNature(wordDictionary):
    return sampleNWordsFromExclusiveGroupList(wordDictionary, NATURE_KEY)


def sampleEntad(wordDictionary):
    shape = sampleRandomNoun(wordDictionary)
    primaryAdjectives = sampleNRandomAdjectives(wordDictionary, 2)
    primaryNature = sampleRandomNature(wordDictionary)
    print(f"ENTAD")
    print(f"[{shape}] that is {primaryAdjectives}")
    print(f"has [{primaryNature}] nature")


formatWordDictionary()
wordDictionary = loadWordDictionary()
sampleEntad(wordDictionary)
