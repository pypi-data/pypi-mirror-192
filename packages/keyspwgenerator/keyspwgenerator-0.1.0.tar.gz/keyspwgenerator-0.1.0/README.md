# Keys (Password Generator)

![python](https://img.shields.io/badge/Python-3.8%2C%203.9%2C%203.10%2C%203.11-blue)
[![pip install](https://img.shields.io/badge/pip%20install-click-blue)](https://palletsprojects.com/p/click/)
[![license](https://img.shields.io/badge/License-MIT-blue)](https://opensource.org/license/mit/)
[![Testing](https://github.com/jsattari/keys/actions/workflows/tests.yaml/badge.svg)](https://github.com/jsattari/keys/actions/workflows/tests.yaml)
[![codecov](https://codecov.io/gh/jsattari/keys/branch/master/graph/badge.svg?token=8XQ4MXVR3M)](https://codecov.io/gh/jsattari/keys)

---

## Introduction to Keys

Keys is a password generator that creates new passwords from uppercase letters, lowercase letters, digits, and special characters all within the Terminal.

## Installation

    pip3 install keys

## Usage

    Usage: keys [OPTIONS]

        CLI app that creates a password for you!

    Options:
        -l, --length INTEGER  Length of desired password. Will default to 8
                                if flag is not used
        -r, --remove TEXT     Values or characters to be excluded from the created
                                password (Enter values as a string... ex: 'j9_@Dy]'
        -n, --no_repeats      Ensures there are no duplicate characters
        -c, --check TEXT      Checks string and returns password strength rating
        -s, --strong          Ignores length input and instead returns a strong
                                password
        --help                Show this message and exit.

## Notes

- Works with Python 3.8^
