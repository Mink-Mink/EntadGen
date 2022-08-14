# EntadGen by Mink-Mink

## What does this do

This script is meant to be an "idea engine" for generating entads - unique magic items.
Entad ideas this script generates are simply a list of shape, key areas of magic, and limitations; turning this into a complete magic items is left as an exercise to the user.

## Discord integration

This code has been integrated into a discord bot. To add it to your server, simply use this link: https://discord.com/api/oauth2/authorize?client_id=1008363355653799956&permissions=277025426432&scope=bot%20applications.commands

Currently the bot runs on my laptop, and would probably only be active about a quarter of the time; I am looking into cheap hosting possibilities which would reduce downtime to zero.

To generate an entad, use /entad slash command

## Installation

To run the script locally, you will require a minimum knowledge of programming. To install it, you want to clone the git repository, then use the following console commands in a console window from the repository root folder:

On windows:

```
python -m venv venv
./venv/Scripts/activate
pip install -r ./requirements.txt
python ./entadGen.py
```

On linux:

```
python3 -m venv venv
./venv/bin/activate
pip install -r ./requirements.txt
python ./entadGen.py
```

To generate a new entad, simply execute the script again.

## Output format

Here is an eample of the script output:

```
ENTAD
shaped as ['kitchen knife'] that is ['wooden', 'red', 'miniscule']
has ['travel'] nature with magic of ['Aerokinesis (normal)']
limited due to ['effect distance: room-scope']
```

Going from the beginning you can see that the script gives you a randomly generated common object that is the shape of the entad, followed by a set of discriptors. Currently, material, color and size descriptors are in place.

Next line has entad nature. This can be "offensive", "defensive", "storage", "travel" and "metamagic", and describes the broad area of focus for the entad.

* Offensive entads damage or otherwise affect enemies
* Defensive entads protect friends
* Storage entads are used to transport or store a bunch of stuff; bag of holding is a classic example
* Travel entads make you travel faster or over a long distance or make this travel easier
* Metamagic entads affect other entads or magic itself. These are generally very powerful.

Following entad nature, there is a list of descriptors for the magic of the entad itself. This can include one or more elements, with each element having a strength rating in brackets. Strength can be "minor", "normal", "major" and "world-class", depending on how strong the entad in question is.

Final line has the limitations of the entad. This can include things like what can be affected by it and at what distance.

To turn this into a full entad, we apply a little bit of creativity to these descriptors; in this case, we can imagine a tiny wooden kitchen knife, which, when pointed in a direction, can quickly move you there with bursts of air; however, the maximum distance it can move you is only the size of a room, so at most a hundred feet.

## Word dictionaries

All random idea generation in this script is based on dictionaries of various words, with frequencies of usage associated with them.

## TODO

* Describe word dictionaries in actual detail
* Add more limitations and adjectives
* figure out hosting?
* Add a function to list out the probabilities of all the options
* Go through the dictionaries and tinker with odds

## Art license

Thumbnail art for the bot was generated using [Stable Diffusion](https://stability.ai/blog/stable-diffusion-announcement), and is in the public domain.
