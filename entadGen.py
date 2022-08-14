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


if __name__ == "__main__":
    formatWordDictionary()
    wordDictionary = loadWordDictionary()
    print(sampleEntad(wordDictionary))
