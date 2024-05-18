date insert:
  insert(user.time_format("%Y-%m-%d"))
timestamp insert:
  insert(user.time_format("%Y-%m-%d %H:%M:%S"))
timestamp insert high resolution:
  insert(user.time_format("%Y-%m-%d %H:%M:%S.%f"))

# Arbitrary time.
time insert <user.number_small> <user.number>: insert("{number_small}:{number}")
time insert <user.number_small> o clock: insert("{number_small}:00")

# Arbitrary date.
date insert <user.number> <user.number_small> <user.number_small>:
  insert(user.date_utc(number, number_small_1, number_small_2))

# Convert unix timestamps.
convert unix show: user.notify_selected_unix_to_datetime()
convert unix copy: user.clipboard_selected_unix_to_datetime()
