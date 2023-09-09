import os
import json
import dropbox
import cloudinary.uploader
from cloudinary import api
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from dotenv import load_dotenv

from .models import UploadedUserFiles


from dropbox.exceptions import AuthError
import requests
from django.http import JsonResponse, FileResponse, HttpResponse


import datetime

load_dotenv()

DROPBOX_APP_KEY = os.environ.get("DROPBOX_APP_KEY")
DROPBOX_APP_SECRET = os.environ.get("DROPBOX_APP_SECRET")
REDIRECT_URL = 'http://127.0.0.1:8000/utils/'

cloudinary.config(
  cloud_name = "dsjusqa4p",
  api_key = "599877185773136",
  api_secret = "VFeBRMltUi1d8Jz_aCwOGLF4b8k"
)

extensions = {'Images': ['jpeg', 'png', 'jpg', 'svg'],
              "Documents": ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
              "Unknown": []}

access_token = os.environ.get('ACCESS_TOKEN')

def get_current_datetime_string():
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")


def check_time_difference(datetime_str, path):
    current_datetime = datetime.datetime.now()
    provided_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    time_difference = current_datetime - provided_datetime
    if time_difference.total_seconds() > 60:
        os.remove(path)
        return "clear"
    return None


def check_extensions(file):
    extns = file.split('.')[-1]
    for key, value in extensions.items():
        if extns in value:
            return key
    return "Unknown"


def create_dropbox_folders(request, user_id):
    dbx = get_access_dbx(request)
    user_1_folder_path = f'/User_{user_id}'
    try:
        dbx.files_create_folder(user_1_folder_path)
        response = cloudinary.api.create_folder(f'User_{user_id}')
        print(f'Створено папку {user_1_folder_path}')
    except dropbox.exceptions.ApiError as e:
        print(f'Помилка при створенні папки {user_1_folder_path}: {e}')


@login_required
def upload_files(request):
    dbx = get_access_dbx(request)
    if request.method == 'POST':
        uploaded_file = request.FILES['file']

        if uploaded_file.size > 128 * 1024 * 1024:
            return HttpResponse("Файл більше 128 МБ. Завантаження не дозволено.")

        fs = FileSystemStorage()
        filename = fs.save(f'Utils/files_to_upload/{uploaded_file}', uploaded_file)
        full_path2 = os.path.join(os.getcwd(), 'Utils')
        full_path3 = os.path.join(full_path2, "files_to_upload")

        for file in os.listdir(full_path3):
            file_path = os.path.join(full_path3, file)
            result = check_extensions(file)
            print(result)
            try:
                user = User.objects.get(username=request.user)
                if result == 'Images':
                    folder_path = 'user_10/Images'
                    path = os.path.join(os.getcwd(), "Utils")
                    path = os.path.join(path, "files_to_upload")
                    upload = cloudinary.uploader.upload(os.path.join(path, file), folder=folder_path)
                    file_url = upload["secure_url"]
                    file_id = upload["public_id"]
                    user_file = UploadedUserFiles(href=file_url, type=file, category=result,file_id=file_id, user=user)
                    user_file.save()
                    return redirect('/base')
                with open(file_path, 'rb') as f:
                    folder_path = f'user_{user.id}/{result}'
                    dbx_file = dbx.files_upload(f.read(), f'/{folder_path}/{file}')
                public_url = dbx.sharing_create_shared_link_with_settings(path=dbx_file.path_display)
                user_file = UploadedUserFiles(href=public_url.url, type=file, category=result, user=user)
                user_file.save()
                os.remove(file_path)
                return redirect('/base')
            except Exception as e:
                print(e)
    return render(request, 'Utils/upload_files.html')


@login_required
def show_user_images(request):
    user_files = UploadedUserFiles.objects.filter(user_id=request.user.id, category='Images')
    href_list = [file.href for file in user_files if file.href]
    context = {'href_list': href_list}
    return render(request, 'Utils/show_images.html', context)


@login_required
def show_user_documents(request):
    user_documents = UploadedUserFiles.objects.filter(user_id=request.user.id, category='Documents')
    context = {'user_documents': user_documents}
    return render(request, 'Utils/show_documents.html', context)


@login_required
def show_user_unknown(request):
    user_files = UploadedUserFiles.objects.filter(user_id=request.user.id, category='Unknown')
    href_list = [file.href for file in user_files if file.href]
    context = {'href_list': href_list}
    return render(request, 'Utils/show_else.html', context)

@login_required
def remove_user_file(request, file_id):
        dbx = get_access_dbx(request)
        file = UploadedUserFiles.objects.get(id=file_id)
        if file.file_id:
            cloudinary.api.delete_resources([file_id])
            return HttpResponse('Done')
        dbx.files_delete_v2(f'/User_{file.user_id}/{file.category}/{file.type}')
        file.delete()
        return HttpResponse('Done')




@login_required
def download_user_file(request, file_id):

    dbx = get_access_dbx(request)
    file = UploadedUserFiles.objects.get(id=file_id)
    dropbox_file_path = (f'/User_{file.user_id}/{file.category}/{file.type}')
    path = os.path.join(os.getcwd(), 'Utils')
    local_file_path = os.path.join(path, "downloaded")
    # for file in local_file_path:
    #     dayt = file.split('//')[0]
    #     check_time_difference(dayt, f'{local_file_path}/{file}')
    if not os.path.exists(local_file_path):
        os.makedirs(local_file_path)
        print('Folder not exist')
    metadata, res = dbx.files_download(dropbox_file_path)
    name = f'{get_current_datetime_string()}//{metadata.name}'

    with open(f'{local_file_path}/{metadata.name}', 'wb') as f:
        f.write(res.content)

    file_path = f'{local_file_path}/{metadata.name}'
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{metadata.name}"'
    return response



def dropbox_oauth(request):
    print('!!!!!!Auth Started !!!!!!!!!!!')
    return redirect(f'https://www.dropbox.com/oauth2/authorize?client_id={DROPBOX_APP_KEY}&redirect_uri={REDIRECT_URL}authorized&response_type=code')

def get_access_token():
    with open('OAuth_token.json', 'r') as file:
        data = json.load(file)
        date = data.get('datetime')
        date_dt_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        curent_time = datetime.datetime.now()
        delta = ((curent_time - date_dt_obj).total_seconds()) / 60 / 60
        print(delta)
        if delta > 3:
            return None
        token = data.get('token')
        print(date, token)
        return token


def get_access_dbx(request):
    dbx = None
    try:
        access_token = get_access_token()
        if access_token:
            dbx = dropbox.Dropbox(access_token)
        else:
            print("Try refresh!!!!!!!!!!!!")
            return redirect(to="utils:dropbox_oauth")
    except Exception as err:
        print(f"My ERROR !!!!! ::: {err}")

    return dbx

def dropbox_authorized(request):
    try:
        code = request.GET["code"]
        print(f"Code: {code}")
    except KeyError:
        return JsonResponse({"error": "Authorization code not found in the request."}, status=400)
    data = requests.post('https://api.dropboxapi.com/oauth2/token', {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": f"{REDIRECT_URL}authorized",
    }, auth=(DROPBOX_APP_KEY, DROPBOX_APP_SECRET))
    request.session["DROPBOX_ACCESS_TOKEN"] = data.json()["access_token"]
    with open('OAuth_token.json', 'w') as file:
        json.dump({"datetime":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "token": data.json()["access_token"]}, file, indent=4, ensure_ascii=False)

    return redirect(to="/base")
