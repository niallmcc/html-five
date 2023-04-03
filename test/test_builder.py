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
from htmlfive import Html5Builder

expected = """<!DOCTYPE html>
<html>
    <head>
        <title>
            Title!
        </title>
    </head>
    <body>
        <h1 id="heading">
            Heading
        </h1>
        <br>
        <div>
            Lorem Ipsum
        </div>
    </body>
</html>"""

class BasicTest(unittest.TestCase):

    def test_simple(self):
        # round trip some simple HTML
        builder = Html5Builder()
        builder.head().add_element("title").add_text("Title!")
        builder.body().add_element("h1",{"id":"heading"}).add_text("Heading")
        builder.body().add_element("br")
        builder.body().add_element("div").add_text("Lorem Ipsum")
        self.assertEqual(builder.get_html(),expected)

if __name__ == '__main__':
    unittest.main()

