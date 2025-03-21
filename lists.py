# this is a library for adding multiple lists to the doit app

import os, json,click, doit

def viewlists():
    home = os.path.expanduser("~")
    dir_path = home + "/.doit/"
    lists = os.listdir(dir_path)
    for list in lists:
        if list.endswith(".json"):
            click.echo(list.replace(".json",""))

def newlist(name):
    home = os.path.expanduser("~")
    dir_path = home + "/.doit/"
    open(dir_path + name + ".json", "a").close()
    click.echo(f"{name} created successfully")

def switch(name):
    home = os.path.expanduser("~")
    if os.path.exists(home + "/.doit/" + name + ".json"):
        working_list = name + ".json"
        click.echo(f"Switched to {name}")
    else:
        open(home + "/.doit/" + name + ".json", "a").close()
        click.echo(f"{name} created successfully and switched to it")
        working_list = name + ".json"
    return working_list

def deletelist(name):
    home = os.path.expanduser("~")
    dir_path = os.path.join(home, ".doit")
    file_path = os.path.join(dir_path, name + ".json")
    if click.confirm(f"Are you sure you want to delete {name}?"):
        if not os.path.exists(file_path):
            click.echo(f"{name} does not exist")
            filenames = os.listdir(dir_path).strip(".json")
            if doit.fuzzy(name+".json",os.listdir(dir_path)) != False:
                click.echo(f"Did you mean {(doit.fuzzy(name+".json",os.listdir(dir_path))).removesuffix(".json")}?")
            return
        os.remove(file_path)
        click.echo(f"{name} deleted successfully")
        click.echo("Switching to main list")
        config = json.load(open(dir_path + "/config/config.json", "r"))
        config["working_list"] = "main.json"
        with open(dir_path + "/config/config.json", "w") as file:
            json.dump(config, file)
    else:
        click.echo("Operation cancelled")


