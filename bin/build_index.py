#!/bin/python

from genshi.template import TemplateLoader
import os

if __name__ == "__main__":
    loader = TemplateLoader(os.path.abspath("templates"), auto_reload=True)

    tmpl = loader.load("index.html")
    with open("build/index.html", "w") as f:
        f.write(tmpl.generate().render('html', doctype='html'))
