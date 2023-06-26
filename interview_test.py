# coding:utf-8
# @Time : 2022/11/22 20:05 
# @Author : Andy.Zhang
# @Desc : 我这边是用 python3.9 编译的哈，建议 python 3x 运行 (由于时间关系，我就不再用 py2 测试了)

'''
题目一：公司有n个组，每组人数相同，>=1人，需要进行随机的组队吃饭。
要求：1. 两两一队，不能落单，落单则三人一队
  2. 一个人只出现一次
  3. 队伍中至少包含两个组
  4. 随机组队，重复执行程序得到的结果不一样
举例：
GroupList = [  # 小组列表
    ['小名', '小红', '小马', '小丽', '小强'],
    ['大壮', '大力', '大1', '大2', '大3'],
    ['阿花', '阿朵', '阿蓝', '阿紫', '阿红'],
    ['A', 'B', 'C', 'D', 'E'],
    ['一', '二', '三', '四', '五'],
    ['建国', '建军', '建民', '建超', '建跃'],
    ['爱民', '爱军', '爱国', '爱辉', '爱月']
]

输入：GroupList
输出：(A, 小名)，（B, 小红）。。。
'''


from random import randint


def rand_group(group_list):
    result = []

    group_length = len(group_list)

    if not group_length:
        return result
    elif group_length == 1:
        return group_list

    full_arry_index = []

    group_a_index = randint(0, group_length-1)
    group_b_index = randint(0, group_length-1)
    while group_b_index == group_a_index:
        # print('found the same rand group number #%s, need to generate a different group' % group_b_index)
        group_b_index = randint(0, group_length-1)

    group_a = group_list[group_a_index]
    group_a_sub_index = 0 if len(group_a) == 1 else randint(0, len(group_a)-1)
    group_a_val = group_a.pop(group_a_sub_index)

    group_b = group_list[group_b_index]
    group_b_sub_index = 0 if len(group_b) == 1 else randint(0, len(group_b)-1)
    group_b_val = group_b.pop(group_b_sub_index)

    if not group_a:
        group_list.pop(group_a_index)
    if not group_b:
        group_list.pop(group_b_index)

    if group_list:
        if len(group_list) == 1 and len(group_list[0])==1:
            print((group_a_val, group_b_val, group_list[0][0]))

        else:
            print((group_a_val, group_b_val))
            rand_group(group_list)
    else:
        print((group_a_val, group_b_val))


if __name__ == '__main__':
    test_group_list = [  # 小组列表
        ['小名', '小红', '小马', '小丽', '小强'],
        ['大壮', '大力', '大1', '大2', '大3'],
        ['阿花', '阿朵', '阿蓝', '阿紫', '阿红'],
        ['A', 'B', 'C', 'D', 'E'],
        ['一', '二', '三', '四', '五'],
        ['建国', '建军', '建民', '建超', '建跃'],
        ['爱民', '爱军', '爱国', '爱辉', '爱月']
    ]

    print('\n========= begain to show the result =========')
    rand_group(test_group_list)
    print('========= end to show the result =========')