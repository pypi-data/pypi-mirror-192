# findersel

Get selected files from [macOS Finder](https://support.apple.com/HT201732) and use them programatically within your Python program.

## Installation

```console
$ pip install findersel
```

## Usage

Select some files on Finder:

![Finder screenshot](https://github.com/sdelquin/findersel/raw/main/finder-screenshot.png)

And get the selected files:

```python
>>> import findersel

>>> list(findersel.get_selected_files())
['/Users/sdelquin/findersel/LICENSE',
 '/Users/sdelquin/findersel/Makefile',
 '/Users/sdelquin/findersel/README.md',
 '/Users/sdelquin/findersel/requirements.txt',
 '/Users/sdelquin/findersel/setup.cfg',
 '/Users/sdelquin/findersel/setup.py']
```

> Note than the function returns a **generator**.

You can get the selected files _ordered by name_ with:

```python
>>> import findersel

>>> list(findersel.get_selected_files(sort=True))
['/Users/sdelquin/findersel/Makefile',
 '/Users/sdelquin/findersel/README.md',
 '/Users/sdelquin/findersel/requirements.txt',
 '/Users/sdelquin/findersel/setup.cfg',
 '/Users/sdelquin/findersel/setup.py',
 '/Users/sdelquin/findersel/LICENSE']
```

## Changelog

| 0.1.4 | 15/02/2023 |
| ----- | ---------- |

- Fix documentation.

| 0.1.3 | 15/02/2023 |
| ----- | ---------- |

- Add parameter to sort files.

| 0.1.2 | 20/06/2021 |
| ----- | ---------- |

- Get rid of prettyconf external dependency.

| 0.1.1 | 20/06/2021 |
| ----- | ---------- |

- Add documentation.
- Fix bug when no files are selected.

| 0.1.0 | 20/06/2021 |
| ----- | ---------- |

- Add initial code.

## License

MIT
