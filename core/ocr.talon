# Select full OCR results.
screen line <user.textflow_word>: user.ocr_select_full_result_by_word(textflow_word)
screen line <user.textflow_word> <user.textflow_target_combo_type> <user.textflow_word>:
  user.ocr_select_full_result_by_word_range(textflow_word_1, textflow_word_2, textflow_target_combo_type)

# Select using textflow modifiers.
screen sentence <user.textflow_word>: user.ocr_select_by_word(textflow_word, "SENTENCE")
screen argument <user.textflow_word>: user.ocr_select_by_word(textflow_word, "ARGUMENT")
screen doubles <user.textflow_word>: user.ocr_select_by_word(textflow_word, "STRING", "\"")
screen singles <user.textflow_word>: user.ocr_select_by_word(textflow_word, "STRING", "'")
screen graves <user.textflow_word>: user.ocr_select_by_word(textflow_word, "STRING", "`")
screen whitespace <user.textflow_word>: user.ocr_select_by_word(textflow_word, "BETWEEN_WHITESPACE")
screen brackets <user.textflow_word>: user.ocr_select_by_word(textflow_word, "BRACKETS")
screen invoke <user.textflow_word>: user.ocr_select_by_word(textflow_word, "CALL")

# Select a range in the text using textflow modifiers.
screen sentence <user.textflow_word> <user.textflow_target_combo_type> <user.textflow_word>:
  user.ocr_select_by_word_range(textflow_word_1, textflow_word_2, textflow_target_combo_type, "SENTENCE")
screen whitespace <user.textflow_word>  <user.textflow_target_combo_type> <user.textflow_word>:
  user.ocr_select_by_word_range(textflow_word_1, textflow_word_2, textflow_target_combo_type, "BETWEEN_WHITESPACE")
