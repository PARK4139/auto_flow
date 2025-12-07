def convert_img_to_img_blurred(img_pnx):
    from PIL import Image, ImageFilter
    img_converted = Image.open(img_pnx).filter(ImageFilter.GaussianBlur(10))  # 가우시안 블러 적용 # 숫자크면 많이흐려짐
    img_converted.show()
