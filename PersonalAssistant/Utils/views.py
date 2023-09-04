import os
import cloudinary.api
import cloudinary.uploader
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from dotenv import load_dotenv


from .models import UserFiles

load_dotenv()

cloudinary.config(cloud_name=os.environ.get('cloud_name'),
    api_key=os.environ.get('api_key'),
                  api_secret=os.environ.get('api_secret'))

extensions = {'Images': ['jpeg', 'png', 'jpg', 'svg'],
              "Documents": ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
              "Unknown": []}


def exception(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(e)
            return redirect('/base')
    return wrapper


def check_extensions(file):
    extns = file.split('.')[-1]
    for key, value in extensions.items():
        if extns in value:
            return key
    return "Unknown"

@exception
def create_user_folders(user_id=1):
    user_folder_name = f"user_{user_id}"
    cloudinary.api.create_folder(user_folder_name)
    image_folder_name = f"{user_folder_name}/Images"
    cloudinary.api.create_folder(image_folder_name)
    documents_folder_name = f"{user_folder_name}/Documents"
    cloudinary.api.create_folder(documents_folder_name)
    unknown_folder_name = f"{user_folder_name}/Unknown"
    cloudinary.api.create_folder(unknown_folder_name)


@login_required
def upload_files(request):
    if request.method == 'POST':
        current_time = timezone.now().strftime("%Y%m%d%H%M%S")
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(f'Utils/files_to_upload/{current_time}_{uploaded_file.name}', uploaded_file)
        full_path = os.path.join(os.getcwd(), 'files_to_upload')

        for file in os.listdir(full_path):
            file_path = os.path.join(full_path, file)
            result = check_extensions(file)
            try:
                user = User.objects.get(username=request.user)
                folder_path = f'user_{user.id}/{result}'
                upload = cloudinary.uploader.upload(file_path, folder=folder_path)
                public_url = upload['secure_url']
                user_file = UserFiles.objects.get(user_id=user.id)
                res = user_file.Image
                if res is None:
                    res = []
                res.append(public_url)
                user_file.Image = res
                user_file.save()
                os.remove(file_path)
                return redirect('/base')
            except Exception as e:
                print(e)
    return render(request, 'Utils/upload_files.html')


def show_user_images(request):
    pass


def show_user_documents(request):
    pass


def show_user_unknown(request):
    pass


def remove_user_file(request):
    pass


def download_user_file(request):
    pass
