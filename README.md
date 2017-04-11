# jamman-rip

Extract and reorganize recordings from the JamMan loop sequencer by DigiTech.

The recording can also be timestretched with the --roundbpm option so that its bpm is a whole number.


## Usage
JamMan patch folder structure is as follows

    /JamManStereo
        /Patch01
            patch.xml
            /PhraseA/
            phrase.xml
            phrase.wav
        /Patch02
            patch.xml
            /PhraseA/
            phrase.xml
            phrase.wav


Running the command `python jamman-rip JamManStereo` produces the following files:

    loop01-98_552001bpm.wav
    loop02-118_10164bpm.wav

Running the command `python jamman-rip JamManStereo --roundbpm` produces the following files (with timestrech modification):

    loop01-99bpm.wav
    loop02-118bpm.wav


