from googletrans import Translator
import json
import os
import time

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def translate_dict(data, target_language):
    translated_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            translated_data[key] = translate_dict(value, target_language)
        elif isinstance(value, list):
            translated_data[key] = [translate_text(str(item), target_language) for item in value]
        else:
            translated_data[key] = translate_text(str(value), target_language)
    time.sleep(10)  # Google APIの使用制限を考慮してsleepを入れています
    return translated_data

def create_language_folders(output_folder, target_languages, sub_directory):
    for lang in target_languages:
        folder_path = os.path.join(output_folder, lang, sub_directory)
        os.makedirs(folder_path, exist_ok=True)

def translate_file(input_file, target_languages):
    # output_folderは固定で "translate" に設定
    output_folder = "translate"
    sub_directory = os.path.split(os.path.dirname(input_file))[1]  # input_fileのディレクトリ部分をサブディレクトリに設定
    output_file_name = os.path.splitext(os.path.basename(input_file))[0]  # input_fileのファイル名部分から拡張子を除去

    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    create_language_folders(output_folder, target_languages, sub_directory)

    for target_language in target_languages:
        translated_data = translate_dict(data, target_language)

        # 出力ファイルのパスを指定
        output_file = os.path.join(output_folder, target_language, sub_directory, output_file_name + "_" + target_language + ".tsx")
        
        # ファイルが存在するか確認し、存在すれば内容を更新、なければ新規作成
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as file:
                existing_data = file.read()

            # JSONの形式に適合するように既存データを修正
            try:
                existing_json = json.loads(existing_data.split("=", 1)[1].rsplit("\n", 2)[0].strip())
            except:
                existing_json = {}

            # 既存データを翻訳結果で上書き
            existing_json.update(translated_data)

            # 更新したデータを再度書き込む
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write("export const {} = ".format(output_file_name + "_" + target_language.upper()))
                json.dump(existing_json, file, ensure_ascii=False, indent=2)
                file.write("\n\nexport default {}".format(output_file_name + "_" + target_language.upper()))
                print(f"{output_file} has been updated with new translation.")
        else:
            # ファイルが存在しない場合は新規作成
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write("export const {} = ".format(output_file_name + "_" + target_language.upper()))
                json.dump(translated_data, file, ensure_ascii=False, indent=2)
                file.write("\n\nexport default {}".format(output_file_name + "_" + target_language.upper()))
                print(f"{output_file} has been created with new translation.")

if __name__ == "__main__":
    """
    jsonファイルを翻訳し、指定した言語のtsxファイルを生成します。
    """
    input_file = "jsons/pages/Index.json"
    
    # 翻訳対象言語
    # 全言語：target_languages = ['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'ny', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']
    target_languages = ['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'ny', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']


    # input_fileを指定するだけで他のパス関連は自動で設定されます
    translate_file(input_file, target_languages)
