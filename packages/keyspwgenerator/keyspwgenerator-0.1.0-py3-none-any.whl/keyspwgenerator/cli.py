#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import click
from keyspwgenerator.tools import CmdLine, strength_checker


@click.command()
@click.option(
    "--length",
    "-l",
    "length",
    required=False,
    default=8,
    type=int,
    help="Length of desired password",
)
@click.option(
    "--remove",
    "-r",
    "remove",
    required=False,
    type=str,
    help="Values or characters to be excluded from the created \
        password (Enter values as a string... ex: 'j9_@Dy]'",
)
@click.option(
    "--no_repeats",
    "-n",
    "no_repeats",
    required=False,
    is_flag=True,
    default=False,
    help="Ensures there are no duplicate characters",
)
@click.option(
    "--check",
    "-c",
    "check",
    required=False,
    type=str,
    help="Checks string and returns password strength rating",
)
@click.option(
    "--strong",
    "-s",
    "strong",
    required=False,
    is_flag=True,
    help="Ignores length input and instead returns a strong password",
)
def main(
    length: int, remove: str, no_repeats: str, check: str, strong: bool
) -> None:  # main function
    """CLI app that creates a password for you!

    This function will create a random password for you. Default
    password length is 8 but can be changed by implementing the proper
    option. Refer to the --help option for more guides.

    Arguments:
        length: Desired length of password. Default is 8 characters.
        remove: Option that ensures characters are exempt (input as string)
        no_repeats: Flag that disables repeated characters
        check:  Reviews password input and provides a strength rating
    """

    # check password strength
    if check:
        click.echo(strength_checker(check))
    elif strong:
        pw = CmdLine(length=length, strong=strong)

        pw.create_password()

        click.echo(pw.get_password())
    else:
        # instantiate password object
        pw = CmdLine(length=length, strong=strong)

        pw.create_password()

        if remove:
            pw.remove_chars(remove)
        elif no_repeats:
            pw.remove_repeats()

        click.echo(pw.get_password())


if __name__ == "__main__":
    main()
