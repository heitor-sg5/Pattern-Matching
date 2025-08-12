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
        if bwt[i] == symbol:
            count += 1
    return count

def better_bw_matching(bwt, pattern, suffix_array):
    last_col = bwt
    first_col = ''.join(sorted(bwt))
    first_occurrence = {}
    for i, char in enumerate(first_col):
        if char not in first_occurrence:
            first_occurrence[char] = i
    checkpoints, step = build_checkpoints(last_col)
    top = 0
    bottom = len(last_col) - 1
    while top <= bottom:
        if pattern:
            symbol = pattern[-1]
            pattern = pattern[:-1]
            if symbol not in first_occurrence:
                return []
            top = first_occurrence[symbol] + count_symbol(checkpoints, last_col, symbol, top, step)
            bottom = first_occurrence[symbol] + count_symbol(checkpoints, last_col, symbol, bottom + 1, step) - 1
            if top > bottom:
                return []
        else:
            return (sorted(suffix_array[top:bottom + 1]), bottom - top + 1)
    return []

text = "GCACGGGGGTCACGGCGGTGAGGTGCTGCGCCGCCCGGGCGGAGACACGGGGCCGCGCGGCGGCCGCAGCGTCGGGGCTGCGCCCGCACCAGACGAGGGCCTGCGCCCACCGGCCGAGCCCCCTCCCCAGGCGGGCCCCCCGAGCCGGGGGGGACCCGGCGCAGGGGAGTTACGGGCGCGCACCCCTGGGGCTCGGTGCGCCTGCGCATTTCGTTCGCTCCGGGGGATTCACCGAGCCGCGTGCGCACTCCGCTGGGTCGTTGCGGCACGACGCCTGGCGGTCGGGCTAGTGGCCCTAGGCAACCGGGGCCGATGCGGGCTCACCCAAGGAGGGGTGCGGTCAACGCCTCGCGGCTCGGACAACGGCGCTCGGGGTAACACCCGCCCCGTAGGCTTTCGCTCCGGGGAGCACTCCCGAGCGCTCGCCGCCTCCGCCCCGAGCCCGCAGCACAGGCCAAAGCCCGCGCCCCCTTGCCGTCTCGGGGGGGCCCGTGCACGGGCCGAGCGTGGTCGGGGCTTGCCTTGGGCTGGCCTGGTCCAGACGCCGCCTCGGCAGGCGGCCCTGGGGCGCTGGCTCCGGGTACGTCTGTGTGCAGAGGATCGCGGAGCCGCTGCCGGGGCCGCGGGGGGGGGGAGGAACCTTGGCCCGTCCCGGTTCCCTCGCGCGCTGAGGCGGCGCGGACGGGTCAGTCGACCGCCCGGACAAGCAGAGGGGTTAGGCTGCCCGGGCAAGCGACCGCCCGGGCCCGGGCGGCGAGTCCGGCGAGGACCGCAAGGCTCTCCGCCCGCGGCCCATCCGGAAAGTCACGACTCCATGCGTGTGGGGTGCGCGGGTCCGCCCACCGTCGGGCCGCCCACATGCCCCGCGCGGCGGCGGTTCAGGTAACGCGGGAGGACGTCCGGGTGCCCGTGGCGCCCGGTGCGCACGCGGCGGCAGGGGGTTGCGGGGAACTGGCCCGGCCCCCCCCGCCGGGCGCCGCGCCTGGCCGGCGTGATGCCA$"
pattern = "CCGC"
bwt = burrows_wheeler_transform(text)
suffix_array = build_suffix_array(text)
positions = better_bw_matching(bwt, pattern, suffix_array)
print(f"BWT: {bwt}")
print(f"Occurances: {positions[1]} at positions {positions[0]}")
