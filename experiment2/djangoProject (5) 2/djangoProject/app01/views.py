from django.shortcuts import render
from django.http import JsonResponse
from .euqiconcept_reduction import dynamic_add_3


def matrix_view(request):
    return render(request, 'matrix.html')


def process_matrix(request):
    if request.method == 'POST':
        print(f"Request data: {request.POST}")
        matrix_str = request.POST.get('matrix')
        if matrix_str is None:
            print("Matrix is None")
            return JsonResponse({'error': '处理矩阵时出现错误,请重试。'}, status=500)

        try:
            print(f"Received matrix: {matrix_str}")

            # 修改解析逻辑
            matrix = []
            for row in matrix_str.split(']'):
                if row:
                    # 将每个数字字符串转换为整数列表
                    int_row = [int(digit) for digit in row if digit.isdigit()]
                    # 确保每行有6个元素，不足的用0填充
                    int_row += [0] * (6 - len(int_row))
                    matrix.append(int_row[:6])  # 只取前6个元素，以防超过6个

            print(f"Parsed matrix: {matrix}")

            result = dynamic_add_3(matrix)
            print(f"Result: {result}")

            # 将 set 集合转换为列表
            result_list = [list(row) for row in result]

            return JsonResponse({'result': result_list})
        except Exception as e:
            print(f"Error processing matrix: {e}")
            return JsonResponse({'error': '处理矩阵时出现错误,请重试。'}, status=500)
    return JsonResponse({'error': '无效的请求方法。'}, status=405)

from .models import AccuracySubmission
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

@csrf_exempt
def save_accuracy(request):
    if request.method == 'POST':
        try:
            accuracy_str = request.POST.get('accuracy', '0.00')
            accuracy = Decimal(accuracy_str)  # 转换为 Decimal 对象

            new_submission = AccuracySubmission(accuracy=accuracy)
            new_submission.full_clean()  # 进行完整性检查
            new_submission.save()
            return JsonResponse({"message": "准确率已保存！"})
        except (ValueError, ValidationError, IntegrityError) as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "无效的请求。"}, status=400)