from constants import *
from samplingMethods import *
import json
from collections import defaultdict
import os


def formatWordDictionary():
    dictionaries = os.listdir(WORD_LIST_FOLDER)
    for dictFileName in dictionaries:
        wordDictionary = loadWordDictionaryFile(dictFileName)
        with open(f"{WORD_LIST_FOLDER}{dictFileName}", "w") as wordDictionaryFile:
            json.dump(wordDictionary, wordDictionaryFile, sort_keys=True, indent=4)


def loadWordDictionary():
    wordDictionary = loadWordDictionaryFile(MAIN_WORD_DICTIONARY_FILENAME)
    wordDictionary = recursivelyLoadSubDictionaries(wordDictionary)
    return preProcessWordDictionary(wordDictionary)


def recursivelyLoadSubDictionaries(wordDictionary):
    dictionaryList = []
    for wordGroup in wordDictionary[DICTIONARY_KEY]:
        if FILENAME_KEY in wordGroup:
            loadedFile = loadWordDictionaryFile(wordGroup[FILENAME_KEY])
            wordGroup = {**wordGroup, **loadedFile[WORD_GROUP_KEY]}
            if SAMPLING_STRATEGY_KEY in loadedFile:
                wordDictionary[SAMPLING_STRATEGY_KEY] = {
                    **wordDictionary[SAMPLING_STRATEGY_KEY],
                    **loadedFile[SAMPLING_STRATEGY_KEY],
                }
        dictionaryList.append(wordGroup)
    wordDictionary[DICTIONARY_KEY] = dictionaryList
    return wordDictionary


def loadWordDictionaryFile(filename):
    with open(f"{WORD_LIST_FOLDER}{filename}") as wordDictionaryFile:
        return json.load(wordDictionaryFile)


def preProcessWordDictionary(wordDictionary):
    preProcessedWordDictionary = {}

    for wordGroup in wordDictionary[DICTIONARY_KEY]:
        preProcessedWordDictionary[wordGroup[LABEL_KEY]] = parseFromObject(wordGroup)

    samplingStrategyDict = defaultdict(defaultSamplingStrategy)
    for samplingKey, samplingStrategy in wordDictionary[SAMPLING_STRATEGY_KEY].items():
        samplingStrategyDict[samplingKey] = parseFromObject(samplingStrategy)
    preProcessedWordDictionary[SAMPLING_STRATEGY_KEY] = samplingStrategyDict
    return preProcessedWordDictionary
