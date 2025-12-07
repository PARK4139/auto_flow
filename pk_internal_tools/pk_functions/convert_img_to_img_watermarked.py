def convert_img_to_img_watermarked(img_pnx):
    from PIL import Image, ImageFont, ImageDraw

    # step2.워터마크 삽입할 이미지 불러오기
    img = Image.open('cat.jpg')
    width, height = img.size

    # step3.그림판에 이미지를 그대로 붙여넣는 느낌의 Draw() 함수
    draw = ImageDraw.Draw(img)

    # step4.삽입할 워터마크 문자
    text = "봵 워터마크"

    # step5.삽입할 문자의 폰트 설정
    font = ImageFont.truetype('/Users/sangwoo/Downloads/나눔 글꼴/나눔손글씨_펜/NanumPen.ttf', 30)

    # step6.삽입할 문자의 높이, 너비 정보 가져오기
    width_txt, height_txt = draw.textsize(text, font)  # noqa

    # step7.워터마크 위치 설정
    margin = 10
    x = width - width_txt - margin
    y = height - height_txt - margin

    # step8.텍스트 적용하기
    draw.text((x, y), text, fill='blue', font=font)

    # step9.이미지 출력
    img.show()

    # step10.현재작업 경로에 완성 이미지 저장
    img.save("cat_watermakr.jpg")  # 절대경로 되는지 확인해보자.
