from constants import *
from samplingMethods import *
import json
from collections import defaultdict


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
        parseFromObject(W) for W in wordDictionary[NATURE_KEY]
    ]

    for groupKey in [ADJ_KEY, OBJECT_KEY]:
        wordDictionary[groupKey] = [
            parseFromObject(W) for W in wordDictionary[groupKey]
        ]
    samplingStrategyDict = defaultdict(defaultSamplingStrategy)
    for samplingKey, samplingStrategy in wordDictionary[SAMPLING_STRATEGY_KEY].items():
        samplingStrategyDict[samplingKey] = parseFromObject(samplingStrategy)
    wordDictionary[SAMPLING_STRATEGY_KEY] = samplingStrategyDict
    return wordDictionary
