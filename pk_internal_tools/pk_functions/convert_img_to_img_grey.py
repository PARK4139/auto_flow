def convert_img_to_img_grey(img_pnx):
    from PIL import Image
    img_converted = Image.open(img_pnx).convert("L")
    img_converted.show()
