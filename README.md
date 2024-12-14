# findprob

## Installation

1. Install the package: `pip install findprob`
2. (Optional) Install autocompletion: `findprob --install-completion`
3. Create an [OpenAI](https://platform.openai.com/signup) account and generate a new API key.
4. Create a [LangChain](https://smith.langchain.com/) account and generate a new API key and project.
5. Create a `.env` file (in the same directory as your problem bank) according to the [`.env-template`](.env-template), or set environment variables through your terminal directly.
    1. **Make sure you add `.env` to your `.gitignore`! Do not push API keys to GitHub.**

## Usage

Run `findprob --help` for information.

Available commands:

```sh
findprob text
findprob classify
findprob search
```
