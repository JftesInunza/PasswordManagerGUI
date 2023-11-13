import pathlib
import json


def open_json(filepath: str) -> dict:
    json_file = pathlib.Path(filepath)
    if not json_file.exists():
        return {}

    with json_file.open('r+') as f:
        return json.load(f)


def save_json(filepath: str, data: dict) -> None:
    try:
        with pathlib.Path(filepath).open("w") as f:
            json.dump(data, f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error occurred: {e}")
