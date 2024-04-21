import os
import uuid
import requests
from bs4 import BeautifulSoup

class NewsExtractor:
    def __init__(self, cfg):
        self.image_save_basepath = cfg["image_save_basepath"]
        if not os.path.exists(self.image_save_basepath):
            os.makedirs(self.image_save_basepath)

    def extract(self, news_url):
        response = requests.get(news_url, headers={'User-agent': 'Mozila/5.0'})

        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.select_one("#title_area")
        print(title.text)

        # get the body of the news
        content = soup.select_one("#dic_area")

        print(content.text)

        img_src = soup.select_one("#img1")

        if img_src is not None and img_src.get('data-src') is not None:
            img_url = img_src['data-src']

            img_data = requests.get(img_url).content

            # generate random string for image name
            filename = str(uuid.uuid4())
            image_save_path = f'{self.image_save_basepath}/{filename}.jpg'
            with open(image_save_path, 'wb') as handler:
                handler.write(img_data)
        else:
            image_save_path = None

        return title.text, content.text, image_save_path
