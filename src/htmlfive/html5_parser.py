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
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from .html5_common import HTML5_DOCTYPE, require_end_tags, void_elements
import html as htmlutils


class Html5Parser:
    """
    Initialise an HTML parser

    A way you might use me is:

    >>> from htmlfive import Html5Parser
    >>> parser = Html5Parser()
    >>> doc = parser.parse("<!DOCTYPE html><html><body>Hello World</body></html>")
    >>> print(doc)
    <xml.dom.minidom.Document object at 0x7f53106c6dc0>
    >>> print(doc.toprettyxml(indent="    "))
    <?xml version="1.0" ?>
    <html>
        <body>Hello World</body>
    </html>
    """

    def __init__(self):
        self.pos = 0
        self.current_tag = None
        self.tag_stack = []

    def __skip_doctype(self):
        if self.content[0:10] == "<!DOCTYPE ":
            self.pos = 10
            while self.content[self.pos] == " ":
                self.pos += 1
            while self.content[self.pos] != ">":
                self.pos += 1
            self.pos += 1

    def __parse_attrs(self, s):
        attrs = {}
        attr_name = ""
        idx = 0
        while idx < len(s):
            c = s[idx]
            if c == ' ' or c == '=':
                idx += 1
            elif c == '"' or c == '\'':
                attr_value = ""
                idx += 1
                quote = c
                while idx < len(s):
                    c = s[idx]
                    idx += 1
                    if c != quote:
                        attr_value += c
                    else:
                        break
                attrs[attr_name] = htmlutils.unescape(attr_value)
                attr_name = ""
            else:
                if attr_name:
                    attrs[attr_name] = None
                attr_name = ""
                while idx < len(s):
                    c = s[idx]
                    idx += 1
                    if c != ' ' and c != '=':
                        attr_name += c
                    else:
                        break

        if attr_name:
            attrs[attr_name] = None
        return attrs

    def __pop_tag_stack(self):
        self.tag_stack = self.tag_stack[:-1]
        self.current_tag = self.tag_stack[-1] if self.tag_stack else None

    def __push_tag_stack(self, tag):
        self.tag_stack.append(tag)
        self.current_tag = tag

    def __get_tokens(self):
        while self.pos < len(self.content):
            token = ''
            # rather crudely intercept XML comments and yield contents with tag=__comment__
            if self.content[self.pos:self.pos+4] == "<!--":
                self.pos += 4
                comment_start = self.pos
                while self.content[self.pos:self.pos+3] != "-->":
                    self.pos += 1
                comment_end = self.pos
                self.pos += 3
                yield ("__comment__", self.content[comment_start:comment_end])
            if self.content[self.pos] == "<":
                quoted = False
                while self.content[self.pos] != ">" or quoted:
                    c = self.content[self.pos]
                    if c == '"':
                        quoted = not quoted
                    token += c
                    self.pos += 1
                    if self.pos >= len(self.content):
                        yield (None, None)
                token += ">"
                self.pos += 1
                if token.startswith("</"):
                    info = (self.current_tag, None)
                    self.__pop_tag_stack()
                    yield info
                else:
                    attrs = {}
                    if " " in token:
                        attrs_str = token[token.find(" "):]
                        if attrs_str.endswith("/>"):
                            attrs_str = attrs_str[:-2]
                        elif attrs_str.endswith(">"):
                            attrs_str = attrs_str[:-1]
                        attrs = self.__parse_attrs(attrs_str)
                        tag = token[1:token.find(" ")]
                    else:
                        tag = token[1:]
                    if tag.endswith(">"):
                        tag = tag[:-1]
                    info = (tag, attrs)
                    if not token.endswith("/>") and tag not in void_elements:
                        self.__push_tag_stack(tag)
                    yield info
                    if token.endswith("/>") or tag in void_elements:
                        yield (tag, None)
            else:
                while self.content[self.pos] != "<" or \
                        (self.current_tag and self.current_tag in require_end_tags \
                         and not self.content[self.pos:].startswith("</" + self.current_tag)):
                    token += self.content[self.pos]
                    self.pos += 1
                    if self.pos >= len(self.content):
                        yield (None, None)
                yield (None, token)

    def parse(self, html: str) -> xml.dom.minidom.Document:
        """
        Parse the HTML content.  The HTML must be valid otherwise the behaviour is undefined.

        Args:
            html: A string containing the HTML to parse

        Returns:
            Document object representing the HTML document
        """
        self.content = html.strip(" \t\n")

        self.pos = 0
        self.current_tag = None
        self.tag_stack = []

        self.__skip_doctype()

        impl = getDOMImplementation()
        dom = None
        current_element = None
        for (tag, content) in self.__get_tokens():
            if tag is not None and content is not None:
                if dom is None:
                    dom = impl.createDocument(None, tag, None)
                    current_element = dom.documentElement
                else:
                    if tag == "__comment__":
                        comment = dom.createComment(content)
                        current_element.appendChild(comment)
                    else:
                        child = dom.createElement(tag)
                        current_element.appendChild(child)
                        current_element = child
                        for (name, value) in content.items():
                            current_element.setAttribute(name, value)
            elif tag is not None and content is None:
                current_element = current_element.parentNode
            elif content is not None:
                if content.replace(" ", "").replace("\n", "").replace("\t", ""):
                    current_element.appendChild(dom.createTextNode(htmlutils.unescape(content)))
            else:
                return None
        return dom
