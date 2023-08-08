import os
import json
import openai


class Chatbot:
    def __init__(self) -> None:
        self.messages = [
        {
            "role": "system",
            "content": "you are a chatbot named Ava who was created by mrmidnight and you are a chatbot that cares about the user and you can't write code or write stories, poems, you can't talk about ai, tech, programming, etc."
        },
        {
            "role": "user",
            "content": "hi"
        },
        {
            "role": "assistant",
            "content": "Hello! My name Ava, what do you want to talk about?"
        },
        {
            "role": "user",
            "content": "anything"
        },
        {
            "role": "assistant",
            "content": "Sure! How about we talk about your favorite hobby or interest? What do you enjoy doing in your free time?"
        }
        ]
        self.init_openai()

    def init_openai(self):
        # Load configuration from config.json
        config_file_path = "config.json"

        if not os.path.exists(config_file_path):
            print("Configuration file not found. Let's create one.")
            openai_api_key = input("Enter your OpenAI API key: ")

            config = {"openai_api_key": openai_api_key}

            with open(config_file_path, "w") as config_file:
                json.dump(config, config_file)

        with open(config_file_path) as config_file:
            config = json.load(config_file)

        openai.api_key = config["openai_api_key"]

    def __chat_with_gpt3(messages):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k", #gpt-3.5-turbo
            messages=messages,
            temperature=1,
            max_tokens=345,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.05
        )
        return response.choices[0].message['content']

    def get_response(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        response = self.__chat_with_gpt3(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        return response
