from MorphPieceWPE import MorphPieceWPE

tokenizer = MorphPieceWPE()

text = "He is an internationally acclaimed celebrity"
tokens = tokenizer(text)
# print(tokenizer.decode(tokens['input_ids'],skip_special_tokens=False))
print(tokenizer.convert_ids_to_tokens(tokens['input_ids']))
print(tokens['input_ids'])