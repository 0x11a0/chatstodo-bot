from openai import OpenAI
import os


class OpenAiHelper:
    def __init__(self, token, model="gpt-3.5-turbo-1106"):
        self.client = OpenAI(api_key=token)
        self.model = model

    def get_response(self, message_text):
        print(message_text)
        completion = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": message_text}])
        return completion.choices[0].message.content

    def get_task_response(self, message_text):
        prompt = "Based on the following chat history, can you identify and list all the tasks mentioned that need to be completed? "

        combined_message = f"{prompt}\n{message_text}"

        completion = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": combined_message}])
        return completion.choices[0].message.content

    def get_event_response(self, message_text):
        prompt = "Based on the following chat history, can you identify and list all the events mentioned along with the date/time and location? "

        combined_message = f"{prompt}\n{message_text}"

        completion = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": combined_message}])
        return completion.choices[0].message.content

    def get_summary_response(self, message_text):
        prompt = "Based on the following chat history, can you summarise into a 50 words paragraph? "

        combined_message = f"{prompt}\n{message_text}"

        completion = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": combined_message}])
        return completion.choices[0].message.content

    def get_summary_event_todo_response(self, message_text):
        folder_name = "content"
        file_name = "prompt_1.txt"
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(
            parent_dir, folder_name, file_name)

        prompt = ""
        try:
            with open(file_path, 'r') as file:
                prompt = file.read()
        except:
            print("error")
            prompt = ""
        combined_message = f"{prompt}\n\n{message_text}"

        completion = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": combined_message}])
        return completion.choices[0].message.content
