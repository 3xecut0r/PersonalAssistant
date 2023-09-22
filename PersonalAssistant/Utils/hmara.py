import os
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive


g_auth = GoogleAuth()
# g_auth.LocalWebserverAuth()
g_auth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
'service_account_key.json', ['https://www.googleapis.com/auth/drive'])

g_auth.Authorize()

drive = GoogleDrive(g_auth)

extensions = {'Images': ['jpeg', 'png', 'jpg', 'svg'],
              "Documents": ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
              "Unknown extensions": []}


def exception(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception:
            print("Erorr")
    return wrapper


def check_extensions(file):
    extns = file.split('.')[-1]
    for key, value in extensions.items():
        if extns in value:
            return key
    return "Unknown extensions"


def create_folders_for_user(id = 3):
        user_folder = drive.CreateFile({'title': f'User_{id} Folder',
                                        'mimeType': 'application/vnd.google-apps.folder'})
        user_folder.Upload()
        user_folder_id = user_folder['id']
        image_folder = drive.CreateFile(
            {'title': 'Images', 'mimeType': 'application/vnd.google-apps.folder',
             'parents': [{'id': user_folder_id}]})
        image_folder.Upload()
        image_folder_id = image_folder['id']
        document_folder = drive.CreateFile(
            {'title': 'Documents', 'mimeType': 'application/vnd.google-apps.folder',
             'parents': [{'id': user_folder_id}]})
        document_folder.Upload()
        document_folder_id = document_folder['id']
        unknown_folder = drive.CreateFile(
            {'title': 'Unknown extensions', 'mimeType': 'application/vnd.google-apps.folder',
             'parents': [{'id': user_folder_id}]})
        unknown_folder.Upload()
        unknown_folder_id = unknown_folder['id']
        return {'Images': image_folder_id, 'Documents': document_folder_id,"Unknown extensions": unknown_folder_id}

@exception
def upload_file(folders: dict):
    full_path = os.path.join(os.getcwd(), '../Utils/files_to_upload')
    for file in os.listdir(full_path):
        result = check_extensions(file)
        try:
            res = drive.CreateFile({'title': f"{file}"})
            res['parents'] = [{'id': folders.get(result)}]
            res.SetContentFile(os.path.join(full_path, file))
            res.Upload()
        except Exception as e:
            print(e)





@exception
def get_files_links_in_folder(id_list: dict):
    file_links = []
    folders_list_id = [id for id in id_list.values()]
    for folder_id in folders_list_id:
        drive.CreateFile({'id': folder_id})
        file_list = drive.ListFile({'q': f"'{folder_id}' in parents"}).GetList()
        for file in file_list:
            file_links.append({
                'title': file['title'],
                'link': file['alternateLink']
            })

    return file_links


@exception
def remove_user_file(file_link):
    file_id = file_link.split('/')[-2]
    file = drive.CreateFile({'id': file_id})
    file.Delete()


if __name__ == '__main__':
    result = create_folders_for_user()
    print(result)
    upload_file(result)
    print(get_files_links_in_folder(result))
    # обработчик обьема пишем уже непосредственно в джанго


