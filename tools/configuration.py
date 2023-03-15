import yaml
from .utils import is_float, color_print
from typing import Union

default_config = {
    "model": "gpt-3.5-turbo",
    "temperature": 1.0,
    "max_tokens": 300,
    "presence_penalty": 1.0,
    "frequency_penalty": 1.0,
}


def fine_turn(input_message, input_type, default_value, min, max) -> Union[float, int]:
    if not input_type in ["int", "float"]:
        raise ValueError("implementation error.")
    while True:
        temp = input(input_message)
        if temp == "":
            return default_value
        if input_type == "float":
            if not is_float(temp):
                raise ValueError("Implementation error.")
            temp = float(temp)
        elif input_type == "int":
            if not temp.isdigit():
                raise ValueError("Implementation error.")
            temp = int(temp)
        else:
            raise ValueError("Implementation error.")
        if temp == default_value:
            return default_value
        if temp >= min and temp <= max:
            return temp
        else:
            color_print("Invalid input.", "yellow")


def config_gen(config_path):
    config = default_config.copy()
    if input("Generate config file with default settings? (Y/n) ").lower() in {"n"}:
        print("\nLet's customize your cGPT experience.\n")
        config["max_tokens"] = fine_turn(
            input_message="max_tokens(integers only, defaults to 300): ",
            input_type="int",
            default_value=300,
            min=1,
            max=4096,
        )
        config["temperature"] = fine_turn(
            input_message="temperature(between 0 and 2, defaults to 1): ",
            input_type="float",
            default_value=1,
            min=0,
            max=2,
        )
        config["presence_penalty"] = fine_turn(
            input_message="presence_penalty(between -2.0 and 2.0, defaults to 1): ",
            input_type="float",
            default_value=1,
            min=-2.0,
            max=2.0,
        )
        config["frequency_penalty"] = fine_turn(
            input_message="frequency_penalty(between -2.0 and 2.0, defaults to 1): ",
            input_type="float",
            default_value=1,
            min=-2.0,
            max=2.0,
        )
    with open(config_path, "w") as file:
        file.write(yaml.dump(config))


def read_config(config_path) -> dict:
    with open(config_path) as file:
        return yaml.safe_load(file)
