





def click_center_of_img_recognized_by_mouse_left(img_pnx: str, loop_limit_cnt=0, is_zoom_toogle_mode=False):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    img = get_img_when_img_recognized_succeed(img_pnx, loop_limit_cnt, is_zoom_toogle_mode)
    if not img is None:
        center_x = img.left + (img.width / 2)
        center_y = img.top + (img.height / 2)
        ensure_mouse_moved(x_abs=center_x, y_abs=center_y)
        click_mouse_left_btn(x_abs=center_x, y_abs=center_y)
        return 1
    else:
        return 0
