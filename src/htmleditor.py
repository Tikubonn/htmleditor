
import html
from io import TextIOBase, StringIO
from html.parser import HTMLParser
from typing import NamedTuple, ClassVar, Callable
from dataclasses import dataclass

"""HTML編集を行うための機能を提供します。"""

@dataclass
class HTMLWriter:

  """設定したオブジェクトにHTMLコードを書き込むための機能を提供します。

  Attributes
  ----------
  text_io : TextIOBase
    書き込み先のオブジェクトです。
  """

  text_io:TextIOBase

  def put_start_tag (self, tag:str, attrs:list[tuple[str, str]]|dict[str, str]):

    """設定された `TextIOBase` にHTML開始タグを書き込みます。

    Notes
    -----
    引数 `attrs` で指定された属性値は `html.escape` 関数により適切にエスケープ処理されます。

    Parameters
    ----------
    tag : str
      書き込まれる開始タグ名です。
    attrs : list[tuple[str, str]]|dict[str, str]
      タグに設定される属性の集合です。
      属性名・値の組のリストあるいは辞書を指定することができます。
    """

    attrs_dict = dict(attrs)
    self.text_io.write("<{:s}".format(tag))
    for key, value in sorted(list(attrs_dict.items())):
      self.text_io.write(" {:s}=\"{:s}\"".format(key, html.escape(value)))
    self.text_io.write(">")

  def put_end_tag (self, tag:str):

    """設定された `TextIOBase` にHTML終了タグを書き込みます。

    Parameters
    ----------
    tag : str
      書き込まれる終了タグ名です。
    """

    self.text_io.write("</{:s}>".format(tag))

  def put_data (self, data:str):

    """設定された `TextIOBase` にテキストを書き込みます。

    Notes
    -----
    引数 `data` で指定されたテキストは `html.escape` 関数により適切にエスケープ処理されます。

    Parameters
    ----------
    data : str
      書き込まれるテキストです。
    """

    self.text_io.write(html.escape(data))

  def put_html (self, data:str):

    """設定された `TextIOBase` に生のHTMLコードを書き込みます。

    Parameters
    ----------
    data : str
      書き込まれる生のHTMLコードです。
    """

    self.text_io.write(data)

  def put_comment (self, data:str):

    """設定された `TextIOBase` にコメントを書き込みます。

    Notes
    -----
    引数 `data` で指定された文章は `html.escape` 関数により適切にエスケープ処理されます。

    Parameters
    ----------
    data : str
      書き込まれるコメント文章です。
    """

    self.text_io.write("<!--{:s}-->".format(html.escape(data)))

  def put_decl (self, decl:str):

    """設定された `TextIOBase` にHTML宣言を書き込みます。

    Parameters
    ----------
    decl : str
      書き込まれるHTML宣言文です。
    """

    self.text_io.write("<!{:s}>".format(decl))

class Element (NamedTuple):

  """単独のHTML要素を表すクラスです。

  Attributes
  ----------
  tag : str
    HTML要素の要素名です。
  attrs : dict[str, str]
    HTML要素の属性の集合です。
  """

  tag:str
  attrs:dict[str, str]

class _HTMLEditor (HTMLParser):

  VOID_ELEMENT_TAGS:ClassVar[set[str]] = {
    "area", "base", "br", "col", "embed", 
    "hr", "img", "input", "link", "meta", 
    "param", "source", "track", "wbr",
  }

  def __init__ (
    self,
    *,
    start_tag_handler:Callable[[str, dict[str, str], bool, HTMLWriter, list[Element]], None]|None=None,
    end_tag_handler:Callable[[str, HTMLWriter, list[Element]], None]|None=None,
    data_handler:Callable[[str, HTMLWriter, list[Element]], None]|None=None,
    comment_handler:Callable[[str, HTMLWriter, list[Element]], None]|None=None,
    decl_handler:Callable[[str, HTMLWriter, list[Element]], None]|None=None):
    super().__init__()
    self.start_tag_handler = start_tag_handler
    self.end_tag_handler = end_tag_handler
    self.data_handler = data_handler
    self.comment_handler = comment_handler
    self.decl_handler = decl_handler
    self._buffer = StringIO()
    self._element_stack = []

  def __enter__ (self):
    return self

  def __exit__ (self, exc_type, exc_value, traceback):
    self.close()

  def result (self) -> str:
    return self._buffer.getvalue()

  def handle_starttag (self, tag:str, attrs:list[tuple[str, str]]):
    attrs_dict = dict(attrs)
    element = Element(tag, attrs_dict)
    self._element_stack.append(element)
    writer = HTMLWriter(self._buffer)
    if self.start_tag_handler:
      self.start_tag_handler(tag, attrs_dict, tag in self.VOID_ELEMENT_TAGS, writer, self._element_stack)
    else:
      writer.put_start_tag(tag, attrs_dict)
    if tag in self.VOID_ELEMENT_TAGS:
      self._element_stack.pop()

  def handle_endtag (self, tag:str):
    writer = HTMLWriter(self._buffer)
    if self.end_tag_handler:
      self.end_tag_handler(tag, writer, self._element_stack)
    else:
      writer.put_end_tag(tag)
    self._element_stack.pop()

  def handle_data (self, data:str):
    writer = HTMLWriter(self._buffer)
    if self.data_handler:
      self.data_handler(data, writer, self._element_stack)
    else:
      writer.put_data(data)

  def handle_comment (self, data:str):
    writer = HTMLWriter(self._buffer)
    if self.comment_handler:
      self.comment_handler(data, writer, self._element_stack)
    else:
      writer.put_comment(data)

  def handle_decl (self, decl:str):
    writer = HTMLWriter(self._buffer)
    if self.decl_handler:
      self.decl_handler(decl, writer, self._element_stack)
    else:
      writer.put_decl(decl)

  def close (self):
    self._buffer.close()
    super().close()

def html_edit (
  source:str,
  *,
  start_tag_handler:Callable[[str, dict[str, str], bool, HTMLWriter, list[Element]], None]|None=None,
  end_tag_handler:Callable[[str, HTMLWriter, list[Element]], None]|None=None,
  data_handler:Callable[[str, HTMLWriter, list[Element]], None]|None=None,
  comment_handler:Callable[[str, HTMLWriter, list[Element]], None]|None=None,
  decl_handler:Callable[[str, HTMLWriter, list[Element]], None]|None=None):

  """設定された各種コールバック関数を用いてHTML文書を編集します。

  Examples
  --------
  >>> import htmleditor
  >>> 
  >>> def data_handler (data, writer, element_stack):
  >>>   writer.put_data(data.upper())
  >>> 
  >>> htmleditor.html_edit("<p>Hello.</p>", data_handler=data_handler)
  <p>HELLO.</p>

  Parameters
  ----------
  source : str
    編集元となるHTML文書です。
  start_tag_handler : Callable[[str, dict[str, str], bool, HTMLWriter, list[Element]], None]|None
    開始タグを発見したときに実行されるコールバック関数です。
    未指定ならば `None` が設定されます。
  end_tag_handler : Callable[[str, HTMLWriter, list[Element]], None]|None
    終了タグを発見したときに実行されるコールバック関数です。
    未指定ならば `None` が設定されます。
  data_handler : Callable[[str, HTMLWriter, list[Element]], None]|None
    テキストを発見したときに実行されるコールバック関数です。
    これはインデント等の空白文字だけの部分にも反応して呼び出されます。
    未指定ならば `None` が設定されます。
  comment_handler : Callable[[str, HTMLWriter, list[Element]], None]|None
    コメントを発見したときに実行されるコールバック関数です。
    未指定ならば `None` が設定されます。
  decl_handler : Callable[[str, HTMLWriter, list[Element]], None]|None
    HTML宣言を発見したときに実行されるコールバック関数です。
    未指定ならば `None` が設定されます。

  Returns
  -------
  str
    編集されたHTML文書を返します。
  """

  with _HTMLEditor(
    start_tag_handler=start_tag_handler,
    end_tag_handler=end_tag_handler,
    data_handler=data_handler,
    comment_handler=comment_handler,
    decl_handler=decl_handler) as editor:
    editor.feed(source)
    return editor.result()
