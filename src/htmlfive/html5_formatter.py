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
from typing import Union
from .html5_common import void_elements, require_end_tags


class Html5Formatter:
    """
    Export a DOM describing an HTML5 document to a formatted (and styled) HTML string.

    Args:
        indent_spaces: number of spaces to make up each indent
        line_limit: limit the length of formatted output lines
        tag_style: CSS to apply to tag names
        attribute_name_style: CSS to apply to attribute names
        attribute_value_style: CSS to apply to attribute values
        comment_style: CSS to apply to comments
    Returns:
        A string containing the formatted HTML

    A way you might use me is:

    >>> from htmlfive import Html5Formatter
    >>> from xml.dom.minidom import getDOMImplementation
    >>> doc = getDOMImplementation().createDocument(None, "html", None)
    >>> body = doc.createElement("body")
    >>> body.setAttribute("attrname", "attrvalue")
    >>> doc.documentElement.appendChild(body)
    >>> txt = doc.createTextNode("Hello")
    >>> body.appendChild(txt)
    >>> formatter = Html5Formatter()
    >>> exported = formatter.format(doc)
    >>> print(exported)
    &lt;!DOCTYPE html&gt;
    &lt;<span style="color:red;">html</span>&gt;
        &lt;<span style="color:red;">body</span> <span style="color:blue;">attrname</span>=<span style="color:purple;">"attrvalue"</span>&gt;
            Hello
        &lt;/<span style="color:red;">body</span>&gt;
    &lt;/<span style="color:red;">html</span>&gt;

    """

    def __init__(self, indent_spaces: int = 4, line_limit: int = 40, tag_style: str = "color:red;",
                 attribute_name_style: str = "color:blue;", attribute_value_style: str = "color:purple;",
                 comment_style: str = "color:gray;"):
        self.indent_spaces = indent_spaces
        self.line_limit = line_limit
        self.tag_style = tag_style
        self.attribute_name_style = attribute_name_style
        self.attribute_value_style = attribute_value_style
        self.comment_style = comment_style

    def format(self, doc_or_element: Union[xml.dom.minidom.Element, xml.dom.minidom.Document]) -> str:
        """
        Export a DOM to a formatted HTML string.

        Args:
            doc_or_element: the DOM document or element to export.

        Returns:
            A string containing the formatted HTML
        """
        if isinstance(doc_or_element, xml.dom.minidom.Document):
            element = doc_or_element.documentElement
            header = "&lt;!DOCTYPE html&gt;\n"
        else:
            element = doc_or_element
            header = ""
        return header + self.__escape_element(element, 0)[1:]  # skip newline

    def __indent_line(self, indent):
        return "\n" + " " * indent * self.indent_spaces

    def __escape_element(self, element, indent):
        tag = element.tagName.lower()

        lines = ""
        line = self.__indent_line(indent)
        line_length = len(line)

        line += "&lt;"
        line += '<span style="%s">' % self.tag_style + tag + '</span>'
        line_length += len(tag) + 1
        attrs = element.attributes;
        for (aname, avalue) in attrs.items():
            if line_length > self.line_limit:
                lines += line
                line = self.__indent_line(indent + 1)
                line_length = len(line)

            line += ' ' + '<span style="%s">' % self.attribute_name_style + aname + '</span>';
            if avalue is not None:
                q = '"'
                if q in avalue:
                    q = "'"

                line += "=" + '<span style="%s">' % self.attribute_value_style + q + avalue + q + '</span>'
            else:
                avalue = ""
            line_length += len(aname) + len(avalue) + 4

        children = element.childNodes;
        if len(children) == 0 and tag != "div" and tag not in require_end_tags:
            if tag not in void_elements:
                line += "/"
            line += "&gt;"
            lines += line
        else:
            line += "&gt;"

            if len(children):
                lines += line

                for node in children:

                    if node.nodeType == node.ELEMENT_NODE:
                        lines += self.__escape_element(node, indent + 1)

                    elif node.nodeType == node.TEXT_NODE:
                        if node.nodeValue:
                            lines += self.__dump_text_node(node, indent + 1)

                    elif node.nodeType == node.COMMENT_NODE:
                        lines += self.__dump_comment_node(node, indent + 1)

                line = self.__indent_line(indent)
            line += "&lt;/" + '<span style="%s">' % self.tag_style + tag + '</span>' + "&gt;"
            lines += line

        return lines

    def __dump_text_node(self, node, indent):
        lines = ""
        textlines = node.nodeValue.split("\n")
        for line in textlines:
            line = line.strip()
            if line:
                lines += self.__indent_line(indent) + line
        return lines

    def __dump_comment_node(self, node, indent):
        lines = ""
        lines += self.__indent_line(indent)+'<pre style="%s">'% self.comment_style
        lines += self.__indent_line(indent)+"&lt;!--"
        textlines = node.nodeValue.split("\n")
        for line in textlines:
            line = line.strip()
            if line:
                lines += self.__indent_line(indent+1) + line
            line += "\n"
        lines += self.__indent_line(indent) + "&gt;!--"
        lines += "</pre>"
        return lines
