
import os

from package import Package
from config import Config


def verify_basic_conf(config: Config):
    if not config.base:
        raise Exception('base not valid')
    if not config.token:
        raise Exception('token not valid')


def verify_basic_package(package: Package):
    if not package.name:
        raise Exception('package name not valid')
    if not package.version:
        raise Exception(f'version of {package.name} not valid')
    if not package.project:
        raise Exception(f'project of {package.name} not valid')
    if not len(package.project.split('/')) == 2:
        raise Exception(
            f'project of {package.name} does not contain exactly one namespace'
        )
    if not package.filename:
        raise Exception(f'filename of {package.name} not valid')
    if not package.filename.endswith('tar.gz'):
        raise Exception(f'filename of {package.name} must end with tar.gz')
    if not os.path.split(package.filename)[0] == '':
        raise Exception(
            f'filename of {package.name} can not be a path or directory')


def verify_pull_package(package: Package):
    verify_basic_package(package=package)


def verify_push_package(package: Package):
    verify_basic_package(package=package)
    if not package.src:
        raise Exception(f'src of {package.name} not valid')
    if not os.path.exists(package.src):
        raise Exception(f'src of {package.name} does not exist')


def verify_for_push(config: Config):
    verify_basic_conf(config=config)
    for p in config.packages:
        verify_push_package(p)


def verify_for_pull(config: Config):
    verify_basic_conf(config=config)
    for p in config.packages:
        verify_pull_package(p)
