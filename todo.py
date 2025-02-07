#Version: 1.1.0
version = "1.1.0"
import click, os, json
home = os.path.expanduser("~")
try:
    os.makedirs(home + "/.todo")
except FileExistsError:
    pass


dir_path = home + "/.todo/"

working_list = "main.json"
open(dir_path + working_list, "a").close()

@click.group()
@click.version_option(version)
def cli():
    pass

@click.command()

def list():
    file = open(dir_path + working_list, "r")
    tasks = json.load(file)
    for task in tasks:
        click.echo(str(task["name"]))
    file.close()

@click.command()
@click.argument("new")
def add(new):
    with open(dir_path + working_list, "r") as file:
        try:
            tasks = json.load(file)
        except json.decoder.JSONDecodeError:
            tasks = []
    working_task = {"name": new}
    with open(dir_path + working_list, "w") as file:
        tasks.append(working_task)
        json.dump(tasks, file)
    click.echo(f"{new} added successfully")
    file.close()


@click.command()
@click.argument("target")
def remove(target):
    with open(dir_path + working_list, "r") as file:
        try:
            tasks = json.load(file)
        except json.decoder.JSONDecodeError:
            tasks = []

    with open(dir_path + working_list, "w") as file:
        #.strip("\n")
        new_tasks = []
        for task in tasks:
            if task["name"] != target:
                new_tasks.append(task)
        json.dump(new_tasks, file)
        click.echo(f"{target} removed successfully")

cli.add_command(list)
cli.add_command(add)
cli.add_command(remove)


if __name__ == '__main__':
    cli()