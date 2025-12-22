def convert_img_to_img_resized(img_pnx, width_px, height_px):
    from PIL import Image
    img_converted = Image.open(img_pnx).resize((width_px, height_px))
    img_converted.show()
