import string
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

def tally_file(params):
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

    
    return modes[params["mode"]](file_contents, params["offsets"], grouping) + params['offsets'].get("SALT", 0)

alpha_dict = {c: ord(c) - ord('a') + 1 for c in string.ascii_lowercase}
alpha_dict.update({str(i): i for i in range(10)})

ascii_dict = {c: ord(c) for c in string.printable}

def max_terms_dp(target, val_map):
    items = list(val_map.items())  # list of (key, value) pairs

    dp = [-float('inf')] * (target + 1)
    dp[0] = 0
    parent = [None] * (target + 1)

    for i in range(1, target + 1):
        for k, v in items:
            if v <= i and dp[i - v] + 1 > dp[i]:
                dp[i] = dp[i - v] + 1
                parent[i] = (k, v)

    if dp[target] < 0:
        return None

    result = []
    while target > 0:
        k, v = parent[target]
        result.append(k)
        target -= v
    return result

def tally_alpha(target, offsets):
    pass

def tally_ascii(target, offsets):
    pass

def create_tally(params):
    if (
        "offsets" not in params
        or any(not isinstance(c, int) for c in params["offsets"].values())
        or "mode" not in params
        or params["mode"] not in modes
        or "target" not in params
        or not isinstance(params["target"], int)
    ):
        print("Invalid parameters.")
        return
    
    