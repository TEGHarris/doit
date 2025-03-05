# this is a library for adding multiple lists to the todo app

import os, json,click,todo

def viewlists():
    home = os.path.expanduser("~")
    dir_path = home + "/.todo/"
    lists = os.listdir(dir_path)
    for list in lists:
        if list.endswith(".json"):
            click.echo(list.replace(".json",""))

def newlist(name):
    home = os.path.expanduser("~")
    dir_path = home + "/.todo/"
    open(dir_path + name + ".json", "a").close()
    click.echo(f"{name} created successfully")

def switch(name):
    home = os.path.expanduser("~")
    if os.path.exists(home + "/.todo/" + name + ".json"):
        working_list = name + ".json"
        click.echo(f"Switched to {name}")
    else:
        open(home + "/.todo/" + name + ".json", "a").close()
        click.echo(f"{name} created successfully and switched to it")
        working_list = name + ".json"
    return working_list

def deletelist(name):
    home = os.path.expanduser("~")
    dir_path = os.path.join(home, ".todo")
    file_path = os.path.join(dir_path, name + ".json")
    if click.confirm(f"Are you sure you want to delete {name}?"):
        os.remove(file_path)
        click.echo(f"{name} deleted successfully")
        click.echo("Switching to main list")
        config = json.load(open(dir_path + "/config/config.json", "r"))
        config["working_list"] = "main.json"
        with open(dir_path + "/config/config.json", "w") as file:
            json.dump(config, file)
    else:
        click.echo("Operation cancelled")


