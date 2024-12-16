# findprob

1. Table of Contents
{:toc}

A CLI to classify and search for problems using LLMs

## Installation

See the [README](https://github.com/phrdang/findprob/blob/main/README.md#installation).

## Commands

### text

Chunks the textbook of the course to aid in problem classification using Retrieval Augmented Generation (RAG), and stores the resulting document chunks in a vectorstore.

This command supports ingesting the textbook via a URL or as a directory containing at PDF(s) of the textbook.

After creating chunks of the textbook, the command creates a [FAISS](https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/) vectorstore using [OpenAI's ada-002 embeddings](https://platform.openai.com/docs/guides/embeddings) through the [LangChain](https://python.langchain.com/docs/integrations/vectorstores/faiss/) API.

Run `findprob text --help` for information on arguments and options.

### classify

Classifies all problems in the problem bank and outputs a JSON file.

This command utilizes [OpenAI's gpt-4o-mini model](https://platform.openai.com/docs/models#gpt-4o-mini) with `temperature=0` and `max_tokens=256`. It loads in the FAISS vectorstore and performs a similarity search to retrieve the top `k` related chunks, using [LangChain's RAG APIs](https://python.langchain.com/docs/tutorials/rag/).

This command supports 3 classification modes:

1. `topics-given`: The user provides a list of topics and optional descriptions in a text file, and the LLM is instructed to only classify problems with topics from the list, or use "other" if none of the topics apply.
2. `no-topics`: The LLM comes up with its own topics to label the problems.
3. `feedback`: A combination of the first two modes. The user provides a starting topic list but the LLM is also free to add more topics to the list. Whenever a topic is added, the LLM will go back and reclassify all previous problems with the new list of topics.

The precise prompts for each mode can be found in the [source code](https://github.com/phrdang/findprob/blob/main/src/findprob/classify_helpers.py#L14-L85).

Run `findprob classify --help` for information on arguments and options.

### search

Searches for all classified problems tagged with the given topic, and outputs a text file with all problem file paths that match.

Run `findprob search --help` for information on arguments and options.

## Credits

See the [README](https://github.com/phrdang/findprob/blob/main/README.md#credits).
