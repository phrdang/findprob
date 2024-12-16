from .text_helpers import (
    get_document_loader_from_url,
    get_document_loader_from_pdf,
    chunk_documents,
    save_vectorstore,
)
from .classify_helpers import (
    get_vectorstore_retriever,
    topics_given_classify,
    no_topics_classify,
    feedback_classify,
    save_classifications,
)

from enum import Enum
import os
from rich.progress import Progress, SpinnerColumn, TextColumn
import typer
from typing_extensions import Annotated


app = typer.Typer(
    help="A CLI to classify and search for problems using LLMs",
    pretty_exceptions_show_locals=False,  # prevent sensitive info like API keys from being displayed
)


class TextType(str, Enum):
    url = "url"
    pdf = "pdf"


class ClassifyMode(str, Enum):
    topics_given = "topics-given"
    no_topics = "no-topics"
    feedback = "feedback"


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
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be a non-negative integer")

    if text_type == TextType.pdf:
        if not os.path.exists(source):
            raise ValueError(f"Textbook source directory {source} does not exist")

        if (
            len(
                [
                    file_name
                    for file_name in os.listdir(source)
                    if file_name.endswith(".pdf")
                ]
            )
            == 0
        ):
            raise ValueError(
                f"Textbook source directory {source} is empty or contains no PDFs"
            )

    if os.path.exists(out_dir):
        overwrite = typer.confirm(
            f"{out_dir} already exists. Do you wish to overwrite it?"
        )
        if not overwrite:
            raise typer.Abort()
        print(f"Overwriting contents of {out_dir}")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        if text_type == TextType.url:
            progress.add_task(description="Chunking textbook from URL...", total=None)
            textbook_loader = get_document_loader_from_url(source)
            chunks = chunk_documents(textbook_loader, chunk_size, chunk_overlap)
        else:
            progress.add_task(description="Chunking textbook from PDFs...", total=None)

            pdfs = [
                file_name
                for file_name in os.listdir(source)
                if file_name.endswith(".pdf")
            ]
            chunks = []

            for file_name in pdfs:
                pdf_doc_loader = get_document_loader_from_pdf(f"{source}/{file_name}")
                chunks_in_pdf = chunk_documents(
                    pdf_doc_loader, chunk_size, chunk_overlap
                )
                chunks.extend(chunks_in_pdf)

        progress.add_task(
            description=f"Writing {len(chunks)} to {out_dir} directory...", total=None
        )
        save_vectorstore(chunks, out_dir)


@app.command()
def classify(
    field: Annotated[
        str, typer.Argument(help="The field of study the problems are in")
    ],
    in_dir: Annotated[str, typer.Argument(help="Problem bank directory")],
    out_file: Annotated[
        str, typer.Argument(help="Path of output JSON file with classified problems")
    ],
    mode: Annotated[ClassifyMode, typer.Argument(help="Classification mode")],
    vec_dir: Annotated[
        str,
        typer.Argument(help="Path to vectorstore directory"),
    ],
    topics: Annotated[
        str,
        typer.Option(
            help="Text file with a topic and description in parentheses on each line"
        ),
    ] = None,
    k: Annotated[
        int,
        typer.Option(help="Number of document chunks to retrieve for each LLM call"),
    ] = 1,
):
    """
    Classifies all problems in the problem bank and outputs a JSON file.
    """
    if not os.path.exists(in_dir):
        raise ValueError(f"Problem bank directory {in_dir} does not exist")

    if os.path.exists(out_file):
        overwrite = typer.confirm(
            f"{out_file} already exists. Do you wish to overwrite it?"
        )
        if not overwrite:
            raise typer.Abort()
        print(f"Overwriting contents of {out_file}")

    if not os.path.exists(vec_dir):
        raise ValueError(f"Vectorstore directory {vec_dir} does not exist")

    if mode == ClassifyMode.topics_given or mode == ClassifyMode.feedback:
        if topics is None:
            raise ValueError(
                f"topics option required when using 'topics-given' or 'feedback' mode"
            )

        if not os.path.exists(topics):
            raise ValueError(f"Topics file {topics} does not exist")

    if k <= 0:
        raise ValueError(f"k must be a positive integer")

    retriever = get_vectorstore_retriever(vec_dir, k)

    if mode == ClassifyMode.topics_given:
        classifications = topics_given_classify(in_dir, field, retriever, topics)
    elif mode == ClassifyMode.no_topics:
        classifications = no_topics_classify(in_dir, field, retriever)
    else:
        classifications = feedback_classify(in_dir, field, retriever, topics)

    save_classifications(classifications, out_file)


@app.command()
def search(
    classify_file: Annotated[
        str,
        typer.Argument(
            help="JSON file with classified problems (must be in same format as classify command output)"
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
    # TODO case insensitivity
