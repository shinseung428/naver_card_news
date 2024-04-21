import json
from openai import OpenAI

class NewsSummarizer:
    def __init__(self, cfg):
        self.temperature = 0
        self.max_title_len = 30
        self.model = cfg["model_name"]
        # self.model =
        self.main_prompt = cfg["main_prompt"]
        self.title_prompt = cfg["title_prompt"]
        self.response_format={"type":"json_object"}

        if "solar" in self.model:
            self.client = OpenAI(
                api_key=cfg["api_key"],
                base_url="https://api.upstage.ai/v1/solar"
            )
        else:
            self.client = OpenAI(api_key=cfg["api_key"])

    def _solar(self, title, content):
        messages = [
                {"role": "user", "content": "Title: {} \n Content: {} \n {}".format(title, content, self.main_prompt)},
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            extra_body={
                "format": "bullets",
                "length": "short"
            },
            temperature=self.temperature
        )
        text_list = completion.choices[0].message.content
        text_list = json.loads(text_list)["summary"]

        # shorten title if it's too long
        if len(title) > self.max_title_len:
            messages = [
                {"role": "user", "content": "{} \n {}".format(title, self.title_prompt)},
            ]
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                extra_body={
                    "format": "paragraph",
                    "length": "short"
                },
                temperature=self.temperature
            )
            title = completion.choices[0].message.content
            title = json.loads(title)["titles"]

        return text_list, title

    def _openai(self, title, content):
        messages = [
                {"role": "system", "content": self.main_prompt},
                {"role": "user", "content": "Title: {} \n Content: {}".format(title, content)},
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            response_format=self.response_format,
            temperature=self.temperature,
            messages=messages
        )
        text_list = completion.choices[0].message.content
        text_list = json.loads(text_list)["summary"]

        # shorten title if it's too long
        if len(title) > self.max_title_len:
            messages = [
                {"role": "system", "content": self.title_prompt},
                    {"role": "user", "content": "{}".format(title)},
            ]
            completion = self.client.chat.completions.create(
                model=self.model,
                response_format=self.response_format,
                temperature=self.temperature,
                messages=messages
            )
            title = completion.choices[0].message.content
            title = json.loads(title)["titles"]

        return text_list, title

    def summarize(self, title, content):

        if "solar" in self.model:
            text_list, title = self._solar(title, content)
        else:
            text_list, title = self._openai(title, content)

        print("########## SUMMARY ##########")
        print(title)
        print(text_list)
        return text_list, title
