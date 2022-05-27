import time

info = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabcaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


# info = "abcdefghijklmnopqrstuvwxyzzyxwvutsrqponmlkjihgfedcba"
# info = "babad"
# info = "cbbd"


def get_back_num(info, left, right):
    # print('left : {}, right : {}, {} , {} , {}'.format(left, right, info[left], info[right], info[left: right+1]))
    # print('left : {}, right : {}'.format(left, right))
    # print('{} , {}'.format(info[left], info[right]))
    if left < 0:
        return info[0: right]
    if right > len(info) - 1:
        return info[left + 1:]
    if info[left] == info[right]:
        return get_back_num(info, left - 1, right + 1)
    else:
        return info[left + 1: right]


start_time = time.perf_counter()
index = 0
max_len = 1
max_value = info[0]
info_len = len(info)
for index in range(info_len - 1):
    # print("index : {}".format(index))
    if info_len - index < max_len / 2:
        break
    # 以自身为中心对称
    temp_num = get_back_num(info, index, index)
    if len(temp_num) > max_len:
        max_len = len(temp_num)
        max_value = temp_num
    if info[index] == info[index + 1]:
        # 当前元素和后一个元素对称，没有中轴元素
        temp_num = get_back_num(info, index, index + 1)
        if len(temp_num) > max_len:
            max_len = len(temp_num)
            max_value = temp_num

# for index in range(len(info)):
#     # print("index : {}".format(index))
#     temp_num = get_back_num(info, index, index+1)
#     # print('temp num : {}'.format(temp_num))
#     if len(temp_num) > max_len:
#         max_len = len(temp_num)
#         max_value = temp_num

print(max_value)
print('执行用时: {}'.format(time.perf_counter() - start_time))
