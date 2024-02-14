from openai import OpenAI

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class OpenAiHelper:
    def __init__(self, token, model="gpt-3.5-turbo-1106"):
        self.client = OpenAI(api_key=token)
        self.model = model

    def get_response(self, message_text):
        print(message_text)
        completion = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": message_text}])
        return completion.choices[0].message.content

    def get_prompt(self, prompt_type="all"):
        folder_name = "content/prompts/"
        if prompt_type == 'task':
            folder_name += "task"
            file_name = str(os.getenv("PROMPT_TASK")) + ".txt"
        elif prompt_type == 'summary':
            folder_name += "summary"
            file_name = str(os.getenv("PROMPT_SUMMARY")) + ".txt"
        elif prompt_type == 'event':
            folder_name += "event"
            file_name = str(os.getenv("PROMPT_EVENT")) + ".txt"
        else:
            folder_name += "all"
            file_name = str(os.getenv("PROMPT_ALL")) + ".txt"

        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(
            parent_dir, folder_name, file_name)

        prompt = ""
        try:
            with open(file_path, 'r') as file:
                prompt += file.read()
        except:
            print("error")
            prompt == ""
        print(f"Prompt used: {prompt}")
        return prompt

    def get_task_response(self, message_text, username):
        prompt = self.get_prompt("task")
        prompt = prompt.replace("{username}", username)
        combined_message = f"{prompt}\n\n{message_text}"
        print("get /task")

        completion = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": combined_message}])
        return completion.choices[0].message.content

    async def get_event_response(self, message_text, username):
        prompt = self.get_prompt("event")
        prompt = prompt.replace("{username}", username)
        combined_message = f"{prompt}\n\n{message_text}"
        print("get /event")

        completion = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": combined_message}])
        return completion.choices[0].message.content

    def get_summary_response(self, message_text, username):
        prompt = self.get_prompt("summary")
        prompt = prompt.replace("{username}", username)
        combined_message = f"{prompt}\n\n{message_text}"
        print("get /summary")

        completion = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": combined_message}])
        return completion.choices[0].message.content

    def get_summary_event_todo_response(self, message_text, username):
        prompt = self.get_prompt("all")
        prompt = prompt.replace("{username}", username)
        combined_message = f"{prompt}\n\n{message_text}"
        print("get /all")

        completion = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": combined_message}])
        return completion.choices[0].message.content
