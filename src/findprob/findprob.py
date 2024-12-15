from enum import Enum

import os

from rich.progress import track, Progress, SpinnerColumn, TextColumn

from .text_helpers import get_document_loader_from_url, get_document_loader_from_pdf, chunk_documents, save_vectorstore

import typer

from typing import Optional
from typing_extensions import Annotated


app = typer.Typer(
    help="A CLI to classify and search for problems using LLMs",
    pretty_exceptions_show_locals=False, # prevent sensitive info like API keys from being displayed
)


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
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be a non-negative integer")
    
    if text_type == TextType.pdf:
        if not os.path.exists(source):
            raise ValueError(f"Textbook source directory {source} does not exist")

        if len([file_name for file_name in os.listdir(source) if file_name.endswith('.pdf')]) == 0:
            raise ValueError(f"Textbook source directory {source} is empty or contains no PDFs")
    
    if os.path.exists(out_dir):
        overwrite = typer.confirm(f"{out_dir} already exists. Do you wish to overwrite it?")
        if not overwrite:
            raise typer.Abort()
        print(f'Overwriting contents of {out_dir}')
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        if text_type == TextType.url:
            progress.add_task(description="Chunking textbook from URL...", total=None)
            textbook_loader = get_document_loader_from_url(source)
            chunks = chunk_documents(textbook_loader, chunk_size, chunk_overlap)
        else:
            progress.add_task(description="Chunking textbook from PDFs...", total=None)

            pdfs = [file_name for file_name in os.listdir(source) if file_name.endswith('.pdf')]
            chunks = []

            for file_name in pdfs:
                pdf_doc_loader = get_document_loader_from_pdf(f'{source}/{file_name}')
                chunks_in_pdf = chunk_documents(pdf_doc_loader, chunk_size, chunk_overlap)
                chunks.extend(chunks_in_pdf)

        progress.add_task(description=f"Writing {len(chunks)} to {out_dir} directory...", total=None)
        save_vectorstore(chunks, out_dir)


@app.command()
def classify(
    in_dir: Annotated[str, typer.Argument(help="Problem bank directory")],
    out_file: Annotated[
        str, typer.Argument(help="Path of output CSV file with classified problems") # TODO consider switching to JSON? native arrays supported
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

    # TODO add fewshot mechanism - another command line option?
    # TODO check that all paths exist
    # TODO use model to classify problems and output into csv file with header problem_path, topics


@app.command()
def search(
    classify_file: Annotated[
        str,
        typer.Argument(
            help="CSV file with classified problems (must be in same format as classify command output)" # TODO make this json
        ),
    ],
    out_file: Annotated[
        str,
        typer.Argument(
            help="Name of output text file containing problem paths that match topic" # TODO json file
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
