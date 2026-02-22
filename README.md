# tally-ho
Have you ever wanted to count the value of the contents of your files?  No? Well now you can!


Call the function like this:

count_file({  
    "mode": "ascii" or "alpha",  # see Modes  
    "path": FILEPATH,  
    "offsets": { ... },          # see Offsets  
    "grouping": True/False       # optional, alpha mode only  
})  



## Modes:

### ascii
    Counts every character in the file using its ASCII value.
    - Offsets are case-sensitive.

### alpha
    Counts letters based on their position in the alphabet (a=1, b=2, ..., z=26)
    and digits as their numeric value.
    - Letters are case-insensitive.
    - Optional grouping=True: consecutive digits are treated as a single number
      (e.g., 123 counts as 123).
    - Optional grouping=False: digits are counted individually
      (e.g., 123 counts as [1, 2, 3]).



## Offsets:

- Required dictionary parameter.
- Each key represents a character or number string.
  Its value (integer) is added to the counted value.
  - Example: {"a": 5} in alpha mode → a = 1 + 5 = 6.

### Special keys:
- ALL: applies the offset to every character.
- OTHERWISE: applies the offset to any character not explicitly defined.

### Notes:
- In alpha mode with grouping=True, offsets apply only to the whole number,
  not to individual digits.
- ASCII mode offsets are case-sensitive; alpha mode offsets are case-insensitive.
