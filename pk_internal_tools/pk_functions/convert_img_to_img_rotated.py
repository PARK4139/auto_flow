def convert_img_to_img_rotated(img_pnx, degree: int):
    import os
    from PIL import Image
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    img_converted = Image.open(img_pnx).rotate(degree)
    img_converted.show()
    img_converted.save(
        f"{os.path.dirname(img_pnx)}   {os.path.splitext(img_pnx)[0]}_$flipped_h{os.path.splitext(img_pnx)[1]}")
