import openai
import os
from tools.token import save_token, load_token
from tools.configuration import config_gen, read_config
from tools.utils import typewriter

KEY_PATH = ".secret"
CONFIG_PATH = "config.yaml"


def openai_token():
    password = None
    if not os.path.isfile(KEY_PATH):
        token = input("Please input OpenAI API Key: ")
        password = input("Please input password: ")
        save_token(KEY_PATH, token, password)
        print("\nToken saved.\n")
    if password is None:
        password = input("Please input password: ")
        print()
    return load_token(KEY_PATH, password)


def gpt(message, config) -> dict:
    return openai.ChatCompletion.create(
        model=config["model"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        presence_penalty=config["presence_penalty"],
        frequency_penalty=config["frequency_penalty"],
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ],
    )


def main():
    os.system("clear")
    openai.api_key = openai_token()
    if not os.path.isfile(CONFIG_PATH):
        config_gen(CONFIG_PATH)
    config = read_config(CONFIG_PATH)
    while True:
        response = gpt(message=input("===== Input Below ====\n\n"), config=config)
        typewriter(response["choices"][0]["message"]["content"] + "\n\n")


if __name__ == "__main__":
    main()
