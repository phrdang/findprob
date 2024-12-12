import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command()
def config():
    print('config called')

@app.command()
def classify():
    print('classify called')

@app.command()
def search():
    print('search called')
