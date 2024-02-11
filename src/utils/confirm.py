import click


def confirm(text: str, default: bool = True, abord: bool = False):
    if click.confirm(text, default):
        return True
    else:
        return exit(0) if abord else False
