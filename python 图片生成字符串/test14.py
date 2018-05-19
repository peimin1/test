import argparse
from PIL import Image


codeLib = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''
count = len(codeLib)


def transform1(image_file):
    image_file = image_file.convert("L")
    codePic = ''
    for h in range(0, image_file.size[1]):
        for w in range(0, image_file.size[0]):
            gray = image_file.getpixel((w, h))
            codePic = codePic +codeLib[int(((count - 1)*gray)/256)]
        codePic = codePic + '\r\n'
    return codePic

# def transform2(image_file):
#     codePic = ''
#     for h in range(0, image_file.size[1]):
#         for w in range(0, image_file.size[0]):
#             g, r, b = image_file.getpixel((w, h))
#             gray = int(r * 0.299 + g * 0.587 + b * 0.114)
#             codePic = codePic + codeLib[int(((count - 1)* gray)/ 256)]
#         codePic = codePic + '\r\n'


def main():
    fp = open(u'123456.jpg', 'rb')
    image_file = Image.open(fp)
    image_file = image_file.resize((int(image_file.size[0] * 0.75), int(image_file.size[1] * 0.5)))  # 调整图片大小
    print(u'Info:', image_file.size[0], ' ', image_file.size[1], ' ', count)

    tmp = open('tmp.txt', 'w')
    tmp.write(transform1(image_file))
    tmp.close()


if __name__ == '__main__':
    main()


