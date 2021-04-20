# jamman-rip

Extract and reorganize recordings from the JamMan loop sequencer by DigiTech.

The bpm of the extracted sample(s) is given in the sample file name. JamMan uses tap tempo which generates fractional values for bpm. If whole number bpm is desired, the recording can be timestretched with the --roundbpm option.


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


Running the command `python jamman-rip.py JamManStereo` produces the following files:

    loop01-98_552001bpm.wav (98.552001bpm)
    loop02-118_10164bpm.wav (118.10164bpm)

Running the command `python jamman-rip.py JamManStereo --roundbpm` produces the following files (with timestrech modification):

    loop01-99bpm.wav (99bpm)
    loop02-118bpm.wav (118bpm)


