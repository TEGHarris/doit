import dropbox, os, click, hashlib
APP_KEY = 'SECRET'
APP_SECRET = 'SECRET'
flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
auth_url = flow.start()
print("1. Go to: " + auth_url)
print("2. Click 'Allow' (you might need to log in).")
print("3. Copy the authorization code.")
auth_code = input("Enter the authorization code here: ").strip()
oauth_result = flow.finish(auth_code)
ACCESS_TOKEN = oauth_result.access_token
user_id = oauth_result.user_id
dbx = dropbox.Dropbox(ACCESS_TOKEN)
print("Linked account: ", dbx.users_get_current_account().email)

home = os.path.expanduser("~")
dir_path = home + "/.todo/"

def upload(path, parent_folder=""):
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isdir(full_path):
            upload(full_path, parent_folder + "/" + file)
        else:
            with open(full_path, "rb") as f:
                data = f.read()
                dbx.files_upload(data, parent_folder + "/" + file)
                click.echo(f"{file} uploaded successfully")

def download(dir_path, folder_path=""):
    # List folder contents
    for entry in dbx.files_list_folder(folder_path).entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            # Create local folder
            local_folder = os.path.join(dir_path, entry.name)
            os.makedirs(local_folder, exist_ok=True)
            # Recursively download subfolder
            download(local_folder, entry.path_lower)
        elif isinstance(entry, dropbox.files.FileMetadata):
            # Download file
            local_file = os.path.join(dir_path, entry.name)
            dbx.files_download_to_file(local_file, entry.path_lower)
            print(f"{entry.name} downloaded successfully")

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
    """Generate a hash for a dropbox file"""
    hasher = hashlib.sha1()
    for entry in dbx.files_list_folder(path).entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            hasher.update(get_dropbox_hash(entry.path_lower).encode("utf-8"))
        elif isinstance(entry, dropbox.files.FileMetadata):
            metadata, response = dbx.files_download(entry.path_lower)
            hasher.update(response.content)
    return hasher.hexdigest()


print(f"local hash: {get_local_hash(dir_path)}")
print(f"dropbox hash: {get_dropbox_hash('')}")