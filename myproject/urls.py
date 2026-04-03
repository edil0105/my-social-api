from django.contrib import admin
from django.urls import path
from django.http import JsonResponse # Тексеру үшін уақытша керек

# Тексеру үшін уақытша функция (юзерлер тізімін қайтарады)
def get_users(request):
    data = [
        {"id": 1, "username": "admin", "email": "admin@example.com"},
        {"id": 2, "username": "user1", "email": "user1@example.com"}
    ]
    return JsonResponse(data, safe=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', get_users), # ОСЫ ЖОЛДЫ МІНДЕТТІ ТҮРДЕ ҚОС
]