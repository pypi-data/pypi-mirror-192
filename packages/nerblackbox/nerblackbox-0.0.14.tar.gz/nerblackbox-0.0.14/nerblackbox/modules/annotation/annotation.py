import os
import json
from typing import Optional


def doccano2nerblackbox(_input_file: str, _output_file: str, verbose: bool = False):
    if verbose:
        print(f"> read input_file = {_input_file}")
    with open(_input_file, "r") as f:
        input_lines = [json.loads(line) for line in f]

    output_lines = list()
    for input_line in input_lines:
        output_line = {
            "text": input_line["text"],
            "tags": [
                {
                    "char_start": label[0],
                    "char_end": label[1],
                    "token": input_line["text"][label[0] : label[1]],
                    "tag": label[2],
                }
                for label in input_line["label"]
            ],
        }
        output_lines.append(output_line)

    if verbose:
        print(f"> write output_file = {_output_file}")

    os.makedirs("/".join(_output_file.split("/")[:-1]), exist_ok=True)
    with open(_output_file, "w") as f:
        for line in output_lines:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    return _output_file


def nerblackbox2doccano(
    _input_file: str, _max_lines: Optional[int] = None, verbose: bool = False
) -> str:

    if verbose:
        print(f"> read input_file = {_input_file}")
    with open(_input_file, "r") as f:
        input_lines = [json.loads(line) for line in f]

    if _max_lines is not None:
        input_lines = input_lines[:_max_lines]

    output_lines = list()
    for input_line in input_lines:
        output_line = {
            "text": input_line["text"],
            "label": [
                [int(tag["char_start"]), int(tag["char_end"]), tag["tag"]]
                for tag in input_line["tags"]
            ],
        }
        output_lines.append(output_line)

    output_file = _input_file.replace(".jsonl", "_DOCCANO.jsonl")
    if verbose:
        print(f"> write output_file = {output_file}")
    with open(output_file, "w") as f:
        for line in output_lines:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    return output_file
