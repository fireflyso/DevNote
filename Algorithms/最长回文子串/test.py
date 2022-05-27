def fun(str_info):
    info_len = len(str_info)
    if not str_info:
        return None
    if info_len == 1:
        return str_info
    max_len = 1
    max_value = str_info[0]
    for i in range(info_len):
        if info_len - i < max_len:
            break
        for j in range(info_len + 1, i + 1, -1):
            if j - i < max_len:
                break
            temp_value = str_info[i:j]
            # print("temp_value : {}, check res: {}".format(temp_value, check_str(temp_value)))
            is_back_num = check_str(temp_value)
            if is_back_num:
                if len(temp_value) > max_len:
                    max_len = len(temp_value)
                    max_value = temp_value
                # print('len : {}, value : {}'.format(len(temp_value), temp_value))
                break

    return max_value


count = 0


def check_str(info: str = ''):
    global count
    count += 1
    info_len = len(info)
    if info_len == 1:
        return True
    for index in range(int(info_len / 2)):
        if info[index] != info[0 - index - 1]:
            return False

    return True


info = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabcaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
# info = "aaaaaaaaabaaaaaaaaaa"

import time

start_time = time.perf_counter()
print(fun(info))
print('执行用时: {}'.format(time.perf_counter() - start_time))
print(count)
