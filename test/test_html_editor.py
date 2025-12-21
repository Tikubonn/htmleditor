
import pytest
from htmleditor import HTMLWriter, _HTMLEditor

def test_html_editor ():
  with _HTMLEditor() as editor:
    editor.feed("<p>abc<img>def</p>")
    assert editor.result() == "<p>abc<img>def</p>"

def test_html_editor_start_tag ():

  cur_index = 0
  expect_args = [
    ("p", {}, False, [("p", {})]),
    ("img", {"src": "123"}, True, [("p", {}), ("img", {"src": "123"})]),
  ]

  def start_tag_handler (tag:str, attrs:dict[str, str], is_void:bool, writer:HTMLWriter, element_stack:list[tuple[str, dict[str, str]]]):
    nonlocal cur_index
    assert expect_args[cur_index] == (tag, attrs, is_void, element_stack)
    cur_index += 1

  with _HTMLEditor(start_tag_handler=start_tag_handler) as editor:
    editor.feed("<p>abc<img src=\"123\">def</p>")
    assert editor.result() == "abcdef</p>"

def test_html_editor_end_tag ():

  cur_index = 0
  expect_args = [
    ("p", [("p", {})]),
  ]

  def end_tag_handler (tag:str, writer:HTMLWriter, element_stack:list[tuple[str, dict[str, str]]]):
    nonlocal cur_index
    assert expect_args[cur_index] == (tag, element_stack)
    cur_index += 1

  with _HTMLEditor(end_tag_handler=end_tag_handler) as editor:
    editor.feed("<p>abc<img src=\"123\">def</p>")
    assert editor.result() == "<p>abc<img src=\"123\">def"

def test_html_editor_data ():

  cur_index = 0
  expect_args = [
    ("abc", [("p", {})]),
    ("def", [("p", {})]),
  ]

  def data_handler (data:str, writer:HTMLWriter, element_stack:list[tuple[str, dict[str, str]]]):
    nonlocal cur_index
    assert expect_args[cur_index] == (data, element_stack)
    cur_index += 1

  with _HTMLEditor(data_handler=data_handler) as editor:
    editor.feed("<p>abc<img src=\"123\">def</p>")
    assert editor.result() == "<p><img src=\"123\"></p>"

def test_html_editor_comment ():

  cur_index = 0
  expect_args = [
    ("123", [("p", {})]),
  ]

  def comment_handler (data:str, writer:HTMLWriter, element_stack:list[tuple[str, dict[str, str]]]):
    nonlocal cur_index
    assert expect_args[cur_index] == (data, element_stack)
    cur_index += 1

  with _HTMLEditor(comment_handler=comment_handler) as editor:
    editor.feed("<p>abc<!--123-->def</p>")
    assert editor.result() == "<p>abcdef</p>"

def test_html_editor_decl ():

  cur_index = 0
  expect_args = [
    ("DOCTYPE html", []),
  ]

  def decl_handler (decl:str, writer:HTMLWriter, element_stack:list[tuple[str, dict[str, str]]]):
    nonlocal cur_index
    assert expect_args[cur_index] == (decl, element_stack)
    cur_index += 1

  with _HTMLEditor(decl_handler=decl_handler) as editor:
    editor.feed("<!DOCTYPE html><p>abc<img src=\"123\">def</p>")
    assert editor.result() == "<p>abc<img src=\"123\">def</p>"
