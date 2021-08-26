#!/bin/bash

### This file needs to run with sudo!
[ "$UID" -eq 0 ] || exec sudo "$0" "$@"

CWD="$(pwd)"

apt-get install -y gcc git portaudio19-dev libfftw3-dev libsamplerate0-dev

TMPFOLDER=$(mktemp -d)
git clone --single-branch --branch python-rt https://github.com/tschechniker/BTrack.git $TMPFOLDER
cd $TMPFOLDER/modules-and-plug-ins/btrack-rt
python3 setup.py install
cd $CWD
rm -rf $TMPFOLDER
python3 setup.py install --force

CONFIG_DIR="/etc/pydiscodmx"

if [[ ! -d $CONFIG_DIR ]]; then
    mkdir $CONFIG_DIR
    cp pydiscodmx/pyDiscoDmx.dist.ini $CONFIG_DIR/pyDiscoDmx.ini
    cp pydiscodmx/fixtures.dist.json $CONFIG_DIR/fixtures.json
    mkdir $CONFIG_DIR/chases
fi

