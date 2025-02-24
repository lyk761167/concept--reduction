
def dynamic_add_3(matrix):
    """动态生成新矩阵的特定概念约简, 最终版"""
    intersections = []
    print(matrix)
    for i in range(2, len(matrix) + 1):
        new_row = ''.join(map(str, matrix[i - 1][:i]))
        row_num = i - 1

        print('ttttttttt')
        print(new_row)
        print('kkkkkkkkk')
        print(row_num)
        intersections = dynamic_add_3_helper(intersections, row_num, new_row)
    return intersections
def dynamic_add_3_helper(intersections, row_num, new_row):
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


if __name__ == "__main__":

    # 对称形式背景下的关系矩阵
    matrix = [
        [1, 1, 0, 1, 0, 0],
        [1, 1, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1]
    ]

    ####################### 动态 ##########################

    intersections_3 = []

    for i in range(2, len(matrix) + 1):
        new_row = ''.join(map(str, matrix[i - 1][:i]))
        row_num = i - 1
        intersections_3 = dynamic_add_3(intersections_3, row_num, new_row)

    total_length = 0
    print("概念约简", intersections_3)




