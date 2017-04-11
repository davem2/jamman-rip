#!/usr/bin/env python3

VERSION="0.1.0" # MAJOR.MINOR.PATCH | http://semver.org

import xml.etree.ElementTree as etree
import argparse
import os
import re
import shutil
import subprocess


def parse_commandline():
    parser = argparse.ArgumentParser(prog='jamman-rip', description='Tool for extracting recordings from the JamMan loop sequencer by DigiTech.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s v{0}'.format(VERSION))
    parser.add_argument('inputdir', help='directory containing JamMan patch folders')
    parser.add_argument('-o', '--outputdir', default='', help='directory to output ripped samples')
    parser.add_argument('--roundbpm', default=False, action='store_true', help='set sample bpm to nearest whole number (requires rubberband)')

    return parser.parse_args()


def main():
    args = parse_commandline()

    samples = parse_samples(args.inputdir)

    for sample in samples:
        print("\nProcessing {}".format(sample['path']))

        if args.roundbpm:
            sample['origbpm'] = sample['bpm']
            sample['bpm'] = str(round(float(sample['bpm'])))

        outfn = "loop{}-{}bpm.wav".format(sample['id'],sample['bpm'].replace('.','_'))
        outpath = os.path.join(args.outputdir,outfn)

        if args.roundbpm:
            print("Stretching sample..")
            rubberband(sample['path'], outpath, sample['origbpm'], sample['bpm'])
        else:
            shutil.copyfile(sample['path'], outpath)

        print("Generated {}".format(outpath))


def rubberband(infn, outfn, inbpm, outbpm):
    commandLine = ['rubberband', '-T', '{}:{}'.format(inbpm,outbpm), infn, outfn]
    print("{}".format(' '.join(commandLine)))
    proc = subprocess.Popen(commandLine)
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError("Timestrech failed for sample {}".format(infn))

    return


def getbpm(fn=None):
    xml = etree.parse(fn)

    return xml.find("{http://schemas.digitech.com/JamMan/Phrase}BeatsPerMinute").text


def parse_samples(directory=None):
    samples = []

    for patch in os.listdir(directory):
        path = os.path.join(directory,patch)
        if os.path.isdir(path):
            for phrase in os.listdir(path):
                path = os.path.join(directory,patch,phrase)
                if os.path.isdir(path) and os.path.isfile(os.path.join(path,"phrase.wav")):
                    sample = {}
                    sample['path'] = os.path.abspath(os.path.join(path,"phrase.wav"))
                    sample['bpm'] = getbpm(os.path.join(path,"phrase.xml"))
                    sample['id'] = re.search(r"Patch(\d{2})", patch).group(1)

                    samples.append(sample)

    return samples


if __name__ == "__main__":
    main()

