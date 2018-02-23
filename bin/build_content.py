#!/bin/python

import os
import yaml
from hanziconv import HanziConv
import pinyin

def parse_content(i):
    return yaml.load(i, Loader=yaml.Loader)

def fill_atom(atom):
    if "zh" in atom:
        zh = atom["zh"]
    else:
        zh = HanziConv.toTraditional(atom["cn"])

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

    return zh, cn, py, en

def write_line(line, f):
    f.write("""        <div class="audio" onClick="new Audio('{}').play();">\n""".format(line["cn_audio"]))

    for atom in line["atoms"]:
        zh, cn, py, en = fill_atom(atom)
        f.write("""            <div class="atom highlight">
            <div>{}</div>
            <div class="zh">{}</div>
            <div class="cn">{}</div>
            <div>{}</div>
        </div>
""".format(py, zh, cn, en))
    f.write("""        </div>
            <br>
            <div class="atom audio" onClick="new Audio('{}').play();">({})</div>
""".format(line["en_audio"], line["en"]))

def write_content(content, f):
    f.write("""<html>
    <head>
""")

    f.write("""        <title>{}</title>
""".format(content["title"]["en"]))

    f.write("""        <style>
div.story {
    font-size: 24px;
    width: 800px;
    margin-left: auto;
    margin-right: auto;
    padding: 2em;
    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.2);
    background-color: white;
}

div.cn {
    display: none;
    font-family: 'Noto Sans', 'Microsoft Yahei', SimSun, sans-serif;
}

div.zh {
    display: block;
    font-family: 'Noto Sans', 'Microsoft Yahei', SimSun, sans-serif;
}

div.line {
    padding-bottom: 1em;
}

div.indented {
    padding-left: 2em;
}

div.atom {
    padding-right: 0.2em;
    display: inline-block;
}

div.highlight:hover {
    background-color: #DDF;
}

div.audio {
    display: inline-block;
}

div.audio:hover {
    background-color: #EEF;
    cursor: pointer;
}
        </style>
""")
    f.write("""        <script src="https://code.jquery.com/jquery-1.11.3.js"></script>
    <script>
var traditional = true;

function toggle_charset() {
    traditional = !traditional;

    if (traditional) {
        $('.cn').css('display', 'none');
        $('.zh').css('display', 'block');
        $('#charset').text('Switch to Simplified');
    } else {
        $('.cn').css('display', 'block');
        $('.zh').css('display', 'none');
        $('#charset').text('Switch to Traditional');
    }
}
        </script>
""")

    f.write("""    </head>
    <body background="/bamboo.jpg">
    <a href="/content/sitemap.html">Back to site map</a><br>
    <button id="charset" onClick="toggle_charset();">Switch to Simplified</button><br>
""")

    f.write("""            <div class="story">
    <center style="font-weight: bold;">
""")
    write_line(content["title"], f)
    f.write("""            </center>
            <p>
""")

    for line in content["body"]["lines"]:
        if "flow" in line and line["flow"] == "indent":
            f.write("""           <div class="indented line">\n""")
        else:
            f.write("""           <div class="line">\n""")

        write_line(line, f)
        f.write("""            </div>
""")

    f.write("""        </div>
""")
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
            with open(out_basename + ".html", "w") as o:
                write_content(content, o)
