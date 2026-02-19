# tally-ho
Have you ever wanted to count the value of the contents of your files?  No? Well now you can!

# DOCUMENTATION:
Just call count_file with the following parameter:
count_file({
  "mode": "ascii" or "alpha" (SEE BELOW),
  "path": FILEPATH,
  "offsets": {SEE BELOW},
  (optionally) "grouping": True/False
})

MODES:
"ascii" mode will count every character in your file and aggregate it as its ASCII value
"alpha" mode will count every alphanumeric character in your file and aggregate it based on its numerical value or position in the alphabet.
    optionally, you can pass in True for "grouping" and numbers will be treated as their whole, whereas passing in False, numbers will be treated individually. (eg. 123 vs. [1, 2, 3]) (only applies to alpha mode)

OFFSETS:
offsets are a required parameter that is passed as a dictionary. For every key (string) in the dictionary, when it is encountered in the counting process, it will have its value (integer) applied onto it in addition to its counted value. (eg. {"a": 5} in alpha mode will result in a being worth 6 instead of 1)
    offsets ARE case-sensitive in ascii mode but NOT case-sensitive in alpha mode
    if an offset is applied in addition to the grouping option in alpha mode, the offset will only apply to the whole number (eg. {"1": 5} will only apply to an individual 1 and not 123
    the "ALL" key can be used to apply an offset to every single character
    the "OTHERWISE" key can be used to apply an offset to any character that is not defined an offset
