#Version: 2.0.0
version = "2.0.0"

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
    config = json.load(file)
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


cli.add_command(list)
cli.add_command(add)
cli.add_command(remove)
cli.add_command(removeall)
cli.add_command(viewlists)
cli.add_command(newlist)
cli.add_command(deletelist)
cli.add_command(switch)

if __name__ == '__main__':
    cli()