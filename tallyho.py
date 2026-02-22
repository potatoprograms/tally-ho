import string
from random import sample
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

def max_terms_dp(target, val_map):
    items = list(val_map.items())

    dp = [-float('inf')] * (target + 1)
    dp[0] = 0
    parent = [None] * (target + 1)

    for k, v in items:
        for i in range(target, v - 1, -1):
            if dp[i - v] + 1 > dp[i]:
                dp[i] = dp[i - v] + 1
                parent[i] = (k, v)

    # find the best reachable value we can top up from
    best = max(range(target + 1), key=lambda i: dp[i] if dp[i] > -float('inf') else -float('inf'))

    result = []
    remaining = best
    while remaining > 0:
        k, v = parent[remaining]
        result.append(k)
        remaining -= v

    remaining = target - best
    for k, v in sorted(items, key=lambda x: x[1]):  # smallest value first for flexibility
        while remaining >= v:
            result.append(k)
            remaining -= v

    if remaining != 0:
        return None  # impossible even with repeats

    return result

def exact_terms_dp(target, val_map, n):
    items = list(val_map.items())

    # dp[i][j] = True if value i is reachable in exactly j unique keys
    dp = [[False] * (n + 1) for _ in range(target + 1)]
    dp[0][0] = True
    parent = [[None] * (n + 1) for _ in range(target + 1)]

    for k, v in items:
        for i in range(target, v - 1, -1):
            for j in range(n, 0, -1):
                if dp[i - v][j - 1] and not dp[i][j]:
                    dp[i][j] = True
                    parent[i][j] = (k, v)

    best_val, best_j = 0, 0
    for i in range(target + 1):
        for j in range(n + 1):
            if dp[i][j] and j > best_j:
                best_val, best_j = i, j

    # reconstruct unique portion
    result = []
    remaining = target - best_val
    terms_left = n - best_j
    i, j = best_val, best_j
    while i > 0:
        k, v = parent[i][j]
        result.append(k)
        i -= v
        j -= 1

    filled = False
    for k, v in sorted(items, key=lambda x: x[1]):
        if remaining % v == 0 and remaining // v == terms_left:
            for _ in range(terms_left):
                result.append(k)
            filled = True
            break

    if not filled and remaining > 0:
        return None  # impossible to hit exact n terms

    return result

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
    
    if "length" in params and isinstance(params["length"], int):
        x = exact_terms_dp(params["target"], create_modes[params["mode"]], params["length"])
    else:
        x = max_terms_dp(params['target'], create_modes[params["mode"]])
    return ''.join(sample(x, len(x)))
    