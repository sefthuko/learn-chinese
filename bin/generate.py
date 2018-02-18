#!/bin/python

import os

def parse_index():
    return {}

def parse_content():
    return {}

def write_content(model):
    pass

if __name__ == "__main__":
    os.mkdir("build")
    index = parse_index()
    model = parse_content()

    write_content(model)
