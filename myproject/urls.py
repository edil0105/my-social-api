from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

# Тексеру үшін қарапайым функция
def get_users(request):
    return JsonResponse([
        {"id": 1, "username": "edil", "email": "edil@example.com"}
    ], safe=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', get_users),  # ОСЫ ЖОЛ МІНДЕТТІ ТҮРДЕ КЕРЕК
]