# this is a library for adding multiple lists to the todo app

import os, json,click

def viewlists():
    home = os.path.expanduser("~")
    dir_path = home + "/.todo/"
    lists = os.listdir(dir_path)
    for list in lists:
        click.echo(list)

def newlist(name):
    home = os.path.expanduser("~")
    dir_path = home + "/.todo/"
    open(dir_path + name + ".json", "a").close()
    click.echo(f"{name} created successfully")