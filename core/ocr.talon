# Select full OCR results.
screen line <user.scrambler_word>: user.ocr_select_full_result_by_word(scrambler_word)

# Select using scrambler modifiers.
# TODO: Use captures for the different object expansion types.
screen sentence <user.scrambler_word>: user.ocr_select_by_word(scrambler_word, "SENTENCE")
screen argument <user.scrambler_word>: user.ocr_select_by_word(scrambler_word, "ARGUMENT")
screen dubstring <user.scrambler_word>: user.ocr_select_by_word(scrambler_word, "STRING", "\"")
screen string <user.scrambler_word>: user.ocr_select_by_word(scrambler_word, "STRING", "'")
screen graves <user.scrambler_word>: user.ocr_select_by_word(scrambler_word, "STRING", "`")
screen whitespace <user.scrambler_word>: user.ocr_select_by_word(scrambler_word, "BETWEEN_WHITESPACE")
screen brackets <user.scrambler_word>: user.ocr_select_by_word(scrambler_word, "BRACKETS")
screen invoke <user.scrambler_word>: user.ocr_select_by_word(scrambler_word, "CALL")
