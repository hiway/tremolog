import click


@click.command()
@click.option("--host", default="localhost", help="Host to bind to")
@click.option("--port", default=8080, help="Port to bind to")
def main(host, port):
    click.echo(f"Starting server on {host}:{port}")
    raise NotImplementedError("Not implemented yet")


if __name__ == "__main__":
    main()
