# findprob

## Installation

```sh
pip install findprob
```

## Usage

```sh
findprob config
findprob classify
findprob search
```

## Development

1. Clone the repository: `git clone git@github.com:phrdang/findprob.git`
2. Create virtual environment: `python3 -m venv env`
3. Activate virtual environment: `source env/bin/activate`
4. Install `hatch`: https://hatch.pypa.io/1.9/install/
5. Install pipx:
```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```
6. Install the `findprob` package: `pipx install findprob`
7. Use the CLI as you would normally, e.g. `findprob <command> <options> <arguments>`
8. Very jank way to manually test the CLI at the moment: If you make changes you'll have to `pipx uninstall .` and `pipx install .`
