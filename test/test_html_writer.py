
import pytest
from io import StringIO
from htmleditor import HTMLWriter

def test_html_writer_put_start_tag ():

  with StringIO() as buffer:
    writer = HTMLWriter(buffer)
    writer.put_start_tag("a", {})
    assert buffer.getvalue() == "<a>"

  with StringIO() as buffer:
    writer = HTMLWriter(buffer)
    writer.put_start_tag("a", {"abc": "def"})
    assert buffer.getvalue() == "<a abc=\"def\">"

  with StringIO() as buffer:
    writer = HTMLWriter(buffer)
    writer.put_start_tag("a", {"abc": "<def>"})
    assert buffer.getvalue() == "<a abc=\"&lt;def&gt;\">"

def test_html_writer_put_end_tag ():

  with StringIO() as buffer:
    writer = HTMLWriter(buffer)
    writer.put_end_tag("a")
    assert buffer.getvalue() == "</a>"

def test_html_writer_put_data ():

  with StringIO() as buffer:
    writer = HTMLWriter(buffer)
    writer.put_data("abc")
    assert buffer.getvalue() == "abc"

  with StringIO() as buffer:
    writer = HTMLWriter(buffer)
    writer.put_data("<abc>")
    assert buffer.getvalue() == "&lt;abc&gt;"

def test_html_writer_put_html ():

  with StringIO() as buffer:
    writer = HTMLWriter(buffer)
    writer.put_html("abc")
    assert buffer.getvalue() == "abc"

  with StringIO() as buffer:
    writer = HTMLWriter(buffer)
    writer.put_html("<abc>")
    assert buffer.getvalue() == "<abc>"

def test_html_writer_put_comment ():

  with StringIO() as buffer:
    writer = HTMLWriter(buffer)
    writer.put_comment("abc")
    assert buffer.getvalue() == "<!--abc-->"

  with StringIO() as buffer:
    writer = HTMLWriter(buffer)
    writer.put_comment("<abc>")
    assert buffer.getvalue() == "<!--&lt;abc&gt;-->"

def test_html_writer_put_decl ():

  with StringIO() as buffer:
    writer = HTMLWriter(buffer)
    writer.put_decl("DOCTYPE html")
    assert buffer.getvalue() == "<!DOCTYPE html>"
