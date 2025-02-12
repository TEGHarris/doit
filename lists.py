# this is a library for adding multiple lists to the todo app

import os, json,click

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

def deletelist(name):
    home = os.path.expanduser("~")
    dir_path = home + "/.todo/"
    os.remove(dir_path + name + ".json")
    click.echo(f"{name} deleted successfully")

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

