import re

pronunciation = "uh-PRAY-zuhl"
special_chars = "–,-, ,_"

# Remove special characters except for space
# 文字列内の特殊文字を', 'に置き換えるための変換テーブルを作成します
trans = str.maketrans({char: "," for char in special_chars})

# 文字列内の特殊文字を', 'に置き換えます
output_str = pronunciation.translate(trans)

# Join the pronunciation list with ", "
print(output_str)