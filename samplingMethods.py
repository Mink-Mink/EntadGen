from constants import *
import secrets


def sampleFromFrequencyList(frequencyList):
    totalFrequency = sum([W.frequency for W in frequencyList])
    randomPick = secrets.randbelow(totalFrequency)
    for W in frequencyList:
        if randomPick < W.frequency:
            return W
        else:
            randomPick -= W.frequency


class SamplingStrategy:
    def __init__(self, exclusive, samplingNumbers):
        self.exclusive = exclusive
        self.samplingNumbers = samplingNumbers

    def getSamplingNumber(self):
        return sampleFromFrequencyList(self.samplingNumbers).value


defaultSamplingStrategy = lambda: SamplingStrategy(False, [SamplingData(1, 1)])


class SamplingData:
    def __init__(self, value, frequency, label=None, prefix=None, postfix=None):
        self.value = value
        self.frequency = frequency
        self.label = label
        self.prefix = prefix
        self.postfix = postfix

    def isLeaf(self):
        return not isinstance(self.value, list)

    def getPrefix(self, wordDictionary):
        if isinstance(self.prefix, str):
            return self.prefix
        else:
            return "".join(sampleBasedOnPointer(self.prefix, wordDictionary))

    def getPostfix(self, wordDictionary):
        if isinstance(self.postfix, str):
            return self.postfix
        else:
            return "".join(sampleBasedOnPointer(self.postfix, wordDictionary))

    @classmethod
    def fromObject(cls, dataObject):
        isDataObjectALeaf = not isinstance(dataObject[VAL_KEY], list)
        if isDataObjectALeaf:
            return SamplingData(dataObject[VAL_KEY], dataObject[FREQ_KEY])
        else:
            value = [parseFromObject(W) for W in dataObject[VAL_KEY]]
            frequency = dataObject[FREQ_KEY] if FREQ_KEY in dataObject else None
            if frequency == FREQUENCY_SUM_UP_CHILDREN:
                frequency = sum(W.frequency for W in value)
            return SamplingData(
                value,
                frequency,
                dataObject[LABEL_KEY],
                dataObject[PREFIX_KEY] if PREFIX_KEY in dataObject else "",
                dataObject[POSTFIX_KEY] if POSTFIX_KEY in dataObject else "",
            )


def sampleBasedOnPointer(samplingPointer, wordDictionary):
    if samplingPointer[TYPE_KEY] == SAMPLE_OTHER_WORD_GROUP_TYPE:
        return sampleRecursively(
            wordDictionary[samplingPointer[VAL_KEY]], wordDictionary
        )


def parseFromObject(dataObject):
    if VAL_KEY not in dataObject:
        samplingNumbers = [parseFromObject(W) for W in dataObject[SAMPLING_NUMBERS]]
        return SamplingStrategy(dataObject[EXCLUSIVE_KEY], samplingNumbers)

    return SamplingData.fromObject(dataObject)


def sampleRecursively(samplingObject, wordDictionary, prefix="", postfix=""):
    if samplingObject.isLeaf():
        return [f"{prefix}{samplingObject.value}{postfix}"]

    if wordDictionary[SAMPLING_STRATEGY_KEY][samplingObject.label].exclusive:
        return exclusiveSamplingStrategy(
            samplingObject, wordDictionary, prefix, postfix
        )
    else:
        return nonExclusiveSamplingStrategy(
            samplingObject, wordDictionary, prefix, postfix
        )


def exclusiveSamplingStrategy(samplingObject, wordDictionary, prefix, postfix):
    samplingNumber = wordDictionary[SAMPLING_STRATEGY_KEY][
        samplingObject.label
    ].getSamplingNumber()
    groupFrequencyList = [W for W in samplingObject.value]
    resultWordArray = []
    while samplingNumber > 0 and len(groupFrequencyList) > 0:
        sampledGroup = sampleFromFrequencyList(groupFrequencyList)
        resultWordArray += sampleRecursively(
            sampledGroup,
            wordDictionary,
            f"{prefix}{samplingObject.getPrefix(wordDictionary)}",
            f"{samplingObject.getPostfix(wordDictionary)}{postfix}",
        )
        sampledGroupIndex = [G.label for G in groupFrequencyList].index(
            sampledGroup.label
        )
        groupFrequencyList.pop(sampledGroupIndex)
        samplingNumber -= 1
    return resultWordArray


def nonExclusiveSamplingStrategy(samplingObject, wordDictionary, prefix, postfix):
    samplingNumber = wordDictionary[SAMPLING_STRATEGY_KEY][
        samplingObject.label
    ].getSamplingNumber()
    resultWordArray = []
    while samplingNumber > 0:
        sampledGroup = sampleFromFrequencyList(samplingObject.value)
        resultWordArray += sampleRecursively(
            sampledGroup,
            wordDictionary,
            f"{prefix}{samplingObject.getPrefix(wordDictionary)}",
            f"{samplingObject.getPostfix(wordDictionary)}{postfix}",
        )
        samplingNumber -= 1
    return resultWordArray
