from collections import defaultdict

def burrows_wheeler_transform(text):
    rotations = [text[i:] + text[:i] for i in range(len(text))]
    rotations_sorted = sorted(rotations)
    bwt = ''.join(rotation[-1] for rotation in rotations_sorted)
    return bwt

def build_suffix_array(text):
    return sorted(range(len(text)), key=lambda i: text[i:])

def build_checkpoints(bwt, step=5):
    counts = defaultdict(list)
    total_counts = defaultdict(int)
    length = len(bwt)
    chars = set(bwt)
    for c in chars:
        counts[c] = []
    for i in range(length):
        char = bwt[i]
        total_counts[char] += 1
        if i % step == 0:
            for c in chars:
                counts[c].append((i, total_counts[c]))
    if (length - 1) % step != 0:
        for c in chars:
            counts[c].append((length, total_counts[c]))
    return counts, step

def count_symbol(checkpoints, bwt, symbol, pos, step):
    if pos == 0:
        return 0
    if symbol not in checkpoints:
        return 0
    idx = pos // step
    idx_checkpoint = max(0, min(idx - 1, len(checkpoints[symbol]) - 1))
    checkpoint_pos, checkpoint_count = checkpoints[symbol][idx_checkpoint]
    count = checkpoint_count
    for i in range(checkpoint_pos, pos):
        if i > len(bwt) - 1:
            break
        if bwt[i] == symbol:
            count += 1
    return count

def get_first_occurrence(bwt):
    first_col = ''.join(sorted(bwt))
    first_occurrence = {}
    for i, char in enumerate(first_col):
        if char not in first_occurrence:
            first_occurrence[char] = i
    return first_occurrence

def approximate_bw_matching(bwt, pattern, suffix_array, d):
    first_occurrence = get_first_occurrence(bwt)
    checkpoints, step = build_checkpoints(bwt)

    def recursive_match(pattern, top, bottom, mismatches_left):
        if top > bottom:
            return set()
        if not pattern:
            return set(suffix_array[top:bottom+1])
        symbol = pattern[-1]
        pattern_rest = pattern[:-1]
        matches = set()
        if symbol in first_occurrence:
            new_top = first_occurrence[symbol] + count_symbol(checkpoints, bwt, symbol, top, step)
            new_bottom = first_occurrence[symbol] + count_symbol(checkpoints, bwt, symbol, bottom+1, step) - 1
            if new_top <= new_bottom:
                matches |= recursive_match(pattern_rest, new_top, new_bottom, mismatches_left)
        if mismatches_left > 0:
            for alt_symbol in first_occurrence.keys():
                if alt_symbol == symbol:
                    continue
                new_top = first_occurrence[alt_symbol] + count_symbol(checkpoints, bwt, alt_symbol, top, step)
                new_bottom = first_occurrence[alt_symbol] + count_symbol(checkpoints, bwt, alt_symbol, bottom+1, step) - 1
                if new_top <= new_bottom:
                    matches |= recursive_match(pattern_rest, new_top, new_bottom, mismatches_left - 1)
        return matches
    
    return recursive_match(pattern, 0, len(bwt)-1, d)

with open('kmers_output.txt', 'r') as file:
    patterns = file.read().strip().split()

text = "CCCGGCATCACGGCGCTTTGCCTGTTTAACACTCGGGGAGCTCACTCCAAACGCAGACTGGCTTTCGCTGTCACTGGCCTCTTGGCCGCGATGCGCCGGATCCGAGCCAGGCTCCTACGTCCCAGTTTACTATTCACGACAGGCGTGGTGTGTTGAGGCGAGACTCAGCAAAGGGCTATGAGCGCGACGGTCGCGGTGCT$"
bwt = burrows_wheeler_transform(text)
suffix_array = build_suffix_array(text)
d = 1 
for pat in patterns:
    positions = approximate_bw_matching(bwt, pat, suffix_array, d)
    if positions:
        print(f"Pattern '{pat}' occurs at positions: {sorted(positions)}")