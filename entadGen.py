# Idea here is to have a simple script someone can use to generate entad ideas
# Entad ideas are by necessity incomplete and require human input
#

import json
import secrets
from collections import defaultdict

WORD_LIST_FOLDER = "./WordLists/"
WORD_DICTIONARY_FILENAME = "wordDictionary.json"


class SamplingStrategy:
    def __init__(self, exclusive, samplingNumbers):
        self.exclusive = exclusive
        self.samplingNumbers = samplingNumbers

    def getSamplingNumber(self):
        return sampleFromFrequencyList(self.samplingNumbers).value

    @classmethod
    def fromObject(cls, dataObject):
        samplingNumbers = [WordData.fromObject(W) for W in dataObject[SAMPLING_NUMBERS]]
        return SamplingStrategy(dataObject[EXCLUSIVE_KEY], samplingNumbers)


defaultSamplingStrategy = lambda: SamplingStrategy(False, [WordData(1, 1)])

OBJECT_KEY = "objects"
ADJ_KEY = "adjectives"
NATURE_KEY = "nature"
SAMPLING_STRATEGY_KEY = "samplingStategy"

VAL_KEY = "value"
FREQ_KEY = "frequency"
LABEL_KEY = "label"
EXCLUSIVE_KEY = "exclusive"
SAMPLING_NUMBERS = "samplingNumbers"


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
        return [sampleFromFrequencyList(self.value).value]

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
    samplingStrategyDict = defaultdict(defaultSamplingStrategy)
    for samplingKey, samplingStrategy in wordDictionary[SAMPLING_STRATEGY_KEY].items():
        samplingStrategyDict[samplingKey] = SamplingStrategy.fromObject(
            samplingStrategy
        )
    wordDictionary[SAMPLING_STRATEGY_KEY] = samplingStrategyDict
    return wordDictionary


def sampleUsingSamplingStrategy(wordDictionary, groupKey):
    samplingStrategy = wordDictionary[SAMPLING_STRATEGY_KEY][groupKey]

    if samplingStrategy.exclusive:
        groupFrequencyList = [W for W in wordDictionary[groupKey]]
        labelList = [G.label for G in groupFrequencyList]
        resultWordArray = []
        samplingNumber = samplingStrategy.getSamplingNumber()
        while samplingNumber > 0 and len(labelList) > 0:
            sampledGroup = sampleFromFrequencyList(groupFrequencyList)
            resultWordArray.append(sampledGroup.sample())
            sampledGroupIndex = labelList.index(sampledGroup.label)
            labelList.pop(sampledGroupIndex)
            groupFrequencyList.pop(sampledGroupIndex)
            samplingNumber -= 1
        return resultWordArray
    else:
        sampledGroup = sampleFromFrequencyList(wordDictionary[groupKey])
        if isinstance(sampledGroup, WordData):
            return [sampledGroup.value]
        else:
            return sampledGroup.sample()


def sampleNRandomAdjectives(wordDictionary):
    return sampleUsingSamplingStrategy(wordDictionary, ADJ_KEY)


def sampleRandomObject(wordDictionary):
    return sampleUsingSamplingStrategy(wordDictionary, OBJECT_KEY)


def sampleRandomNature(wordDictionary):
    return sampleUsingSamplingStrategy(wordDictionary, NATURE_KEY)


def sampleEntad(wordDictionary):
    shape = sampleRandomObject(wordDictionary)
    primaryAdjectives = sampleNRandomAdjectives(wordDictionary)
    primaryNature = sampleRandomNature(wordDictionary)
    print(f"ENTAD")
    print(f"shaped as {shape} that is {primaryAdjectives}")
    print(f"has {primaryNature} nature")


formatWordDictionary()
wordDictionary = loadWordDictionary()
sampleEntad(wordDictionary)
