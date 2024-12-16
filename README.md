# findprob

A CLI to classify and search for problems using LLMs

## Installation

1. Install the package: `pip install findprob`
2. (Optional) Install autocompletion: `findprob --install-completion`
3. Create an [OpenAI](https://platform.openai.com/signup) account and generate a new API key.
4. Create a [LangChain](https://smith.langchain.com/) account and generate a new API key and project.
5. Export the environment variables in your terminal:
```sh
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=<YOUR API KEY HERE>
LANGCHAIN_PROJECT=<YOUR PROJECT NAME HERE>

OPENAI_API_KEY=<YOUR API KEY HERE>
```

## Usage

See the [official docs](https://phrdang.github.io/findprob/) or run `findprob --help` for more information.

## Credits

A research project for CS 194-271 at UC Berkeley (Fall 2024) created by:

- Rebecca Dang (rdang [at] berkeley [dot] edu)
- Jessica Lin (linjessica [at] berkeley [dot] edu)
- Samantha Huang (samanthahuang [at] berkeley [dot] edu)

Advised by:

- Professor Gireeja Ranade (ranade [at] eecs [dot] berkeley [dot] edu)
- Professor Narges Norouzi (norouzi [at] berkeley [dot] edu)
