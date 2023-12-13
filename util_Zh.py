import re
# ### functions particularly for Chinese ###

# # for chinese text sequence, with `jieba` for tokenization
# def tokenize_chinese(text):
#     # Use jieba to tokenize Chinese text into words
#     return list(jieba.cut(text))

# # convert all characters in the text sequence to full-width
# def to_full_width(text):
#     #print("converting all characters in the text sequence to full-width ... ")
#     full_width_text = ""
#     for char in text:
#         if unicodedata.east_asian_width(char) == 'Na':
#             num = ord(char)

#             # Convert to full-width if it's a half-width Katakana, full-width form is 0xFEE0 more than half-width
#             if 0xFF61 <= num <= 0xFF9F:
#                 full_width_char = chr(num + 0xFEE0)
#             # For other half-width characters such as ASCII
#             elif 0x0021 <= num <= 0x007E:
#                 full_width_char = chr(num + 0xfee0)
#             else:
#                 full_width_char = char
#             full_width_text += full_width_char
#         else:
#             full_width_text += char
#     return full_width_text

# replace all Chinese punctuations in a Chinese text with spaces (half-width)
def replace_punt(chinese_text):
    # replace all Chinese punctuations in a Chinese text with spaces (half-width), 
    # no need Chinese space(full-width). In 'len' function, it'll be count as 1 no matter half or full width.

    chinese_punctuations = ["，","。","、","；","：","？","！","“","”","‘","’","（","）","【","】","《","》",
                            "——","……","·","「","」","『","』","〈","〉",
                            ",", "?", "!","..."]
    for punct in chinese_punctuations:
        chinese_text = chinese_text.replace(punct, ' ')

    return chinese_text


def replace_space(chinese_text):
    # replace all space in Chinese with '。'

    chinese_text = '。'.join([t.strip() for t in chinese_text.split()])

    # deduplicate end of sentence 收魂器。。还有其他句号。=> 收魂器。还有其他句号。
    deduplicated_text = re.sub(r'([。]){2,}', r'\1', chinese_text)

    return deduplicated_text

