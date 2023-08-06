#!/bin/bash

# path to the project directory
export PATH_REPO="$(dirname "$BASH_SOURCE")"
export PATH_REPO="$(realpath "$PATH_REPO")"

# path to the development virtual environment
export BASE_NAME="$(basename "$PATH_REPO")"
export PATH_VENV=~/.venv/dev/$BASE_NAME

# deactivate the (potential) current virtual environment
workoff() {
    deactivate > /dev/null 2>&1 || true
}

# activate the development virtual environment
workon() {
    source $PATH_VENV/bin/activate
}

# create and activate the development virtual environment
install() {
    workoff
    if test -d "$PATH_VENV"
    then
        workon
    else
        echo "creating virtual environment $PATH_VENV"
        python3 -m venv $PATH_VENV
        workon
        python3 -m pip install --upgrade pip
        python3 -m pip install --upgrade build
        python3 -m pip install --upgrade twine
        python3 -m pip install --upgrade sphinx
        python3 -m pip install --upgrade sphinx-rtd-theme
        python3 -m pip install --upgrade myst-parser
        python3 -m pip install --editable $PATH_REPO
    fi
}

# deactivate and remove the development virtual environment
uninstall() {
    workoff
    if [ -d "$PATH_VENV" ]
    then
        echo "deleting virtual environment $PATH_VENV"
        rm --recursive $PATH_VENV
    fi
}

# recreate the development virtual environment
reinstall() {
    uninstall
    install
}

install
