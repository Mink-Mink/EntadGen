from constants import *
from fileLoading import *
from samplingMethods import *


def sampleEntad(wordDictionary):
    def sampleRandomType(key):
        return sampleRecursively(wordDictionary[key], wordDictionary)

    adjectives = sampleRandomType(ADJ_KEY)
    limitation = sampleRandomType(LIMITATION_KEY)
    return (
        "\n".join(
            [
                "ENTAD",
                f"shaped as {sampleRandomType(OBJECT_KEY)}{'' if len(adjectives) == 0 else f' that is {adjectives}'}",
                f"has {sampleRandomType(NATURE_KEY)} nature with magic of {sampleRandomType(MAGIC_KEY)}",
                f"limited due to {limitation}" if len(limitation) != 0 else "",
            ]
        )
    ).strip()


def writeFrequencyTable(wordDictionary):
    for key in [LIMITATION_KEY, NATURE_KEY, ADJ_KEY, MAGIC_KEY, OBJECT_KEY]:
        writeFrequencySubTable(wordDictionary[key], wordDictionary)
        print("\n\n")


def writeFrequencySubTable(
    samplingObject, wordDictionary, probability=1.0, layer=0, prefix="", postfix=""
):
    print(
        f"{'-'*layer} {probability*100:.3} {prefix}{samplingObject.getText()}{postfix}"
    )
    if isinstance(samplingObject.value, list) and layer == 0:
        totalOdds = sum(O.oddsRatio for O in samplingObject.value)
        for O in samplingObject.value:
            writeFrequencySubTable(
                O,
                wordDictionary,
                probability * O.oddsRatio / totalOdds,
                layer + 1,
                f"{prefix}{samplingObject.getPrefix(wordDictionary)}",
                f"{samplingObject.getPostfix(wordDictionary)}{postfix}",
            )


if __name__ == "__main__":
    formatWordDictionary()
    wordDictionary = loadWordDictionary()
    # writeFrequencyTable(wordDictionary)
    print(sampleEntad(wordDictionary))
