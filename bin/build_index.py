#!/bin/python

import os
import yaml
from hanziconv import HanziConv
import pinyin

def parse_index():
    with open("index.yaml") as idx:
        return yaml.load(idx, Loader=yaml.Loader)

def write_index(index, f):
    if "categories" not in index:
        return

    for category in index["categories"]:
        if "cn" in category:
            cn = category["cn"]
            zh = HanziConv.toTraditional(cn)
            py = pinyin.get(cn, delimiter=" ")
        elif "zh" in category:
            zh = category["zh"]
            cn = HanziConv.toSimplified(zh)
            py = pinyin.get(zh, delimiter=" ")
        f.write("<ul>\n")
        f.write("<li>\n")
        f.write("{}<br>{}<br>{}<br>{}".format(category["en"], cn, zh, py))
        write_index(category, f) 
        f.write("</li>\n")
        f.write("</ul>\n")

if __name__ == "__main__":
    try:
        os.mkdir("build")
    except FileExistsError as e:
        pass

    with open("build/index.html", "w") as o:
        write_index(parse_index(), o)
