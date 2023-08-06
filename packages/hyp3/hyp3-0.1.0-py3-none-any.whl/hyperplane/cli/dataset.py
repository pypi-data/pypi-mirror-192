import click


@click.group("dataset", invoke_without_command=True)
@click.pass_context
def dataset(ctx: str) -> None:
    """Dataset used for Hyperplane"""
    print(ctx)
