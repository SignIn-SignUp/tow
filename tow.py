
from os import path
from pathlib import Path
import sys
from global_packagedir import GlobalPackagedir
from package_controller import PackageController
from config_verifyer import verify_for_pull, verify_for_push
from package import Package

from local_packagedir import LocalPackagedir
from package_repo import PackageRepo
from gitlab_controller import GitLabController
import yml_config_parser
from cli import parse_args
from tokendir import Tokendir

PACKAGE_BASE = 'towed_packages'
GLOBAL_BASE = path.join(Path.home(), '.tow')
V_PRINT = None


def main(args=None):
    tpl = parse_args(
        cfg_parser=yml_config_parser,
        tokenrepo=Tokendir(base=GLOBAL_BASE),
        args=args
    )
    if tpl:
        cmd, config = tpl

        V_PRINT = print if config.settings.verbose else lambda *a, **k: None

        repo = PackageRepo(
            PackageController(
                LocalPackagedir(PACKAGE_BASE),
                GlobalPackagedir(GLOBAL_BASE)
            ),
            GitLabController(config.base, config.token)
        )
        if cmd == 'push':
            config.packages = [p for p in config.packages if p.src]
            V_PRINT(f'{[ p.name for p in config.packages]} will be pushed.')
            verify_for_push(config=config)
            for package in config.packages:
                V_PRINT(f'Pushig {package.name} ..', end='')
                push(package=package, repo=repo)
                V_PRINT(f'. done.')
        elif cmd == 'pull':
            verify_for_pull(config=config)
            for package in config.packages:
                V_PRINT(f'Pulling {package.name} ..', end='')
                pull(package=package, repo=repo)
                V_PRINT(f'. done.')


def pull(package: Package, repo):
    repo.get(package)


def push(package: Package, repo):
    repo.put(package)


if __name__ == "__main__":
    main()
