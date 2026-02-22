def apply_offsets(char, count, offsets):
    if char in offsets:
        count += offsets[char]
    elif "OTHERWISE" in offsets:
        count += offsets["OTHERWISE"]
    if "ALL" in offsets:
        count += offsets["ALL"]
    if "LETTER" in offsets and char.isalpha():
        count += offsets["LETTER"]
    elif "NUMBER" in offsets and char.isdigit():
        count += offsets["NUMBER"]
    elif "SYMBOL" in offsets and not char.isalpha() and not char.isdigit():
        count += offsets["SYMBOL"]

    return count
def ascii_count(s, offsets, **kwargs):
    cnt = 0
    for char in s:
        cnt += ord(char)
        cnt = apply_offsets(char, cnt, offsets)
        
    return cnt

def alphabet_count(s, offsets, grouping=False):
    cnt = 0
    s = s.lower()
    i = 0

    while i < len(s):
        char = s[i]

        if 'a' <= char <= 'z':
            cnt += ord(char) - ord('a') + 1

            cnt = apply_offsets(char, cnt, offsets)

            i += 1

        elif char.isdigit():
            if grouping:
                start = i
                while i < len(s) and s[i].isdigit():
                    i += 1

                number_value = int(s[start:i])
                cnt += number_value
                cnt = apply_offsets(str(number_value), cnt, offsets)

            else:
                cnt += int(char)

                cnt = apply_offsets(char, cnt, offsets)

                i += 1

        else:
            cnt = apply_offsets(char, cnt, offsets)

            i += 1

    return cnt

modes = {
    "ascii": ascii_count,
    "alpha": alphabet_count
}

def count_file(params):
    if (
        "path" not in params
        or "mode" not in params
        or "offsets" not in params
        or params["mode"] not in modes
        or any(not isinstance(c, int) for c in params["offsets"].values())
    ):
        print("Invalid parameters.")
        return

    with open(params["path"], 'r') as f:
        file_contents = f.read()

    grouping = params.get("grouping", False)

    print(
        modes[params["mode"]](file_contents, params["offsets"], grouping)
    )
