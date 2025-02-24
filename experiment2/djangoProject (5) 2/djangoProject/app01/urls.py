from django.urls import path
from .views import matrix_view, process_matrix
from app01 import views
from app01.views import save_accuracy  # 导入 save_accuracy 视图函数

urlpatterns = [
    path('', views.matrix_view, name='matrix_view'),  # 主页
    path('process_matrix/', views.process_matrix, name='process_matrix'),  # 处理矩阵的 URL
    path('save_accuracy/', save_accuracy, name='save_accuracy'),

]