
# htmleditor

## Overview

![](https://img.shields.io/badge/Python-3.12-blue)
![](https://img.shields.io/badge/License-AGPLv3-blue)

コールバック関数を用いてHTML文書を編集する関数を提供します。

`html.parser.HTMLParser` によるHTML文書の編集は、処理毎に派生クラスの定義を行わなければならず、また、処理を行わない場合の関数も毎回定義する必要がありました。
本パッケージが提供する `htmleditor.html_edit` 関数はそれらの面倒な手間を極力排除し、必要なコールバック関数の指定だけでHTML文書の編集を行います。

## Usage

`htmleditor.html_edit` 関数を使用して `class` 属性が一致した要素のテキストだけを大文字に変換する実行例です。

```py
import htmleditor

SOURCE = """
<html>
  <head></head>
  <body>
    <ul>
      <li>First</li>
      <li class="upper">Second</li>
      <li>Third</li>
    </ul>
  </body>
</html>
"""

def data_handler (data:str, writer:htmleditor.HTMLWriter, element_stack:list[htmleditor.Element]):
  if element_stack and element_stack[-1].attrs.get("class", "") == "upper":
    writer.put_data(data.upper())
  else:
    writer.put_data(data)

htmleditor.html_edit(SOURCE, data_handler=data_handler)
```

```txt
<html>
  <head></head>
  <body>
    <ul>
      <li>First</li>
      <li class="upper">SECOND</li>
      <li>Third</li>
    </ul>
  </body>
</html>
```

## Install

```shell
pip install .
```

### Test

```shell
pip install .[test]
pytest .
```

### Document

```py
import htmleditor

help(htmleditor)
```

## Donation

<a href="https://buymeacoffee.com/tikubonn" target="_blank"><img src="doc/img/qr-code.png" width="3000px" height="3000px" style="width:150px;height:auto;"></a>

もし本パッケージがお役立ちになりましたら、少額の寄付で支援することができます。<br>
寄付していただいたお金は書籍の購入費用や日々の支払いに使わせていただきます。
ただし、これは寄付の多寡によって継続的な開発やサポートを保証するものではありません。ご留意ください。

If you found this package useful, you can support it with a small donation.
Donations will be used to cover book purchases and daily expenses.
However, please note that this does not guarantee ongoing development or support based on the amount donated.

## License

© 2025 tikubonn

htmleditor licensed under the [AGPLv3](./LICENSE).
