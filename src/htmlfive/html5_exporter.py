# MIT License
#
# Copyright (c) 2023 Niall McCarroll
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import io

from .html5_common import HTML5_DOCTYPE, raw_text_elements, void_elements

class Html5Exporter:

    def __init__(self):
        pass

    def is_ws(self,txt):
        txt = txt.replace(" ","").replace("\t","").replace("\n","")
        return txt == ""

    def exportElement(self,ele,indent):
        self.of.write(indent*" ")
        self.of.write("<"+ele.tagName)
        attr_count = 0
        for (k,v) in ele.attributes.items():
            if '"' in v:
                self.of.write(" %s='%s'"%(k,v)) # single quote values containing double quote
            else:
                self.of.write(' %s="%s"'%(k,v))
            attr_count += 1
        child_count = len(ele.childNodes)

        if attr_count > 0 or ele.tagName in raw_text_elements or child_count > 0:
            self.of.write(">")
            if child_count:
                self.of.write("\n")
                for childNode in ele.childNodes:
                    if childNode.nodeType == childNode.ELEMENT_NODE:
                        self.exportElement(childNode,indent+4)
                    elif childNode.nodeType == childNode.TEXT_NODE:
                        self.exportText(childNode,indent+4)
                self.of.write(" "*indent+"</%s>"%ele.tagName)
            else:
                if ele.tagName not in void_elements:
                    self.of.write("</%s>"%ele.tagName)
        else:
            if ele.tagName not in void_elements:
                self.of.write("/>")
            else:
                self.of.write(">")
        self.of.write("\n")

    def exportText(self, tn, indent):
        txt = tn.data.rstrip(" \n").lstrip(" \n")
        if not self.is_ws(txt):
            self.of.write(" "*indent)
            self.of.write(txt)
            self.of.write("\n")

    def export(self, doc):
        self.of = io.StringIO()
        self.of.write(HTML5_DOCTYPE+"\n")
        ele = doc.documentElement
        self.exportElement(ele,0)
        return self.of.getvalue()
