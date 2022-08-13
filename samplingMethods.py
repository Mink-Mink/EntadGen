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

    @classmethod
    def fromObject(cls, dataObject):
        if cls.isDataObjectALeaf(dataObject):
            return SamplingData(dataObject[VAL_KEY], dataObject[FREQ_KEY])
        else:
            return SamplingData(
                [parseFromObject(W) for W in dataObject[VAL_KEY]],
                dataObject[FREQ_KEY] if FREQ_KEY in dataObject else None,
                dataObject[LABEL_KEY],
                dataObject[PREFIX_KEY] if PREFIX_KEY in dataObject else "",
                dataObject[POSTFIX_KEY] if POSTFIX_KEY in dataObject else "",
            )

    @classmethod
    def isDataObjectALeaf(cls, dataObject):
        return not isinstance(dataObject[VAL_KEY], list)


def parseFromObject(dataObject):
    if VAL_KEY not in dataObject:
        samplingNumbers = [parseFromObject(W) for W in dataObject[SAMPLING_NUMBERS]]
        return SamplingStrategy(dataObject[EXCLUSIVE_KEY], samplingNumbers)

    return SamplingData.fromObject(dataObject)


def sampleUsingSamplingStrategy(
    samplingObject, samplingStrategyDict, prefix="", postfix=""
):
    if samplingObject.isLeaf():
        return [f"{prefix}{samplingObject.value}{postfix}"]

    samplingStrategy = samplingStrategyDict[samplingObject.label]

    prefix = f"{prefix}{samplingObject.prefix}"
    postfix = f"{samplingObject.postfix}{postfix}"

    if samplingStrategy.exclusive:
        groupFrequencyList = [W for W in samplingObject.value]
        labelList = [G.label for G in groupFrequencyList]
        resultWordArray = []
        samplingNumber = samplingStrategy.getSamplingNumber()
        while samplingNumber > 0 and len(labelList) > 0:
            sampledGroup = sampleFromFrequencyList(groupFrequencyList)
            resultWordArray += sampleUsingSamplingStrategy(
                sampledGroup, samplingStrategyDict, prefix, postfix
            )
            sampledGroupIndex = labelList.index(sampledGroup.label)
            labelList.pop(sampledGroupIndex)
            groupFrequencyList.pop(sampledGroupIndex)
            samplingNumber -= 1
        return resultWordArray
    else:
        sampledGroup = sampleFromFrequencyList(samplingObject.value)
        return sampleUsingSamplingStrategy(
            sampledGroup, samplingStrategyDict, prefix, postfix
        )
