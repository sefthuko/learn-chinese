#!/bin/python

import os
import yaml
from hanziconv import HanziConv
import pinyin

def parse_sitemap():
    with open("sitemap.yaml") as sitemap:
        return yaml.load(sitemap, Loader=yaml.Loader)

def parse_story(fn):
    with open(fn) as story:
        return yaml.load(story, Loader=yaml.Loader)

def write_sitemap(sitemap, f):
    if "categories" in sitemap:
        write_categories(sitemap["categories"], f)
    elif "stories" in sitemap:
        write_stories(sitemap["stories"], f)

def write_stories(stories, f):
    f.write("<ul>\n")
    for story in stories:
        segments = "/".join(story["id"].split("."))
        yaml_path = "content/{}.yaml".format(segments)
        s = parse_story(yaml_path)

        f.write("""<li>
    <a href="{}.html">{}</a></li>
""".format(segments, s["title"]["en"]))

    f.write("</ul>\n")

def write_categories(categories, f):
    for category in categories:
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
        f.write("{}".format(category["en"]))
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
