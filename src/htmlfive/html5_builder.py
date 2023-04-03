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
import typing
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
    """
    Represent an HTML5 element node.  Do not construct these directly, instead use ElementFragment.add_text
    """

    def __init__(self, builder, text):
        super().__init__(builder)
        self.text = text
        self.set_node(self.builder.doc.createTextNode(self.text))


class ElementFragment(Fragment):
    """
    Represent an HTML5 element node.  Do not construct these directly, instead use ElementFragment.add_element
    """

    def __init__(self, builder: "Html5Builder", tag: str, attrs: typing.Dict[str, str] = {},
                 style: typing.Dict[str, str] = {}):
        super().__init__(builder)
        self.tag = tag
        self.attrs = attrs
        self.child_fragments = []
        self.set_node(self.builder.doc.createElement(self.tag))
        for (name, value) in self.attrs.items():
            self.node.setAttribute(name, value)
        if style:
            style_value = ""
            for (name, value) in style.items():
                style_value += name + ":" + str(value) + ";"
            self.node.setAttribute("style", style_value)

    def add_element(self, tag: str, attrs: typing.Dict[str, str] = {},
                    style: typing.Dict[str, str] = {}) -> "ElementFragment":
        """
        Add a child element fragment to this fragment

        Arguments:
            tag: the tag name to add
            attrs: dictionary containing the names and values of attributes.
            style: dictionary contiaining the names and values of CSS styles to apply.

        Returns:
             The child fragment that was added
        """
        fragment = ElementFragment(self.builder, tag, attrs, style)
        self.add_fragment(fragment)
        return fragment

    def add_text(self, text: str) -> TextFragment:
        """
        Add a child text fragment to this fragment

        Arguments:
            text: the text to include

         Returns:
             The child fragment that was added
        """
        fragment = TextFragment(self.builder, text)
        self.add_fragment(fragment)
        return fragment

    def add_fragment(self, fragment: Fragment) -> "Html5Builder":
        self.child_fragments.append(fragment)
        self.node.appendChild(fragment.get_node())
        return self


class Html5Builder:
    """
    Create and populate an html5 document

    A way you might use me is:

    >>> builder = Html5Builder(language="en")
    >>> builder.head().add_element("title").add_text("Title!")
    >>> builder.body().add_element("h1",{"id":"heading"}).add_text("Heading")
    >>> builder.body().add_element("div").add_text("Lorem Ipsum")
    >>> print(builder.get_html())
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>
                Title!
            </title>
        </head>
        <body>
            <h1 id="heading">
                Heading
            </h1>
            <div>
                Lorem Ipsum
            </div>
        </body>
    </html>
    """

    def __init__(self, language: str = ""):
        self.doc = getDOMImplementation().createDocument(None, "html", None)
        self.root = self.doc.documentElement
        if language:
            self.root.setAttribute("lang", language)
        self.__head = ElementFragment(self, "head")
        self.__body = ElementFragment(self, "body")
        self.root.appendChild(self.__head.get_node())
        self.root.appendChild(self.__body.get_node())

    def head(self) -> ElementFragment:
        """
        Get the head fragment of the document being built

        Returns:
             Html <head> fragment
        """
        return self.__head

    def body(self) -> ElementFragment:
        """
        Get the body fragment of the document being built

        Returns:
             Html <body> fragment
        """
        return self.__body

    def get_html(self) -> str:
        """
        Get an HTML5 string representation of the document being built

        Returns:
             Html formatted string
        """
        exporter = Html5Exporter()
        return exporter.export(self.doc).strip()
