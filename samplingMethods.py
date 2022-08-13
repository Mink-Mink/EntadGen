from constants import *
import secrets


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


def sampleUsingSamplingStrategy(wordDictionary, groupKey):
    samplingStrategy = wordDictionary[SAMPLING_STRATEGY_KEY][groupKey]

    if samplingStrategy.exclusive:
        groupFrequencyList = [W for W in wordDictionary[groupKey]]
        labelList = [G.label for G in groupFrequencyList]
        resultWordArray = []
        samplingNumber = samplingStrategy.getSamplingNumber()
        while samplingNumber > 0 and len(labelList) > 0:
            sampledGroup = sampleFromFrequencyList(groupFrequencyList)
            resultWordArray += sampledGroup.sample()
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
