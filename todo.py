import click
import os

home = os.path.expanduser("~")
try:
    os.makedirs(home + "/.todo")
except FileExistsError:
    pass

main_file = open(home + "/.todo/main.txt", "a")


@click.group()
def cli():
    pass


@click.command()
def list():
    # click.echo("This is a list command")
    main_file = open(home + "/.todo/main.txt", "r")
    for line in main_file:
        click.echo(line)

@click.command()
@click.argument("task")
def add(task):
    # click.echo("This is an add command")
    main_file = open(home + "/.todo/main.txt", "a")
    main_file.write(task + "\n")
    click.echo(f"{task} added successfully")


cli.add_command(list)
cli.add_command(add)

if __name__ == '__main__':
    cli()