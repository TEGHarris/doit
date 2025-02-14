#Version: 2.0.1
version = "2.0.1"
import click, os, json, lists
home = os.path.expanduser("~")
try:
    os.makedirs(home + "/.todo")
except FileExistsError:
    pass

try:
    os.makedirs(home + "/.todo/config")
except FileExistsError:
    pass

open(home + "/.todo/config/config.json", "a").close()


dir_path = home + "/.todo/"
with open(dir_path + "config/config.json", "r") as file:
    try:
        config = json.load(file)
    except json.decoder.JSONDecodeError:
        config = {"working_list": "main.json"}
        with open(dir_path + "config/config.json", "w") as file:
            json.dump(config, file)
working_list = config["working_list"]
open(dir_path + working_list, "a").close()

@click.group()
@click.version_option(version)
def cli():
    pass

@click.command()
def list():
    try:
        file = open(dir_path + working_list, "r")
        tasks = json.load(file)
    except json.decoder.JSONDecodeError:
        click.echo("No tasks in the list")
        return
    click.echo(f"Tasks in {working_list[:-5]}:")
    for task in tasks:
        click.echo(f"[ ] -- {str(task["name"])}")
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
    if not click.confirm(f"Are you sure you want to remove {target}?"):
        click.echo("Operation cancelled")
        return
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

@click.command()
def removeall():
    with open(dir_path + working_list, "w") as file:
        file.write("[]")
        click.echo("All tasks removed successfully")

# Commands from lists.py

@click.command()
def viewlists():
    lists.viewlists()

@click.command()
@click.argument("new_list")
def newlist(new_list):
    lists.newlist(new_list)

@click.command()
@click.argument("list_name")
def deletelist(list_name):
    lists.deletelist(list_name)

@click.command()
@click.argument("list_name")
def switch(list_name):
    new_working = lists.switch(list_name)
    config = json.load(open(dir_path + "config/config.json", "r"))
    config["working_list"] = new_working
    with open(dir_path + "config/config.json", "w") as file:
        json.dump(config, file)

@click.command()
def where():
    global working_list
    click.echo(working_list)

cli.add_command(list)
cli.add_command(add)
cli.add_command(remove)
cli.add_command(removeall)
cli.add_command(viewlists)
cli.add_command(newlist)
cli.add_command(deletelist)
cli.add_command(switch)
cli.add_command(where)

if __name__ == '__main__':
    cli()