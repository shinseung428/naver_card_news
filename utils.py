from PIL import ImageFont, ImageDraw, Image

FONT_PATH = 'static/fonts/nanum.ttf'

def find_font_size(image, text_list, margin_height, img_fraction=0.7):
    min_font_size = 1
    for text in text_list:
        draw = ImageDraw.Draw(image)
        fontsize = 1  # starting font size

        font = ImageFont.truetype(FONT_PATH, fontsize)

        while font.getsize(text)[0] < img_fraction * image.size[0] and font.getsize(text)[1] < margin_height * img_fraction:
            # iterate until the text size is just larger than the criteria
            fontsize += 1
            font = ImageFont.truetype(FONT_PATH, fontsize)

        # optionally de-increment to be sure it is less than criteria
        fontsize -= 1
        font = ImageFont.truetype(FONT_PATH, fontsize)

        if fontsize > min_font_size:
            min_font_size = fontsize

    return min_font_size


def put_text(image, text, position, color, font_size):
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(FONT_PATH, font_size)

    draw.text(position, text, font=font, color=color) # put the text on the image

    return image

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result
