# JSON翻訳レポジトリ

このリポジトリは、複数の言語にJSONファイルを翻訳し、TypeScript（`.tsx`）ファイルとして出力するためのフレームワークを提供します。Google翻訳APIを使用して翻訳が管理され、プロセスを自動化するためのさまざまなスクリプトが用意されています。


## 使い方

### tsxファイルを生成または更新する場合

1. **翻訳対象のJSONファイルを指定**: 
   まず、翻訳したいJSONファイルを`main_add_json.py`内で指定します。例えば、`jsons/pages/Index.json`というファイルを翻訳したい場合、以下のように`input_file`としてこのファイルパスを設定します。

   ```python
   input_file = "jsons/pages/Index.json"  # 翻訳対象のjsonファイルを指定
   ```

2. **翻訳対象言語を選択**: 
   次に、翻訳したい言語をリストとして指定します。全言語を一度に翻訳することも可能です。

   ```python
   target_languages = ['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'ny', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']
   ```

3. **翻訳の実行**: 
   設定が終わったら、Pythonスクリプトを実行して翻訳を開始します。以下のコマンドを使用してください。

   ```bash
   python main_add_json.py
   ```

   **注意**: 翻訳が失敗する場合があります。コマンドライン出力を確認し、失敗した言語のみを指定して再実行することを推奨します。その場合、`target_languages`リストを修正し、特定の言語を選んで再度実行してください。

4. **Makefileによる修正の実行**: 
   自動生成された翻訳ファイルに不具合がある場合、Makefileを使用して修正を行うことができます。`fix_translate_to_multi_bbs`ターゲットを実行すると、以下の操作が行われます。

   - `translate/en/`フォルダから`translate/original/`へファイルをコピーし、ファイル名を`_original.tsx`に変更します。
   - `translate`ディレクトリ内で`ZH-CN`を`ZH_CN`に、`ZH-TW`を`ZH_TW`に置換します。

   **Makefileの実行例**:
   ```bash
   make fix_translate_to_multi_bbs
   ```

   このコマンドを実行することで、自動生成されたファイルに対して必要な修正を適用できます。


---

## プロジェクト構成

```
.
├── Makefile
├── create_lang_list.py
├── jsons
│   ├── components
│   └── pages
├── main_add_json.py
├── main_add_lang.py
├── requirements.txt
├── translate
│   ├── af
│   ├── am
│   ├── ar
│   ├── az
│   ├── ...
└── ...
```

## 概要

このリポジトリには、JSONファイルを自動的に翻訳し、`translate/`ディレクトリに翻訳結果を保存するためのスクリプトが含まれています。言語ごとにフォルダが整理され、対応する言語コードを使用して翻訳が管理されます。

### 主なファイル:
- **`create_lang_list.py`**: 翻訳タスクで使用する言語コードと対応する言語名のリストを生成します。
- **`main_add_json.py`**: 複数の言語にJSONファイルを翻訳するためのメインスクリプト。このスクリプトは、`translate/`ディレクトリに翻訳されたTypeScript（`.tsx`）ファイルを生成します。
- **`main_add_lang.py`**: 特定の言語セットに対して、よりカスタマイズ可能な翻訳処理を提供するスクリプトです。
- **`Makefile`**: 翻訳の自動生成後に修正を加えるためのターゲットが含まれています。生成されたファイルに不具合がある場合、このMakefileを使用して修正します。

## 主なスクリプト

### `main_add_json.py`

このスクリプトは、`jsons/`ディレクトリからJSONファイルを読み込み、Google翻訳APIを使用して複数の言語に翻訳し、対応する言語ディレクトリ内の`.tsx`ファイルとして出力します。

**主な機能:**
- `input_file`を自動検出し、そこから`output_folder`、`output_file_name`、`sub_directory`を導き出します。
- 各言語ごとに`.tsx`ファイルを生成します。
- 出力ファイルは、`translate/{language_code}/{sub_directory}/{file_name}_{language_code}.tsx`の形式で保存されます。

### `create_lang_list.py`

このスクリプトは、サポートされている言語と対応する言語コードのリストを生成し、他の翻訳タスクで使用されます。

例:
```python
langs = [
  { "code": "af", "language": "afrikaans", "languageCapitalized": "Afrikaans" },
  { "code": "sq", "language": "albanian", "languageCapitalized": "Albanian" },
  ...
]
```

### `main_add_lang.py`

このスクリプトは、個別の言語に対する柔軟な翻訳プロセスを提供します。複数のJSONファイルを検出し、それらを指定した言語に翻訳します。
基本使うことはないと思います。

## Makefile

このリポジトリには、自動生成された翻訳ファイルに対して修正を加えるためのMakefileが含まれています。特に、`fix_translate_to_multi_bbs`というターゲットを使用して、以下のような修正を行います。

**`fix_translate_to_multi_bbs`の機能:**
1. **`prepare-original`**: `translate/en`フォルダの内容を`translate/original`フォルダにコピーし、ファイル名を`_original.tsx`に置換します。
2. **`replace-zh-cn`**: `translate`ディレクトリ内の`ZH-CN`を`ZH_CN`に置換します。
3. **`replace-zh-tw`**: `translate`ディレクトリ内の`ZH-TW`を`ZH_TW`に置換します。

これにより、自動生成されたファイルのうまくいかない部分を修正することができます。
