#!/bin/python

import os
import yaml
from hanziconv import HanziConv
import pinyin

def parse_sitemap():
    with open("sitemap.yaml") as sitemap:
        return yaml.load(sitemap, Loader=yaml.Loader)

def write_sitemap(sitemap, f):
    if "categories" not in sitemap:
        return

    for category in sitemap["categories"]:
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
        write_sitemap(category, f) 
        f.write("</li>\n")
        f.write("</ul>\n")

if __name__ == "__main__":
    try:
        os.mkdir("build")
    except FileExistsError as e:
        pass

    with open("build/sitemap.html", "w") as o:
        write_sitemap(parse_sitemap(), o)
