from os import path
import os
import tarfile


class LocalPackagedir:

    def __init__(self, base) -> None:
        self.base = base
        self.basedir = path.join(os.getcwd(), base)

    def exists(self, package):
        return path.exists(path.join(self.basedir, package.name, package.version))

    def put(self, package, path):
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

        with tarfile.open(path) as f:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(f, os.path.join(self.basedir,package.name,package.version))
                os.path.join(self.basedir, package.name, package.version)
            )
