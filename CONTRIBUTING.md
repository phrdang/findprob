# Contributing

## Getting Started

1. Clone the repository: `git clone git@github.com:phrdang/findprob.git`
2. Create virtual environment: `python3 -m venv env`
3. Activate virtual environment: `source env/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
    1. If you install new dependencies, make sure to run `pip freeze > requirements.txt`

## Development

1. Install the `findprob` package: `pipx install .` (you should run this in the root directory of the repo)
2. Use the CLI as you would normally, e.g. `findprob <command> <options> <arguments>`
3. Very jank way to manually test the CLI at the moment: If you make changes you'll have to `pipx uninstall .` and `pipx install .`

## Publishing to PyPI or TestPyPI

Do this once:

1. Create an account
    1. PyPI: https://pypi.org/account/register/
    2. TestPyPI: https://test.pypi.org/account/register/
2. For each website, create an API token and copy it.
3. Create a file `~/.pypirc` and paste your API keys in. **IMPORTANT:** Do not replace `__token__` with your username. It should literally be `__token__` in your file.
```
[pypi]
username = __token__
password = <copy and paste PyPi API key here>

[testpypi]
username = __token__
password = <copy and paste Test PyPi API key here>
```

Do this every time you are publishing a new version of the package:

1. Tag the current `git` commit: `git tag <tag_number>`, such as `git tag 1.0`
2. Push the tag to the remote repository: `git push --tags`
3. Build a new distribution: `hatch build`
4. Publish the distribution:
    1. To PyPI: `hatch publish`
    2. To TestPyPI: `hatch publish -r test`

See also: [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#packaging-your-project)

## Documentation Website

- Generated using [Jekyll](https://jekyllrb.com/)
- Deployed with [GitHub Pages](https://pages.github.com/)

To get started:

1. Follow [Jekyll](https://jekyllrb.com/docs/) installation instructions
2. Go into the documentation folder: `cd docs`
3. Run `bundle install` to install dependencies
4. Run `bundle exec jekyll serve` to run preview of website
