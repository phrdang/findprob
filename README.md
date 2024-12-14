# findprob

A CLI to classify and search for problems using LLMs

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

## Credits

A research project created by Rebecca Dang (rdang [at] berkeley [dot] edu), Jessica Lin (linjessica [at] berkeley [dot] edu), and Samantha Huang (samanthahuang [at] berkeley [dot] edu) and advised by Professor Gireeja Ranade (ranade [at] eecs [dot] berkeley [dot] edu) and Professor Narges Norouzi (norouzi [at] berkeley [dot] edu) for CS 194-271 at UC Berkeley (Fall 2024).
