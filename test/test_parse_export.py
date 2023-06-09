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
from htmlfive.html5_exporter import Html5Exporter

simple_test_html=\
"""<!DOCTYPE html>
<html>
    <head a="a" b="b" c>
        <title>
            Title!
        </title>
    </head>
    <body>
        <br>
        <h1 class="heading" a='"hello"' b="こんにちは" c="&lt;&gt;">
            Hello
            こんにちは
        </h1>
        <input type="text" id="text_input">
    </body>
</html>"""

class BasicTest(unittest.TestCase):

    def test_simple(self):
        # round trip some simple HTML
        parser = Html5Parser()
        dom = parser.parse(simple_test_html)
        exporter = Html5Exporter()
        expected = simple_test_html
        self.assertEqual(exporter.export(dom).strip(),expected.strip())

    def test_no_doctype(self):
        # same as simple test but without DOCTYPE
        parser = Html5Parser()
        dom = parser.parse(simple_test_html.replace("<!DOCTYPE html>",""))
        exporter = Html5Exporter()
        expected = simple_test_html
        self.assertEqual(exporter.export(dom).strip(), expected.strip())

if __name__ == '__main__':
    unittest.main()