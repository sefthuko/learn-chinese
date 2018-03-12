#!/bin/python

from genshi.template import TemplateLoader
import os

if __name__ == "__main__":
    loader = TemplateLoader([os.path.abspath("templates"), os.path.abspath("content")])

    tmpl = loader.load("index.xml")
    with open("build/index.html", "w") as f:
        f.write(tmpl.generate().render('html', doctype='html'))
