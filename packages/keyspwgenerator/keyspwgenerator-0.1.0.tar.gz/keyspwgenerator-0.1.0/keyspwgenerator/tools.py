#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from typing import List, Dict
import string
from random import shuffle
from collections import Counter
import secrets as sec
import re


class CmdLine:
    """
    Class that creates password as an object and can apply various methods
    for updates and validation

    Attributes:
        length: Desired length of password
        strength_flag: Flag declaring that the user prefers a strong password.
            If applied, this will ignore legth input and create a strong
            password instead

    Methods:
        create_password: Creates password from input list of chars
        remove_chars: Input is a string of unwanted characters.
            Method removes these characters from the password string
            and replaces them with new characters
        remove_repeats: Removes duplicate values from
            password string. Replaces duplicates with
            new characters from chars list

    """

    password: str = ""
    str_values: str = "".join(
        [
            string.ascii_lowercase,
            string.ascii_uppercase,
            string.digits,
            string.punctuation,
        ]
    )

    def __init__(self, length: int, strong: bool) -> None:
        self.length = length
        self.strong = strong

    def create_password(self) -> None:
        if self.strong:
            new_pw: str = sec.choice(CmdLine.str_values)

            counter: int = len(new_pw)

            strong_pw: str = "\33[30m\33[42m\33[1mSTRONG PASSWORD\033[0m"

            while strength_checker(new_pw) != strong_pw:
                shuffled_str_vals: List[str] = list(CmdLine.str_values)
                shuffle(shuffled_str_vals)
                CmdLine.str_values = "".join(shuffled_str_vals)
                new_char: str = sec.choice(CmdLine.str_values[counter % 4])
                new_pw += new_char
                counter += 1

            CmdLine.password = new_pw
        else:
            CmdLine.password = "".join(
                [sec.choice(CmdLine.str_values) for num in range(self.length)]
            )

    def remove_chars(self, removals: str) -> None:
        for char in removals:
            if char in CmdLine.password:
                CmdLine.str_values = CmdLine.str_values.replace(char, "")
                new_char = sec.choice(CmdLine.str_values)
                CmdLine.password = CmdLine.password.replace(char, new_char)

    def remove_repeats(self) -> None:
        pw_dict: Dict[str, int] = Counter(CmdLine.password)

        self.remove_chars("".join(list(pw_dict.keys())))

        while len(pw_dict) < self.length:
            new_char = sec.choice(CmdLine.str_values)
            pw_dict[new_char] += 1

        CmdLine.password = "".join(list(pw_dict.keys()))

    def get_password(self) -> str:
        return CmdLine.password


def strength_checker(val: str) -> str:
    score: int = 0
    str_values: List[str] = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
    ]

    pw_lens: List[int] = [8, 12, 16, 20]

    char_lens: List[int] = [1, 2, 3]

    for ele in pw_lens:
        if len(val) >= ele:
            score += 1

    for item in str_values:
        item_arr: List[str] = re.findall(f"[{item}]", val)
        for ele in char_lens:
            if len(item_arr) >= ele:
                score += 1

    if len(set(val)) == len(val):
        score += 2
    else:
        score -= 2

    if score >= 14:
        return "\33[30m\33[42m\33[1mSTRONG PASSWORD\033[0m"
    elif score < 14 and score >= 7:
        return "\33[30m\33[43m\33[1mMEDIUM PASSWORD STRENGTH\033[0m"
    else:
        return "\33[30m\33[41m\33[1mWEAK PASSWORD STRENGTH\033[0m"
