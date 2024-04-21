import yaml
import fire

from extractor import NewsExtractor
from summarizer import NewsSummarizer
from generator import NewsGenerator


def main(url):
    config = yaml.safe_load(open('config.yaml', 'r'))

    extractor = NewsExtractor(config)
    summarizer = NewsSummarizer(config)
    generator = NewsGenerator(config)

    title, content, image_path = extractor.extract(url)

    summarized_result, title = summarizer.summarize(title, content)

    generator.generate(title, summarized_result, image_path)


if __name__ == '__main__':
    fire.Fire(main)
