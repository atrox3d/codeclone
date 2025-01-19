import json


def save(data:dict, json_path:str, indent:int=2) -> dict:

    with open(json_path, 'w') as fp:
        json.dump(data, fp, indent=indent)


def load(json_path:str) -> dict:

    with open(json_path) as fp:
        return json.load(fp)