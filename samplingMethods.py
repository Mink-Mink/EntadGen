from constants import *
import secrets


class SamplingStrategy:
    def __init__(self, exclusive, samplingNumbers):
        self.exclusive = exclusive
        self.samplingNumbers = samplingNumbers

    def getSamplingNumber(self):
        return sampleFromFrequencyList(self.samplingNumbers).value


defaultSamplingStrategy = lambda: SamplingStrategy(False, [SampleData(1, 1)])


def sampleFromFrequencyList(frequencyList):
    totalFrequency = sum([W.frequency for W in frequencyList])
    randomPick = secrets.randbelow(totalFrequency)
    for W in frequencyList:
        if randomPick < W.frequency:
            return W
        else:
            randomPick -= W.frequency


class SampleData:
    def __init__(self, value, frequency):
        self.value = value
        self.frequency = frequency


class SamplingList:
    def __init__(self, value, frequency, label):
        self.value = value
        self.frequency = frequency
        self.label = label

    def sample(self):
        return [sampleFromFrequencyList(self.value).value]


def parseFromObject(dataObject):
    if VAL_KEY not in dataObject:
        samplingNumbers = [parseFromObject(W) for W in dataObject[SAMPLING_NUMBERS]]
        return SamplingStrategy(dataObject[EXCLUSIVE_KEY], samplingNumbers)

    if isinstance(dataObject[VAL_KEY], list):
        valueArray = [parseFromObject(W) for W in dataObject[VAL_KEY]]
        return SamplingList(valueArray, dataObject[FREQ_KEY], dataObject[LABEL_KEY])
    else:
        return SampleData(dataObject[VAL_KEY], dataObject[FREQ_KEY])


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
        if isinstance(sampledGroup, SampleData):
            return [sampledGroup.value]
        else:
            return sampledGroup.sample()
