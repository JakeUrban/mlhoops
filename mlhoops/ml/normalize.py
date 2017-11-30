def feature_scaling(data):
    if not data or not data[0]:
        return data
    for i in range(len(data[0])):
        col = [x[i] for x in data]
        _min, _max = min(col), max(col)
        for j, x in enumerate(data):
            if x[i]:
                data[j][i] = -1+((data[j][i] - _min)*2/(_max - _min))
    return data
