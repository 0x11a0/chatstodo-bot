from openai import OpenAI


class OpenAiHelper:
    def __init__(self, token, model="gpt-3.5-turbo-1106"):
        self.client = OpenAI(api_key=token)
        self.model = model

    def get_response(self, message_text):
        print(message_text)
        completion = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": message_text}])
        return completion.choices[0].message.content
