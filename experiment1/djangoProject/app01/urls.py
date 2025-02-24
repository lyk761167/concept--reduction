
from django.urls import path
from . import views  # 导入 views
from django.urls import path
from app01 import views
from .views import save_accuracy
urlpatterns = [
    path('', views.matrix_view, name='matrix_view'),  # 主页
    path('process_matrix/', views.process_matrix, name='process_matrix'),  # 处理矩阵的 URL
    path('save_accuracy/', save_accuracy, name='save_accuracy'),
]