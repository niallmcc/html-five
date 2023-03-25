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

class Html5Formatter:

    def __init__(self, indent_spaces=4, line_limit = 40, tag_style="color:red;", attribute_name_style="color:blue;", attribute_value_style="color:purple;"):
        self.indent_spaces = indent_spaces
        self.line_limit = line_limit
        self.tag_style = tag_style
        self.attribute_name_style = attribute_name_style
        self.attribute_value_style = attribute_value_style

    def format(self, doc):
        element = doc.documentElement
        return self.__escape_element(element,0)[1:] # skip newline

    def __indent_line(self,indent):
        return "\n"+" "*indent*self.indent_spaces

    def __escape_element(self,element,indent):
        tag = element.tagName.lower()

        lines = ""
        line = self.__indent_line(indent)
        line_length = len(line)

        line += "&lt;"
        line += '<span style="%s">'%self.tag_style + tag + '</span>'
        line_length += len(tag) + 1
        attrs = element.attributes;
        for (aname,avalue) in attrs.items():
            if line_length > self.line_limit:
                lines += line
                line = self.__indent_line(indent + 1)
                line_length = len(line)

            line += ' ' + '<span style="%s">'%self.attribute_name_style + aname + '</span>';
            if avalue:
                q = '"'
                if q in avalue:
                    q = "'"

                line += "=" + '<span style="%s">'%self.attribute_value_style + q + avalue + q + '</span>'

            line_length += len(aname) + len(avalue) + 4

        children = element.childNodes;
        if len(children) == 0 and tag != "div":
            line += "/&gt;"
            lines += line
        else:
            line += "&gt;"
            lines += line

            for node in children:

                if  node.nodeType == node.ELEMENT_NODE:
                    lines += self.__escape_element(node, indent+1)

                elif node.nodeType == node.TEXT_NODE:
                    if node.nodeValue:
                        lines += self.__dump_text_node(node, indent+1)

            line = self.__indent_line(indent)
            line += "&lt;/" + '<span style="%s">'%self.tag_style + tag + '</span>' + "&gt;"
            lines += line

        return lines

    def __dump_text_node(self, node, indent):
        lines = ""
        textlines = node.nodeValue.split("\n")
        for line in textlines:
            line = line.strip()
            if line:
                lines += self.__indent_line(indent)+line
        return lines

