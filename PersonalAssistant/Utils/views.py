import os

import dropbox
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from dotenv import load_dotenv

from .models import UploadedUserFiles

load_dotenv()


extensions = {'Images': ['jpeg', 'png', 'jpg', 'svg'],
              "Documents": ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
              "Unknown": []}

access_token = os.environ.get('ACCESS_TOKEN')
dbx = dropbox.Dropbox(access_token)

def create_dropbox_folders(user_id):
    user_1_folder_path = f'/User_{user_id}'
    try:
        dbx.files_create_folder(user_1_folder_path)
        print(f'Створено папку {user_1_folder_path}')
    except dropbox.exceptions.ApiError as e:
        print(f'Помилка при створенні папки {user_1_folder_path}: {e}')


def check_extensions(file):
    extns = file.split('.')[-1]
    for key, value in extensions.items():
        if extns in value:
            return key
    return "Unknown"


@login_required
def upload_files(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(f'Utils/files_to_upload/{uploaded_file}', uploaded_file)
        full_path2 = os.path.join(os.getcwd(), 'Utils')
        full_path3 = os.path.join(full_path2, "files_to_upload")

        for file in os.listdir(full_path3):
            file_path = os.path.join(full_path3, file)
            result = check_extensions(file)
            try:
                user = User.objects.get(username=request.user)
                with open(file_path, 'rb') as f:
                    folder_path = f'user_{user.id}/{result}'
                    dbx_file = dbx.files_upload(f.read(), f'/{folder_path}/{file}')
                public_url = dbx.sharing_create_shared_link(path=dbx_file.path_display)
                user_file = UploadedUserFiles(href=public_url.url, type=file, category=result, user=user)
                user_file.save()
                os.remove(file_path)
                return redirect('/base')
            except Exception as e:
                print(e)
    return render(request, 'Utils/upload.html')

@login_required
def show_user_images(request):
    user_files = UploadedUserFiles.objects.filter(user_id=request.user.id, category='Images')
    href_list = [file.href for file in user_files if file.href]
    context = {'href_list': href_list}
    return render(request, 'Utils/show_images.html', context)


def show_user_documents(request):
    user_files = UploadedUserFiles.objects.filter(user_id=request.user.id, category='Documents')
    href_list = [file.href for file in user_files if file.href]
    context = {'href_list': href_list}
    return render(request, 'Utils/show_documents.html', context)


def show_user_unknown(request):
    user_files = UploadedUserFiles.objects.filter(user_id=request.user.id, category='Unknown')
    href_list = [file.href for file in user_files if file.href]
    context = {'href_list': href_list}
    return render(request, 'Utils/show_else.html', context)


def remove_user_file(request):
    pass


def download_user_file(request):
    pass
