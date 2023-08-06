import webbrowser

import typer

app = typer.Typer()


@app.command()
def blog():
    webbrowser.open_new_tab("https://emilrex.com/")


if __name__ == "__main__":
    app()
