# tow

A package manager for generic package registry in GitLab. \
Every group or project in GitLab has a package registry in which generic packages can be stored and retrived from.
> This project is still under development. 

Packages can be pushed and pulled from a prject or group either specified in a Towfile or via the cli.
The access has to be granted via a private/project access token. This token can be provided dynamicaly or saved by initializing __tow__.

## cli

### Initializing

__tow__ can be initialized to store a access token ba calling: 
```{bash}
tow init
```

Tow then prompts to provide the acess token and a password to protect it. This password has to be entered each time when pushing or pulling. Alternatively the token can be provided each time when pushing and pulling.

### Pushing Packages 

When pushing packages the contents of a source directory will be tared and uplodad to the base under the specified package name and version. The archive will be named afer the value in ```--filename```. If no value is specified the archive will be named package name with __tar.gz__ postfix.

#### Pushing a single package
```{bash}
tow push-single --version VERSION --base GITLABBASE [ --filename PACKAGEFILENAME] --project PROJECT --src SRCDIR PACKAGENAME
```

An example:
```{bash}
tow push-single --version 1.2.0 --base http://gitlab.com --project nmaespace/project --src path/to/package/dir a_new_package
```

#### Pushing from the Towfile

```{bash}
tow pull [--towfile FILE]
```

An example:
```{bash}
tow pull
```
```{bash}
tow pull --towfile Towformatedfile
```

### Pulling Packages

When pulling packages the packages will be downloaded from base and unpacked in the current directory into __towed_packages/packagename/version/__. The archives will nbe stored in __$HOME/.tow/.cache/__. Filename musst be provided if the packaged archive is named idfferently from package name with __.tar.gz__ postfix.

#### Pulling a single package
```{bash}
tow pull-single --version VERSION --base GITLABBASE [ --filename PACKAGEFILENAME] --project PROJECT PACKAGENAME
```

An example:
```{bash}
tow push-single --version 1.2.0 --base http://gitlab.com --project nmaespace/project a_new_package
```

## Pulling from the Towfile

```{bash}
tow push [--towfile FILE]
```

An example:
```{bash}
tow push
```
or 
```{bash}
tow push --towfile Towformatedfile
```

## Towfile

This is a beta Towfile and might be subject to future change.
The Towfile should be located in the directory where __tow__ is executed else it has to be specified. 
Filename can be provided but is not necessary because it is generated automatically.

```{yaml}
gitlab:
  base:  gitlab_baseurl
  packages:
    packagename:
      version: package_version
      project: namespace/project
      filename: somefilename.tar.gz # default is packagename.tar.gz and can be left
      src: path/to/source/folder # all contents of this folder will be packaged and tared
      # the src is only relevant for pushing packages. Packages without a src are not pushed
```

An example:
```{yaml}
gitlab:
  base:  'https://gitlab.com'
  packages:
    packagename:
      version: 0.0.1
      project: namespace/project
      src: path/to/source/folder
    non_pushed_package:
      version: 0.0.2
      project: namepsace/project
```

# TODO

- [ ] clean up repository structure
- [ ] improve usability
- [ ] handle errors better
- [ ] automated tests
- [ ] handle multiple versions of same package cant be specefied (yml)
- [ ] add proper caching strategy options
- [ ] automated tests for functionality
