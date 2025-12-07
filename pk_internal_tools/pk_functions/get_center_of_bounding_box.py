from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_center_of_bounding_box(bounding_box):
    """
    바운딩 박스 좌표를 받아서, 그 중심 좌표를 반환하는 함수.

    :param bounding_box: 바운딩 박스 좌표 [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    :return: 중심 좌표 (x, y)
    """
    # 네 점의 x, y 좌표를 각각 합산
    if bounding_box is None:
        return None
    x_coords = [point[0] for point in bounding_box]
    y_coords = [point[1] for point in bounding_box]

    # x, y 평균값을 구하여 중심 좌표 계산
    center_x = sum(x_coords) / 4
    center_y = sum(y_coords) / 4

    return center_x, center_y
