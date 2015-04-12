# Pla

Make, but with a yaml file

## Install

Use the pip installer to install Pla

``` bash
$ pip install pla
```

## Usage

```bash
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

Then simply run pla from the command line:
```bash
$ pla dev
```

Pla will then run the shell commands you specified in the Plafile.

## Credits

- [Richard Tuin](https://github.com/rtuin)
- [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see the [license file](LICENSE) for more information.
