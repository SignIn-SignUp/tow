import argparse
import os
import getpass
from settings import Settings
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


def get_new_pw_and_tkn():
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
        lambda p: p.add_argument("--quiet", "-q", action='store_true',
                                 help='Only errors will be printed')
    ]

    single_defaults = [
        lambda p: p.add_argument(
            "package", type=str, help='The name of the package'),
        lambda p: p.add_argument(
            "--version", "-v", type=str, required=True, help='The version of the package'),
        lambda p: p.add_argument(
            "--base", "-b", type=str, required=True, help='The base-url of the GitLab instance'),
        lambda p: p.add_argument(
            "--filename", "-f", type=str, help='How the pushed file will be called (recommended: don\'t specify for default)'),
        lambda p: p.add_argument("--project", type=str, required=True,
                                 help='Project name + namespace (namespace/project-name)')
    ]

    batch_defaults = [
        lambda p: p.add_argument(
            "--towfile", "-t", type=str, default=DEFAULT_PARSERFILE)
    ]

    add_subcommand(
        subparsers,
        'push-single',
        defaults + single_defaults +
        [lambda p: p.add_argument("--src", type=str, required=True)],
        help='push a single package'
    )
    add_subcommand(
        subparsers,
        'pull-single',
        defaults + single_defaults,
        help="pull a single package"
    )
    add_subcommand(
        subparsers,
        'push',
        defaults + batch_defaults,
        help=f'push packages specified in the {DEFAULT_PARSERFILE}'
    )
    add_subcommand(
        subparsers,
        'pull',
        defaults + batch_defaults,
        help=f'pull packages specified in the {DEFAULT_PARSERFILE}'
    )
    add_subcommand(
        subparsers,
        'init',
        [],
        help=f'save a access token for later use'
    )


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


def parse_args(cfg_parser, tokenrepo, args=None):
    prog_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        prog=prog_name, description=f'{prog_name} - a package manager for generic packages for the GitLab package registry.')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' +
                        read('VERSION').strip(),
                        help='Print verison infomation and exit')

    subparsers = parser.add_subparsers(help='Commands', dest='command')
    add_subcommands(subparsers=subparsers)

    args = parser.parse_args(args)

    if args.command:
        if args.command == 'init':
            pw, tkn = get_new_pw_and_tkn()
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
                       )],
                       settings=Settings(verbose=not args.quiet)
                       )
            )
        elif token:

            conf_file = args.towfile

            if not (os.path.exists(conf_file) and os.path.isfile(conf_file)):
                print(f'no such file {conf_file}')
                return None
            return (
                args.command,
                Config(
                    base=cfg_parser.get_base(conf_file),
                    token=token,
                    packages=cfg_parser.get_packages(conf_file),
                    settings=Settings(verbose=not args.quiet)
                )
            )

    parser.print_help()
    return None
