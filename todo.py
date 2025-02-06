import click, os, json
home = os.path.expanduser("~")
try:
    os.makedirs(home + "/.todo")
except FileExistsError:
    pass


dir_path = home + "/.todo/"

working_list = "main.txt"
open(dir_path + working_list, "a").close()

@click.group()
def cli():
    pass


@click.command()
def list():
    file = open(dir_path + working_list, "r")
    for line in file:
        click.echo(line)
    file.close()

@click.command()
@click.argument("task")
def add(task):
    file = open(dir_path + working_list, "a")
    file.write(task + "\n")
    click.echo(f"{task} added successfully")
    file.close()


@click.command()
@click.argument("target")
def remove(target):
    file = open(dir_path + working_list, "r+")
    for line in file:
        if line.strip("\n") == target:
            file.remove(line)
            click.echo(f"{target} removed successfully")
            break

cli.add_command(list)
cli.add_command(add)
cli.add_command(remove)


if __name__ == '__main__':
    cli()