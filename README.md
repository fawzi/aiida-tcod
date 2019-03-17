[![Build Status](https://travis-ci.org/aiidateam/aiida-tcod.svg?branch=master)](https://travis-ci.org/aiidateam/aiida-tcod) 
[![Coverage Status](https://coveralls.io/repos/github/aiidateam/aiida-tcod/badge.svg?branch=master)](https://coveralls.io/github/aiidateam/aiida-tcod?branch=master) 
[![Docs status](https://readthedocs.org/projects/aiida-tcod/badge)](http://aiida-tcod.readthedocs.io/) 
[![PyPI version](https://badge.fury.io/py/aiida-tcod.svg)](https://badge.fury.io/py/aiida-tcod)

# aiida-tcod

AiiDA plugin to interact with the TCOD

Templated using the [AiiDA plugin cutter](https://github.com/aiidateam/aiida-plugin-cutter).

## Installation

```shell
git clone https://github.com/aiidateam/aiida-tcod .
cd aiida-tcod
pip install -e .  # also installs aiida, if missing (but not postgres)
#pip install -e .[pre-commit,testing] # install extras for more features
verdi quicksetup  # better to set up a new profile
verdi calculation plugins  # should now show your calclulation plugins
```

## Usage

Here goes a complete example of how to submit a test calculation using this plugin.

A quick demo of how to submit a calculation:
```shell
verdi daemon start         # make sure the daemon is running
cd examples
verdi run submit.py        # submit test calculation
verdi calculation list -a  # check status of calculation
```

The plugin also includes verdi commands to inspect its data types:
```shell
verdi data tcod list
verdi data tcod export <PK>
```

## Tests

The following will discover and run all unit tests:
```shell
pip install -e .[testing]
pytest -v
```

## License

MIT


## Contact

developers@aiida.net

