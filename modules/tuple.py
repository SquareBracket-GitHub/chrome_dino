def editTuple(_tuple, edit_num, content):
    t_li = list(_tuple)
    t_li[edit_num] = content
    
    return tuple(t_li)