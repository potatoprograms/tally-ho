import string
import random
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

create_modes = {
    "alpha": alpha_dict,
    "ascii": ascii_dict
}


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

    val_map = create_modes[params["mode"]]
    
    # apply offsets to get effective values for each character
    effective = {}
    for k in val_map:
        effective_val = apply_offsets(k, val_map[k], params["offsets"])
        if effective_val > 0:
            effective[k] = effective_val

    if not effective:
        print("No usable characters after applying offsets")
        return None

    items = sorted(effective.items(), key=lambda x: x[1], reverse=True)
    min_val = min(v for _, v in items)
    max_val = max(v for _, v in items)
    target = params["target"]

    if "length" in params and isinstance(params["length"], int):
        n = params["length"]
        if target < n * min_val or target > n * max_val:
            print("Value is unreachable in the given number of terms")
            return None

        result = []
        remaining = target
        for step in range(n):
            terms_left = n - step
            lo = (terms_left - 1) * min_val
            hi = (terms_left - 1) * max_val
            valid = [(k, v) for k, v in items if lo <= remaining - v <= hi]
            k, v = random.choice(valid)
            result.append(k)
            remaining -= v

    else:
        result = []
        remaining = target
        while remaining > 0:
            valid = [(k, v) for k, v in items if v <= remaining]
            if not valid:
                print("Value is unreachable")
                return None
            weights = [v ** 2 for _, v in valid]
            k, v = random.choices(valid, weights=weights, k=1)[0]
            result.append(k)
            remaining -= v

    return ''.join(random.sample(result, len(result)))