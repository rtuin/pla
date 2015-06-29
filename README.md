# Pla

Coder's simplest workflow automation tool.

## Install

Use the pip installer to install Pla.

``` bash
$ pip install pla
```

### Upgrade an existing installation

When installed with Pip you can upgrade to the latest version using:
```shell
$ pip install pla --upgrade
```

### Install from git
To install Pla from git you first need to make sure Pla is uninstalled. Then you must clone the repository and install 
the development version:

```shell
$ pip uninstall pla
$ git clone git@github.com:rtuin/pla.git
$ cd pla
$ pip install -e .
```

## Usage

```shell
$ pla [target]
```

If you do not provide a target, the default target called `all` will run.

## Start working with Pla

Pla works similar to [Make](https://www.gnu.org/software/make/). You define the targets in a Yaml file called `Plafile.yml`
and run the targets from the command line.

Lets say we use Pla to kickstart our working day. We will make a Plafile which starts our local dev server, starts our IDE
 and opens the application we're working on in the browser.
 
First create the Plafile with a target called `dev`:

```yaml
# Plafile.yml
dev:
  - docker-compose up -d
  - pstorm .
  - open http://local.project.url/
```

Then simply run Pla from the command line:
```bash
$ pla dev
```

Pla will then run the shell commands you specified in the Plafile.

## Features

### Linking targets

As of Pla v0.2 it is possible to let your targets call each other. This is simply done by refering to the target 
prepended with an `=` sign. Like so:

```yaml
# Plafile.yml
up:
  - docker-compose up -d
  - =updatecode
  - pstorm .
  - open http://local.project.url/
  
updatecode:
  - git submodule update --init --recursive
  - composer install
```

### Target parameters

Pla v0.3 gives you the ability to variables in target commands. This feature is called target parameters.
 
Simply define the parameters in the target definition, and put them in your command. Enclosing the parameters name with 
`%` signs. For example:

```yaml
# Plafile.yml
pr[number]:
  - git pr %number%
  - git pull upstream master
```

You can then call the target like this:

```bash
$ pla pr 123
```

  **Disclaimer** The current implementation of target parameters is built to work only when you directly call the
  parametrized target.
  
### Command OS filter

When you run the same Pla target on multiple operating systems you might want to specify which command to execute on what OS.
You can do this by prefixing your command with a filter that indicates the OS's family name.
 
```yaml
# Plafile
os:
  - (darwin) echo "Mac OS"
  - (redhat) echo "RedHat family"
  - (ubuntu|darwin) echo "Ubuntu or Mac OS"
  - (debian) echo "Debian"
```

If you run `pla os` on a Mac, you'll get the following output:
```
Running target "os":
    ✔ (darwin) echo "Mac OS"
    . (redhat) echo "RedHat family"
    ✔ (ubuntu|darwin) echo "Ubuntu or Mac OS"
    . (debian) echo "Debian"
```

**Operating systems matches**

| System/Family | Match   |
|---------------|---------|
| Linux         | linux   |
| Ubuntu        | ubuntu  |
| Red Hat       | redhat  |
| Mac OS        | darwin  |
| Windows       | windows |

## Changelog

All notable changes are documented in the [changelog file](CHANGELOG.md).

## Credits

- [Richard Tuin](https://github.com/rtuin)
- [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see the [license file](LICENSE) for more information.
