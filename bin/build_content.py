#!/bin/python

import os
import yaml
from hanziconv import HanziConv
import pinyin

def parse_content(i):
    return yaml.load(i, Loader=yaml.Loader)

def fill_atom(atom, charset):
    if charset == "zh":
        if "zh" in atom:
            cn = atom["zh"]
        else:
            cn = HanziConv.toTraditional(atom["cn"])
        
        if "py" in atom:
            py = atom["py"]
        else:
            py = pinyin.get(cn, delimiter=" ")
    elif charset == "cn":
        if "cn" in atom:
            cn = atom["cn"]
        else:
            cn = HanziConv.toSimplified(atom["zh"])
        
        if "py" in atom:
            py = atom["py"]
        else:
            py = pinyin.get(cn, delimiter=" ")

    if "en" in atom:
        en = atom["en"]
    else:
        en = "&nbsp;"

    return cn, py, en

def write_line(line, f, charset):
    for atom in line["atoms"]:
        cn, py, en = fill_atom(atom, charset)
        f.write("""        <div class="atom highlight">
        <div>{}</div>
        <div>{}</div>
        <div>{}</div>
    </div>
""".format(py, cn, en))
    f.write("""        <br>
            <div class="atom">({})</div>
        </div>
""".format(line["en"]))

def write_content(content, f, charset):
    f.write("""<html>
    <head>
        <title>{}</title>
        <style>
div.line {{
    padding-bottom: 1em;
}}

div.indented {{
    padding-left: 2em;
}}

div.atom {{
    padding-right: 0.2em;
    display: inline-block;
}}

div.highlight:hover {{
    background-color: #DDD;
}}
        </style>
    </head>
    <body>
""".format(content["title"]["en"]))

    f.write("            <center>\n")
    write_line(content["title"], f, charset)
    f.write("""            </center>
            <p>
""")

    for line in content["body"]["lines"]:
        if "flow" in line and line["flow"] == "indent":
            f.write("""       <div class="indented line">\n""")
        else:
            f.write("""       <div class="line">\n""")

        write_line(line, f, charset)

    f.write("""    </body>
</html>""")

if __name__ == "__main__":
    for (dirpath, dirnames, filenames) in os.walk("content"):
        for basename in filenames:
            if not basename.endswith(".yaml"):
                continue

            ifn = "{}/{}".format(dirpath, basename)
            od = "build/{}".format("/".join(dirpath.split("/")[1:]))
            try:
                os.makedirs(od)
            except FileExistsError as e:
                pass

            with open(ifn) as i:
                content = parse_content(i)

            out_basename = "{}/{}".format(od, basename.rsplit(".", 1)[0])
            with open(out_basename + "_simp.html", "w") as o:
                write_content(content, o, "cn")

            with open(out_basename + "_trad.html", "w") as o:
                write_content(content, o, "zh")
