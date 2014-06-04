def prev_offset(of, lm):
    if of-lm<0:
        return of
    else:
        return of-lm

def next_offset(of, lm, size):
    if of+lm>size:
        return of
    else:
        return of+lm


def get_offsets(total_rows, limit):
    offset_list = []
    pages = 0
    if total_rows%limit>0:
        pages = (total_rows//limit) + 1
    else:
        pages = (total_rows//limit)
    offset = 0
    for i in range(pages):
        offset_list.append({'page_num': (i+1),
                            'offset'  : offset})
        offset = offset + limit
    return offset_list