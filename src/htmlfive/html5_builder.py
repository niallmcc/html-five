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

from xml.dom.minidom import getDOMImplementation
from .html5_exporter import Html5Exporter

class Fragment:

    def __init__(self, builder):
        self.builder = builder
        self.node = None

    def set_node(self, node):
        self.node = node

    def get_node(self):
        return self.node

class TextFragment(Fragment):

    def __init__(self, builder, text):
        super().__init__(builder)
        self.text = text
        self.set_node(self.builder.doc.createTextNode(self.text))

class Html5Fragment(Fragment):

    def __init__(self, builder, tag, attrs={}, style={}):
        super().__init__(builder)
        self.tag = tag
        self.attrs = attrs
        self.child_fragments = []
        self.set_node(self.builder.doc.createElement(self.tag))
        for (name, value) in self.attrs.items():
            self.node.setAttribute(name, value)
        if style:
            style_value = ""
            for (name,value) in style.items():
                style_value += name + ":" + str(value)+";"
            self.node.setAttribute("style",style_value)

    def add_element(self, tag, attrs={}, style={}):
        fragment = Html5Fragment(self.builder,tag,attrs,style)
        self.child_fragments.append(fragment)
        self.node.appendChild(fragment.get_node())
        return fragment

    def add_text(self, text):
        fragment = TextFragment(self.builder,text)
        self.child_fragments.append(fragment)
        self.node.appendChild(fragment.get_node())
        return fragment

    def add_widget(self, widget_cls, widget_id, **widget_kwargs):
        fragment = widget_cls.to_html(self, widget_id, **widget_kwargs)
        return fragment


class Html5Builder:

    def __init__(self, language=""):
        self.doc = getDOMImplementation().createDocument(None,"html",None)
        self.root = self.doc.documentElement
        if language:
            self.root.setAttribute("lang",language)
        self.__head = Html5Fragment(self,"head",{"class":"abc"})
        self.__body = Html5Fragment(self,"body")
        self.root.appendChild(self.__head.get_node())
        self.root.appendChild(self.__body.get_node())

    def head(self):
        return self.__head

    def body(self):
        return self.__body

    def get_html(self):
        exporter = Html5Exporter(self.doc)
        return exporter.export().strip()







