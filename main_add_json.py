# from googletrans import Translator
# import json

# def translate_text(text, target_language):
#     translator = Translator()
#     translation = translator.translate(text, dest=target_language)
#     return translation.text

# def translate_dict(data, target_language):
#     translated_data = {}
#     for key, value in data.items():
#         if isinstance(value, dict):
#             translated_data[key] = translate_dict(value, target_language)
#         else:
#             translated_data[key] = translate_text(str(value), target_language)  # str()を使用して文字列に変換

#     return translated_data

# def translate_file(input_file, output_file, target_language):
#     with open(input_file, 'r', encoding='utf-8') as file:
#         data = json.load(file)

#     translated_data = translate_dict(data, target_language)

#     # TypeScriptオブジェクトの形式に整形
#     output_data = "const Test = " + json.dumps(translated_data, ensure_ascii=False, indent=2)

#     with open(output_file, 'w', encoding='utf-8') as file:
#         file.write(output_data)

# if __name__ == "__main__":
#     input_file = "input.json"
#     output_file = "output_en.tsx"
#     target_language = "en"

#     translate_file(input_file, output_file, target_language)





from googletrans import Translator
import json
import os
import time

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# def translate_dict(data, target_languages):
#     translated_data = {}
#     for target_language in target_languages:
#         translated_data[target_language] = {}
#         for key, value in data.items():
#             if isinstance(value, dict):
#                 translated_data[target_language][key] = translate_dict(value, [target_language])
#             elif isinstance(value, list):
#                 # print("value: ")
#                 # print(value)
#                 translated_data[target_language][key] = [translate_text(str(item), target_language) for item in value]

#                 # # 新しいリストを作成して翻訳済みのデータを格納
#                 # translated_values = []
#                 # for item in value:
#                 #     # print(str(item))
#                 #     translated_value = translate_text(str(item), target_language)
#                 #     # print(translated_value)

#                 #     translated_values.append(translated_value)

#                 # # translated_data 辞書に新しいエントリを追加
#                 # if target_language not in translated_data:
#                 #     translated_data[target_language] = {}
#                 # translated_data[target_language][key] = translated_values

#             else:
#                 translated_data[target_language][key] = translate_text(str(value), target_language)
#         time.sleep(10)
#     return translated_data

def translate_dict(data, target_language):
    translated_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            translated_data[key] = translate_dict(value, target_language)
        elif isinstance(value, list):
            translated_data[key] = [translate_text(str(item), target_language) for item in value]
        else:
            translated_data[key] = translate_text(str(value), target_language)
    time.sleep(10)
    return translated_data



def create_language_folders(output_folder, target_languages, sub_directory):
    for lang in target_languages:
        folder_path = os.path.join(output_folder, lang, sub_directory)
        os.makedirs(folder_path, exist_ok=True)

def translate_file(input_file, output_folder, target_languages, output_file_name, sub_directory):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    create_language_folders(output_folder, target_languages, sub_directory)

    for target_language in target_languages:
        # translated_data = translate_dict(data, [target_language])
        translated_data = translate_dict(data, target_language)


        output_file = os.path.join(output_folder, target_language, sub_directory, output_file_name + "_" + target_language + ".tsx")
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("export const {} = ".format(output_file_name + "_" + target_language.upper()))
            # json.dump(translated_data[target_language], file, ensure_ascii=False, indent=2)
            json.dump(translated_data, file, ensure_ascii=False, indent=2)

            file.write("\n\n" + "export default {}".format(output_file_name + "_" + target_language.upper()))
            print("{} is translated.".format(target_language))

if __name__ == "__main__":
    input_file = "jsons/pages/Index.json"
    output_file_name = "Index"
    output_folder = "translate"
    sub_directory = "pages"

    # target_languages = ["en", "zh-cn", "es", "ar", "fr", "ja"]
    target_languages = ["af", "am", "fi", "sq", "tl"]

    translate_file(input_file, output_folder, target_languages, output_file_name, sub_directory)


