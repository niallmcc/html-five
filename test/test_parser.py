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

from htmlfive import Html5Parser

import unittest


class BasicTest(unittest.TestCase):

    def test_simple(self):
        parser = Html5Parser()
        doc = parser.parse("<!DOCTYPE html><html><body style='color:red;'><!--comment-->Hello World</body></html>")
        self.assertEqual(doc.documentElement.tagName,"html")
        self.assertEqual(len(doc.documentElement.childNodes), 1)
        self.assertEqual(doc.documentElement.childNodes[0].tagName, "body")
        self.assertEqual(doc.documentElement.childNodes[0].attributes.items(),[("style", "color:red;")])
        self.assertEqual(len(doc.documentElement.childNodes[0].childNodes), 2)
        self.assertEqual(doc.documentElement.childNodes[0].childNodes[0].data, "comment")
        self.assertEqual(doc.documentElement.childNodes[0].childNodes[1].data, "Hello World")

    def test_escape(self):
        parser = Html5Parser()
        doc = parser.parse("<!DOCTYPE html><html><body class=\"&lt;&amp;&gt;\">&lt;Hello World&gt;</body></html>")
        self.assertEqual(len(doc.documentElement.childNodes), 1)
        self.assertEqual(doc.documentElement.childNodes[0].attributes.items(),[("class", "<&>")])
        self.assertEqual(doc.documentElement.childNodes[0].childNodes[0].data, "<Hello World>")
