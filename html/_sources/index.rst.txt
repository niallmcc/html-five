.. unearth documentation master file, created by
   sphinx-quickstart on Thurs Jan 2 09:34:27 2020
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

html-five
=========

html-five is a set of pure-python simple utilities for working with HTML5 utilities.
It is not recommended for production/operational use.

Html5Parser
===========

.. autoclass:: htmlfive.Html5Parser

.. automethod:: htmlfive.Html5Parser.parse

Html5Exporter
=============

.. autoclass:: htmlfive.Html5Exporter

.. automethod:: htmlfive.Html5Exporter.export

Html5Formatter
==============

.. autoclass:: htmlfive.Html5Formatter

   which, when rendered in an HTML document, looks like:

.. raw:: html

   <pre><code>
   &lt;!DOCTYPE html&gt;
   &lt;<span style="color:red;">html</span>&gt;
       &lt;<span style="color:red;">body</span> <span style="color:blue;">attrname</span>=<span style="color:purple;">"attrvalue"</span>&gt;
           Hello
       &lt;/<span style="color:red;">body</span>&gt;
   &lt;/<span style="color:red;">html</span>&gt;
   </code></pre>

.. automethod:: htmlfive.Html5Formatter.format

Html5Builder
============

.. autoclass:: htmlfive.Html5Builder

.. automethod:: htmlfive.Html5Builder.head

.. automethod:: htmlfive.Html5Builder.body

.. automethod:: htmlfive.Html5Builder.get_html

.. automethod:: htmlfive.html5_builder.ElementFragment.add_element

.. automethod:: htmlfive.html5_builder.ElementFragment.add_text

