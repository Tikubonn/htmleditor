
import pytest
import htmleditor

def test_html_edit ():
  assert htmleditor.html_edit("<p>abc<img src=\"123\">def</p>") == "<p>abc<img src=\"123\">def</p>"

def test_html_edit_start_tag ():

  cur_index = 0
  expect_args = [
    ("p", {}, False, [("p", {})]),
    ("img", {"src": "123"}, True, [("p", {}), ("img", {"src": "123"})]),
  ]

  def start_tag_handler (tag:str, attrs:dict[str, str], is_void:bool, writer:htmleditor.HTMLWriter, element_stack:list[tuple[str, dict[str, str]]]):
    nonlocal cur_index
    assert expect_args[cur_index] == (tag, attrs, is_void, element_stack)
    cur_index += 1

  assert htmleditor.html_edit("<p>abc<img src=\"123\">def</p>", start_tag_handler=start_tag_handler) == "abcdef</p>"

def test_html_edit_end_tag ():

  cur_index = 0
  expect_args = [
    ("p", [("p", {})]),
  ]

  def end_tag_handler (tag:str, writer:htmleditor.HTMLWriter, element_stack:list[tuple[str, dict[str, str]]]):
    nonlocal cur_index
    assert expect_args[cur_index] == (tag, element_stack)
    cur_index += 1

  assert htmleditor.html_edit("<p>abc<img src=\"123\">def</p>", end_tag_handler=end_tag_handler) == "<p>abc<img src=\"123\">def"

def test_html_edit_data ():

  cur_index = 0
  expect_args = [
    ("abc", [("p", {})]),
    ("def", [("p", {})]),
  ]

  def data_handler (data:str, writer:htmleditor.HTMLWriter, element_stack:list[tuple[str, dict[str, str]]]):
    nonlocal cur_index
    assert expect_args[cur_index] == (data, element_stack)
    cur_index += 1

  assert htmleditor.html_edit("<p>abc<img src=\"123\">def</p>", data_handler=data_handler) == "<p><img src=\"123\"></p>"

def test_html_edit_comment ():

  cur_index = 0
  expect_args = [
    ("123", [("p", {})]),
  ]

  def comment_handler (data:str, writer:htmleditor.HTMLWriter, element_stack:list[tuple[str, dict[str, str]]]):
    nonlocal cur_index
    assert expect_args[cur_index] == (data, element_stack)
    cur_index += 1

  assert htmleditor.html_edit("<p>abc<!--123-->def</p>", comment_handler=comment_handler) == "<p>abcdef</p>"

def test_html_edit_decl ():

  cur_index = 0
  expect_args = [
    ("DOCTYPE html", []),
  ]

  def decl_handler (data:str, writer:htmleditor.HTMLWriter, element_stack:list[tuple[str, dict[str, str]]]):
    nonlocal cur_index
    assert expect_args[cur_index] == (data, element_stack)
    cur_index += 1

  assert htmleditor.html_edit("<!DOCTYPE html><p>abc<img src=\"123\">def</p>", decl_handler=decl_handler) == "<p>abc<img src=\"123\">def</p>"
