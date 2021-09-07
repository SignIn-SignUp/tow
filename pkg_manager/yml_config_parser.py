import os
from .package import Package
import yaml


class YMLConfigParser():

    def get_packages(self, path: str):
        with open(path, 'r') as stream:
            try:
                return [
                    Package(
                        name=key,
                        version=val['version'],
                        filename=val['filename'] if 'filename' in val.keys(
                        ) else f'{key}.tar.gz',
                        project=val['project'],
                        src=os.path.expanduser(
                            val['src']
                        ) if 'src' in val.keys() else None
                    )
                    for key, val in yaml.safe_load(stream)['gitlab']['packages'].items()
                ]
            except yaml.YAMLError as exc:
                raise exc

    def get_base(self, path: str):
        with open(path, 'r') as stream:
            try:
                return yaml.safe_load(stream)['gitlab']['base']
            except yaml.YAMLError as exc:
                raise exc
