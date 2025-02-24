"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app01 import views
from django.contrib import admin
from django.urls import path, include

from django.contrib import admin
from django.urls import path
from app01 import views  # 使用绝对导入
from app01.views import save_accuracy  # 导入 save_accuracy 视图函数
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.matrix_view, name='matrix_view'),
    path('process_matrix/', views.process_matrix, name='process_matrix'),
    path('save_accuracy/', save_accuracy, name='save_accuracy'),
]
# urls.py


