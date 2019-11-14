# 模拟人滑动轨迹
def get_track(distance):
    '''
    根据偏移量获取移动轨迹
    :param distance: 偏移量
    :return: 移动轨迹
    '''
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    #计算间隔
    t = 0.2
    # 初速度
    v = 0
    while current < distance:
        if current < mid:
            # 加速度为正2
            a = 2
        else:
            # 加速度为-3
            a = -3
        # 初速度v0
        v0 = v
        # 当前速度
        v = v0 + a * t
        # 移动速度
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        # 加入轨迹
        track.append(round(move))
    return track
distance = get_track(112)
print(distance)
print(sum(distance))






