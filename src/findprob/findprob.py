from enum import Enum

import typer

from typing import Optional
from typing_extensions import Annotated


app = typer.Typer(help="A CLI to classify and search for problems using LLMs")


class TextType(str, Enum):
    url = "url"
    pdf = "pdf"


@app.command()
def text(
    source: Annotated[
        str,
        typer.Argument(
            help="The textbook source URL or path to the directory containing PDFs"
        ),
    ],
    text_type: Annotated[
        TextType, typer.Argument(help="The textbook type, must be 'url' or 'pdf'")
    ] = TextType.url,
    out_dir: Annotated[
        str, typer.Argument(help="Directory where the vectorstore will be saved")
    ] = "textbook-vectorstore",
    chunk_size: Annotated[
        int, typer.Option(help="Number of characters in each document chunk")
    ] = 1000,
    chunk_overlap: Annotated[
        int,
        typer.Option(help="Number of characters that overlap across document chunks"),
    ] = 100,
):
    """
    Chunks the textbook of the course to aid in problem classification using Retrieval Augmented Generation (RAG),
    and stores the resulting document chunks in a vectorstore.
    """
    print("text called")

    if chunk_size <= 0:
        print("chunk_size must be a positive integer")

    if chunk_overlap < 0:
        print("chunk_overlap must be a non-negative integer")

    # TODO: if text type is URL, chunk textbook from that URL
    # TODO: elif text type is PDF, chunk textbook from PDFs (check directory exists)
    # TODO: save vectorstore to out_dir


@app.command()
def classify(
    in_dir: Annotated[str, typer.Argument(help="Problem bank directory")],
    out_file: Annotated[
        str, typer.Argument(help="Path of output CSV file with classified problems")
    ] = "classified_problems.csv",
    vectorstore_dir: Annotated[
        Optional[str],
        typer.Option(help="Path to vectorstore directory, if you want to use RAG"),
    ] = None,
    k: Annotated[
        Optional[int],
        typer.Option(help="Number of document chunks to retrieve for each LLM call"),
    ] = None,
    topics_file: Annotated[
        Optional[str],
        typer.Option(help="Text file containing list of topics, each on its own line"),
    ] = None,
):
    """
    Classifies all problems in the problem bank,
    and outputs a CSV file with the headers problem_path, topics.
    """
    print("classify called")

    # TODO check that all paths exist
    # TODO use model to classify problems and output into csv file with header problem_path, topics


@app.command()
def search(
    classify_file: Annotated[
        str,
        typer.Argument(
            help="CSV file with classified problems (must be in same format as classify command output)"
        ),
    ],
    out_file: Annotated[
        str,
        typer.Argument(
            help="Name of output text file containing problem paths that match topic"
        ),
    ],
    topic: Annotated[str, typer.Argument(help="Name of topic you want to search for")],
):
    """
    Searches for all classified problems tagged with the given topic,
    and outputs a text file with all problem file paths that match.
    """
    print("search called")

    # TODO check that all paths exist
