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
import re

from .html5_common import HTML5_DOCTYPE, raw_text_elements, void_elements


class Html5Parser:

    def __init__(self,content):
        self.content = content.strip()
        if self.content.startswith(HTML5_DOCTYPE):
            self.content = self.content[len(HTML5_DOCTYPE):].strip()
        self.pos = 0
        self.current_tag = None
        self.tag_stack = []
        self.attr_regexp1 = re.compile(r'\s*([^\s=]+)\s*=\s*"([^"]*)"')
        self.attr_regexp2 = re.compile(r"\s*([^\s=]+)\s*=\s*'([^']*)'")

    def parse_attrs(self,s):
        attrs = {}
        for regexp in [self.attr_regexp1,self.attr_regexp2]:
            attr_list = regexp.findall(s)
            for attr in attr_list:
                attr_name = attr[0]
                attr_value = attr[1]
                if attr_value == '':
                    attr_value = attr[2]
                attrs[attr_name] = attr_value
        return attrs

    def pop_tag_stack(self):
        self.tag_stack = self.tag_stack[:-1]
        self.current_tag = self.tag_stack[-1] if self.tag_stack else None

    def push_tag_stack(self, tag):
        self.tag_stack.append(tag)
        self.current_tag = tag

    def get_tokens(self):
        while self.pos < len(self.content):
            token = ''
            if self.content[self.pos] == "<":
                quoted = False
                while self.content[self.pos] != ">" or quoted:
                    c = self.content[self.pos]
                    if c == '"':
                        quoted = not quoted
                    token += c
                    self.pos += 1
                    if self.pos >= len(self.content):
                        yield (None,None)
                token += ">"
                self.pos += 1
                if token.startswith("</"):
                    info = (self.current_tag,None)
                    self.pop_tag_stack()
                    yield info
                else:
                    attrs = {}
                    if " " in token:
                        attrs_str = token[token.find(" "):]
                        if attrs_str.endswith("/>"):
                            attrs_str = attrs_str[:-2]
                        elif attrs_str.endswith(">"):
                            attrs_str = attrs_str[:-1]
                        attrs = self.parse_attrs(attrs_str)
                        tag = token[1:token.find(" ")]
                    else:
                        tag = token[1:]
                    if tag.endswith(">"):
                        tag = tag[:-1]
                    info = (tag,attrs)
                    if not token.endswith("/>") and tag not in void_elements:
                        self.push_tag_stack(tag)
                    yield info
                    if token.endswith("/>") or tag in void_elements:
                        yield (tag,None)
            else:
                while self.content[self.pos] != "<" or \
                    (self.current_tag and self.current_tag in raw_text_elements \
                     and not self.content[self.pos:].startswith("</"+self.current_tag)):
                    token += self.content[self.pos]
                    self.pos += 1
                    if self.pos >= len(self.content):
                        yield (None,None)
                yield (None,token)

    def parse(self):
        impl = getDOMImplementation()
        dom = None
        current_element = None
        for (tag, content) in self.get_tokens():
            if tag is not None and content is not None:
                if dom is None:
                    dom = impl.createDocument(None, tag, None)
                    current_element = dom.documentElement
                else:
                    child = dom.createElement(tag)
                    current_element.appendChild(child)
                    current_element = child
                for (name,value) in content.items():
                    current_element.setAttribute(name,value)
            elif tag is not None and content is None:
                current_element = current_element.parentNode
            elif content is not None:
                if content.replace(" ","").replace("\n","").replace("\t",""):
                    current_element.appendChild(dom.createTextNode(content))
            else:
                return None
        return dom

