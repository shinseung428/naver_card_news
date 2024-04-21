import os
import cv2
import numpy as np

from utils import add_margin, find_font_size, put_text
from PIL import Image, ImageDraw, ImageFont

class NewsGenerator:
    def __init__(self, cfg):
        self.template_image_path = cfg["template_image_path"]
        self.image_save_basepath = cfg["save_path"]

        if not os.path.exists(self.image_save_basepath):
            os.makedirs(self.image_save_basepath)

        self.title_text_position = (80, 150)
        self.content_start_x = 120
        self.content_y_margin = 40

        self.title_text_color = (0, 0, 0)
        self.content_text_color = (0, 0, 0)

        self.top_imgfrac_ratio = 0.65
        self.bottom_imgfrac_ratio = 0.5
        self.image_size_ratio = 0.5

    def generate(self, title, text_list, image_path):
        # format title string to file name
        if type(title) == str:
            title_filename = title.replace(' ', '_')
        elif type(title) == list:
            title_filename = title[0].replace(' ', '_')

        # prepare save path
        save_basepath = os.path.join(self.image_save_basepath, title_filename)
        if not os.path.exists(save_basepath):
            os.makedirs(save_basepath)

        # prepare template image
        template_image = Image.open(self.template_image_path)
        template_image = template_image.convert('RGB')
        template_image_width, template_image_height = template_image.size

        image = Image.open(image_path)
        image_width, image_height = image.size

        # resize image in the news to fit in the template
        # the size of the template is 1080 x 1080
        # keep the the same aspect ratio
        if image_width > image_height:
            new_width = int(template_image_width * self.image_size_ratio)
            new_height = int(image_height * new_width / image_width)
        else:
            new_height = int(template_image_height * self.image_size_ratio)
            new_width = int(image_width * new_height / image_height)
        image = image.resize((new_width, new_height))


        top_margin_size = template_image.size[1] // 3
        bottom_margin_size = template_image.size[1] // 2

        if type(title) == str or (type(title) == list and len(title) == 1):
            # put title
            top_imgfrac_ratio = 0.8
            title_font_size = find_font_size(template_image, [title], top_margin_size, img_fraction=top_imgfrac_ratio)
            template_image = put_text(template_image, title, self.title_text_position, self.title_text_color, title_font_size)
        elif type(title) == list:
            min_title_font_size = np.inf
            for title_elem in title:
                # put title
                title_font_size = find_font_size(template_image, [title_elem], top_margin_size, img_fraction=self.top_imgfrac_ratio)
                if title_font_size < min_title_font_size:
                    min_title_font_size = title_font_size

            for title_elem in title:
                template_image = put_text(
                    template_image, title_elem, self.title_text_position, self.title_text_color, min_title_font_size
                )
                self.title_text_position = (self.title_text_position[0], self.title_text_position[1] + 50)
        else:
            raise ValueError('title should be either string or list of strings')

        # put content
        cur_margin = 0
        content_text_position = (self.content_start_x, top_margin_size + new_height)
        content_font_size = find_font_size(template_image, text_list, bottom_margin_size, img_fraction=self.bottom_imgfrac_ratio)
        for idx, text in enumerate(text_list):
            content_text_position = (self.content_start_x, top_margin_size + new_height + cur_margin)
            cur_margin += self.content_y_margin

            text = f'- {text}'
            template_image = put_text(template_image, text, content_text_position, self.content_text_color, content_font_size)

        if image is not None:
            # position image at the center
            position = (template_image.size[0] - image.size[0]) // 2, int(top_margin_size * 0.8)
            template_image.paste(image, position)

        image_save_path = os.path.join(save_basepath, f'result.jpg')
        template_image.save(image_save_path)
