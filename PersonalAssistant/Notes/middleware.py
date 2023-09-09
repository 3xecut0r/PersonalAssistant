from django.contrib.auth import get_user_model, login


class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Автоматическая авторизация тестового пользователя
        if not request.user.is_authenticated:
            user_model = get_user_model()
            try:
                test_user = user_model.objects.get(username="testuser")
                # Авторизовать пользователя без проверки пароля
                login(request, test_user)
            except user_model.DoesNotExist:
                pass

        response = self.get_response(request)
        return response
