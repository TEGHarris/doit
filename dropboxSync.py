# This is a library for syncing files with Dropbox:
import dropbox, os, click, hashlib, json
home = os.path.expanduser("~")
dir_path = home + "/.doit/"


def get_auth_token():
    if json.load(open(dir_path + "config/config.json"))["AUTH_TOKEN"] == "None":
        APP_KEY = json.load(open(dir_path + "config/config.json"))["APP_KEY"]
        flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY,use_pkce=True)
        auth_url = flow.start()
        print("1. Go to: " + auth_url)
        print("2. Click 'Allow' (you might need to log in).")
        print("3. Copy the authorization code.")
        auth_code = input("Enter the authorization code here: ").strip()
        oauth_result = flow.finish(auth_code)
        ACCESS_TOKEN = oauth_result.access_token
        user_id = oauth_result.user_id
        with open(dir_path + "config/config.json", "r") as file:
            config = json.load(file)
            config["AUTH_TOKEN"] = ACCESS_TOKEN
        with open(dir_path + "config/config.json", "w") as file:
            json.dump(config, file)
    else:
        ACCESS_TOKEN = json.load(open(dir_path + "config/config.json"))["AUTH_TOKEN"]
        try:
            dbx = dropbox.Dropbox(ACCESS_TOKEN)
            dbx.users_get_current_account()
        except dropbox.exceptions.AuthError:
            config = json.load(open(dir_path + "config/config.json"))
            config["AUTH_TOKEN"] = "None"
            with open(dir_path + "config/config.json", "w") as file:
                json.dump(config, file)
            print("Sorry, your access token is invalid or expired. This is entirely normal. Please reauthenticate.")
            ACCESS_TOKEN = get_auth_token()

    return ACCESS_TOKEN

def whoami():
    ACCESS_TOKEN = get_auth_token()
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    account = dbx.users_get_current_account()
    click.echo(f"Connected to {account.email}")


def upload(path,clear = False,parent_folder=""):
    ACCESS_TOKEN = get_auth_token()
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    if clear:
        try:
            for file in dbx.files_list_folder(parent_folder).entries:
                dbx.files_delete(file.path_lower)
            print("Deleted existing files")
        except dropbox.exceptions.ApiError:
            print("No existing files to delete")
            pass
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isdir(full_path):
            upload(full_path,clear = False ,parent_folder= parent_folder + "/" + file)
        else:
            with open(full_path, "rb") as f:
                data = f.read()
                try:
                    dbx.files_upload(data, parent_folder + "/" + file)
                except dropbox.exceptions.ApiError:
                    dbx.files_upload(data, parent_folder + "/" + file, mode=dropbox.files.WriteMode.overwrite)
                click.echo(f"{file} uploaded successfully")

def download(dir_path, folder_path=""):
    ACCESS_TOKEN = get_auth_token()
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    for entry in dbx.files_list_folder(folder_path).entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            local_folder = os.path.join(dir_path, entry.name)
            os.makedirs(local_folder, exist_ok=True)
            download(local_folder, entry.path_lower)
        elif isinstance(entry, dropbox.files.FileMetadata):
            local_file = os.path.join(dir_path, entry.name)
            dbx.files_download_to_file(local_file, entry.path_lower)
            click.echo(f"{entry.name} downloaded successfully")

def get_local_hash(filepath):
    """Generate a hash for a local file"""
    hasher = hashlib.sha1()
    for file in os.listdir(filepath):
        if os.path.isdir(filepath + file):
            hasher.update((get_local_hash(filepath + file + "/")).encode("utf-8"))
            continue
        else:
            with open(filepath + file, "rb") as f:
                while chunk := f.read(4096):
                    hasher.update(chunk)
    return hasher.hexdigest()


def get_dropbox_hash(path):
    ACCESS_TOKEN = get_auth_token()
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    """Generate a hash for a dropbox file"""
    hasher = hashlib.sha1()
    for entry in dbx.files_list_folder(path).entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            hasher.update(get_dropbox_hash(entry.path_lower).encode("utf-8"))
        elif isinstance(entry, dropbox.files.FileMetadata):
            metadata, response = dbx.files_download(entry.path_lower)
            hasher.update(response.content)
    return hasher.hexdigest()

def syncDropbox(source, dir_path=dir_path):
    if (get_dropbox_hash("") == get_local_hash(dir_path)):
        click.echo("Files are already in sync")
    else:
        if source == "dropbox":
            download(dir_path)
        elif source == "local":
            upload(dir_path)
        elif source == "clear":
            upload(dir_path, clear=True)
        else:
            click.echo("Invalid source")
            return
        click.echo("Sync completed")

