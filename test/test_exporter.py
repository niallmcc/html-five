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

from htmlfive import Html5Exporter
from xml.dom.minidom import getDOMImplementation


class BasicTest(unittest.TestCase):

    simple_expected = """<!DOCTYPE html>
<html>
    <body a="&lt;b&gt;">
        &lt;Hello&gt;
    </body>
</html>"""

    def test_simple(self):
        doc = getDOMImplementation().createDocument(None, "html", None)
        body = doc.createElement("body")
        body.setAttribute("a","<b>")
        doc.documentElement.appendChild(body)
        txt = doc.createTextNode("<Hello>")
        body.appendChild(txt)
        exporter = Html5Exporter()
        html = exporter.export(doc)
        self.assertEqual(html.strip(),BasicTest.simple_expected.strip())


if __name__ == '__main__':
    unittest.main()