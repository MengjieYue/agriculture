#coding=utf-8
import StringIO
from django.http import HttpResponse
import os
import random
from PIL import Image, ImageDraw, ImageFont
from math import ceil

figures = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
           'a', 'b', 'c', 'd', 'e', 'f',
           'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r',
           's', 't', 'u', 'v', 'w', 'x',
           'y', 'z']

# font path
font_path = os.path.join('/home/server/Agriculture/agriculture/font/', 'timesbi.ttf')


def get_font_size(img_height, img_width):
    """  将图片高度的80%作为字体大小"""
    s1 = int(img_height * 0.8)
    s2 = int(img_width / 4)
    return int(min((s1, s2)) + max((s1, s2))*0.05)


def display(request, img_height, img_width):
    """  生成验证码图片"""
    # font color
    font_color = ['black', 'darkblue', 'darkred']
    # background color
    background = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))

    # creat a image
    im = Image.new('RGB', (img_width, img_height), background)
    #generate code
    words = [''.join(str(random.sample(figures, 1)[0]) for i in range(0, 4))]
    code = random.sample(words, 1)[0]
    request.session['django_captcha_key'] = code

    # set font size automaticly
    font_size = get_font_size(img_height, img_width)

    # creat a pen
    draw = ImageDraw.Draw(im)

    # draw noisy point/line
    for i in range(random.randrange(4, 6)):
        line_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        xy = (
            random.randrange(0, int(img_width*0.2)),
            random.randrange(0, img_height),
            random.randrange(3 * img_width/4, img_width),
            random.randrange(0, img_height)
        )
        draw.line(xy, fill=line_color, width=int(font_size * 0.1))

    # draw code
    j = int(font_size * 0.3)
    k = int(font_size * 0.5)
    x = random.randrange(j, k)
    for i in code:
        y = random.randrange(1, 3)
        # 字体大小变化量,字数越少,字体大小变化越多
        m = random.randrange(0, int(45 / font_size) + int(font_size / 5))
        font = ImageFont.truetype(font_path, font_size + int(ceil(m)))
        draw.text((x, y), i, font=font, fill=random.choice(font_color))
        x += font_size * 0.9
    del draw
    del x
    buf = StringIO.StringIO()
    im.save(buf, 'gif')
    return HttpResponse(buf.getvalue(), 'image/gif')