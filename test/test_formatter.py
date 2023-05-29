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

import unittest
from htmlfive.html5_parser import Html5Parser
from htmlfive.html5_formatter import Html5Formatter
from xml.dom.minidom import getDOMImplementation

simple_test_input=\
"""<!DOCTYPE html>
<html>
    <head>
        <title>
            Title!
        </title>
    </head>
    <body>
        <h1 class="heading" a='"hello"'>
            Hello World
        </h1>
        <input type="text" id="text_input">
    </body>
</html>"""

simple_test_expected=\
"""&lt;!DOCTYPE html&gt;
&lt;<span style="color:red;">html</span>&gt;
    &lt;<span style="color:red;">head</span>&gt;
        &lt;<span style="color:red;">title</span>&gt;
            Title!
        &lt;/<span style="color:red;">title</span>&gt;
    &lt;/<span style="color:red;">head</span>&gt;
    &lt;<span style="color:red;">body</span>&gt;
        &lt;<span style="color:red;">h1</span> <span style="color:blue;">class</span>=<span style="color:purple;">"heading"</span> <span style="color:blue;">a</span>=<span style="color:purple;">'"hello"'</span>&gt;
            Hello World
        &lt;/<span style="color:red;">h1</span>&gt;
        &lt;<span style="color:red;">input</span> <span style="color:blue;">type</span>=<span style="color:purple;">"text"</span> <span style="color:blue;">id</span>=<span style="color:purple;">"text_input"</span>&gt;
    &lt;/<span style="color:red;">body</span>&gt;
&lt;/<span style="color:red;">html</span>&gt;"""

dom_expected = """&lt;!DOCTYPE html&gt;
&lt;<span style="color:red;">html</span>&gt;
    &lt;<span style="color:red;">body</span> <span style="color:blue;">attrname</span>=<span style="color:purple;">"attrvalue"</span>&gt;
        Hello
        <pre style="color:gray;">
        &lt;!--
            comment
        &gt;!--</pre>
    &lt;/<span style="color:red;">body</span>&gt;
&lt;/<span style="color:red;">html</span>&gt;
"""

class BasicTest(unittest.TestCase):

    def test_simple(self):
        # round trip some simple HTML
        parser = Html5Parser()
        dom = parser.parse(simple_test_input)
        formatter = Html5Formatter()
        exported = formatter.format(dom)
        self.assertEqual(exported.strip(), simple_test_expected.strip())

    def test_with_dom(self):
        doc = getDOMImplementation().createDocument(None, "html", None)
        body = doc.createElement("body")
        body.setAttribute("attrname", "attrvalue")
        doc.documentElement.appendChild(body)
        txt = doc.createTextNode("Hello")
        body.appendChild(txt)
        comment = doc.createComment("comment")
        body.appendChild(comment)
        formatter = Html5Formatter()
        exported = formatter.format(doc)
        with open("test.html","w") as f:
            f.write(exported)
        self.assertEqual(exported.strip(), dom_expected.strip())


if __name__ == '__main__':
    unittest.main()