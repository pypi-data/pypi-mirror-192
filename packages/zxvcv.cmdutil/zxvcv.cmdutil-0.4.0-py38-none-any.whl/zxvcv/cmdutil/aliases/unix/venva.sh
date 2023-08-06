#!/bin/bash

if [[ $1 == --help || $1 == "" ]]; then
    echo "Activate python virtual env"
    echo "usage venva [--help] name"
    echo ""
    echo "arguments:"
    echo "  --help      show brief help message"
    echo "  name        anme of python virtual environment to activate"
else
    export _VENV_NAME=$1
    _venva () {
        source ~/pythonvenv/$_VENV_NAME/bin/activate
    }

    _venva
fi
