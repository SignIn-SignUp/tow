import argparse
import os
import getpass
import sys


from package import Package
from config import Config


DEFAULT_PARSERFILE = 'Towfile'


def add_subcommand(subparsers, name, add_args, help=None):
    parser = subparsers.add_parser(name, help=help)
    for a in add_args:
        a(parser)


def get_token(tokenrepo):
    token = None
    if tokenrepo.exists():
        token = tokenrepo.get(getpass.getpass(
            "Password for decrypting access token:"))
        if not token:
            token = getpass.getpass(
                "Access token could not be retrieved. The password might have been wrong.\nPlease enter one:")
    elif not token:
        token = getpass.getpass(
            "No access token found.\nPlease enter one:")
    return token


def get_pw_and_tkn():
    tkn = getpass.getpass(
        "Please enter access token:")
    pw = getpass.getpass(
        "Please enter a password to protect the token:")
    if not pw == getpass.getpass("Please repeat password:"):
        print("Passwords don't match.")
        return (None, None)

    return (pw, tkn)


def add_subcommands(subparsers):

    defaults = [
        lambda p: p.add_argument("package", type=str),
        lambda p: p.add_argument("--version", type=str, required=True),
        lambda p: p.add_argument("--base", type=str, required=True),
        lambda p: p.add_argument("--filename", type=str, required=True),
        lambda p: p.add_argument("--project", type=str, required=True)
    ]
    add_subcommand(
        subparsers,
        'push-single',
        defaults +
        [lambda p: p.add_argument("--src", type=str, required=True)],
        help='push a single package'
    )
    add_subcommand(
        subparsers,
        'pull-single',
        defaults,
        help="pull a single package"
    )
    add_subcommand(
        subparsers,
        'push',
        [lambda p: p.add_argument(
            "--file", type=str, default=DEFAULT_PARSERFILE)],
        help=f'push packages specified in the {DEFAULT_PARSERFILE}'
    )
    add_subcommand(
        subparsers,
        'pull',
        [lambda p: p.add_argument(
            "--file", type=str, default=DEFAULT_PARSERFILE)],
        help=f'pull packages specified in the {DEFAULT_PARSERFILE}'
    )
    add_subcommand(
        subparsers,
        'init',
        [],
        help=f'save a access token for later use'
    )


def parse_args(cfg_parser, tokenrepo, args=None):
    prog_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        prog=prog_name, description=f'{prog_name} - a package manager for generic packages on GitLab.')

    subparsers = parser.add_subparsers(help='Commands', dest='command')
    add_subcommands(subparsers=subparsers)

    args = parser.parse_args(args)

    if args.command:
        if args.command == 'init':
            pw, tkn = get_pw_and_tkn()
            tokenrepo.put(pw, tkn)
            return None

        token = get_token(tokenrepo=tokenrepo)

        if args.command.endswith('-single') and token:
            return (
                args.command.replace('-single', ''),
                Config(base=args.base,
                       token=token,
                       packages=[Package(
                           name=args.package,
                           version=args.version,
                           filename=args.filename,
                           project=args.project,
                           src=os.path.expanduser(
                               args.src
                           ) if args.command == 'push-single' else None
                       )]
                       )
            )
        elif token:

            conf_file = args.file

            if not (os.path.exists(conf_file) and os.path.isfile(conf_file)):
                print(f'no such file {conf_file}.')
                return None
            return (
                args.command,
                Config(
                    base=cfg_parser.get_base(conf_file),
                    token=token,
                    packages=cfg_parser.get_packages(conf_file)
                )
            )

    parser.print_help()
    return None
