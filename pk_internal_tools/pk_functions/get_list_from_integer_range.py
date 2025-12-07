





def get_list_from_integer_range(int_s, int_e):
    if int_s <= int_e:
        return list(range(int_s, int_e + 1))
    else:
        return list(range(int_s, int_e - 1, -1))  # get_list_from_integer_range(10,-10) 인 경우 처리
