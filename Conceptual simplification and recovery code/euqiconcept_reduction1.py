import numpy as np
def dynamic_add_3(intersections, row_num, new_row):
    """动态生成新矩阵的特定概念约简, 最终版"""

    A1 = []
    A2 = []
    A_1 = []
    new_set = {index + 1 for index, value in enumerate(new_row) if value == '1'}
    # print(new_set)
    alr_set = set()
    for t_set in intersections:
        common_set = t_set & new_set
        if common_set:
            set1 = set(common_set)
            set1.add(row_num + 1)
            if common_set == t_set:
                A1.append(set1)
            else:
                A2.append(t_set)
                if set1 not in A_1:
                    A_1.append(set1)
            for i in common_set:
                alr_set.add(i)
        else:
            A2.append(t_set)
    alr_set.add(row_num + 1)
    surplus_set = new_set - alr_set
    intersections_dict = {}
    for i in range(1, row_num + 2):  # 假设最多有5个元素的交集
        intersections_dict[i] = []
    sum = A1 + A_1
    for t in sum:
        intersections_dict[len(t)].append(t)
    A3 = []
    for i in range(1, row_num + 2):  # 1到新行数,都要遍历，因为加的是s2
        for s1 in intersections_dict[i]:
            is_true_subset = False
            if s1 in A1:
                continue
            for j in range(i + 1, row_num + 2):
                for s2 in intersections_dict[j]:
                    if s1.issubset(s2):
                        is_true_subset = True
                        break
                if is_true_subset:
                    break
            if not is_true_subset:
                A3.append(s1)

    for i in surplus_set:
        A3.append({i, row_num + 1})
    SC_n_1 = A2 + A3 + A1

    return SC_n_1


def restore_matrix_from_intersections(intersections, n):
    """
    从概念约简集合还原对称矩阵

    参数:
    - intersections: 概念约简的集合
    - n: 矩阵的大小

    返回:
    - numpy矩阵
    """
    # 初始化矩阵为0
    matrix = np.zeros((n, n), dtype=int)

    # 遍历每个集合
    for subset in intersections:
        # 找出集合中的元素
        elements = list(subset)

        # 如果集合大小大于1（排除单元素集合）
        if len(elements) > 1:
            # 将这些元素对应的位置设置为1
            for i in range(len(elements)):
                for j in range(i + 1, len(elements)):
                    # 注意元素编号从1开始，需要减1转换为矩阵索引
                    row = elements[i] - 1
                    col = elements[j] - 1
                    matrix[row, col] = 1
                    matrix[col, row] = 1
    np.fill_diagonal(matrix, 1)
    return matrix


# 使用示例
if __name__ == "__main__":
    upper_triangle = np.random.randint(2, size=(15, 15))

    # 创建对称矩阵，并确保只有0和1
    symmetric_matrix = np.maximum(upper_triangle, upper_triangle.T)

    # 保持对角线为0
    np.fill_diagonal(symmetric_matrix, 1)

    # 打印矩阵形状以确认
    print(symmetric_matrix)
    # 对称形式背景下的关系矩阵
    matrix = symmetric_matrix

    ####################### 动态 ##########################

    intersections_3 = []

    for i in range(2, len(matrix) + 1):
        new_row = ''.join(map(str, matrix[i - 1][:i]))
        row_num = i - 1
        intersections_3 = dynamic_add_3(intersections_3, row_num, new_row)

    total_length = 0
    print("概念约简", intersections_3)
    # 假设 intersections_3 是你之前生成的概念约简集合
    restored_matrix = restore_matrix_from_intersections(intersections_3, 15)
    print(restored_matrix)
    # 验证还原的矩阵是否与原矩阵相同
    print("是否完全相同:", np.array_equal(matrix, restored_matrix))

    # 可选：打印差异
    diff = np.sum(np.abs(matrix - restored_matrix))
    print("矩阵差异总数:", diff)



    # 生成上三角的随机0和1矩阵


    # 生成上三角的随机0和1矩阵





