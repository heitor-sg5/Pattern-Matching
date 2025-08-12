def burrows_wheeler_transform(text):
    rotations = [text[i:] + text[:i] for i in range(len(text))]
    rotations_sorted = sorted(rotations)
    bwt = ''.join(rotation[-1] for rotation in rotations_sorted)
    return bwt

def last_to_first_mapping(bwt):
    occ_counts = {}
    last_col_ranks = []
    for char in bwt:
        occ_counts[char] = occ_counts.get(char, 0) + 1
        last_col_ranks.append((char, occ_counts[char]))
    first_col = sorted(bwt)
    occ_counts_first = {}
    first_col_ranks = []
    for char in first_col:
        occ_counts_first[char] = occ_counts_first.get(char, 0) + 1
        first_col_ranks.append((char, occ_counts_first[char]))
    lf_mapping = [0] * len(bwt)
    for i, rank in enumerate(last_col_ranks):
        lf_mapping[i] = first_col_ranks.index(rank)
    return lf_mapping

def bw_matching(bwt, pattern):
    lf_mapping = last_to_first_mapping(bwt)
    last_col = bwt
    top = 0
    bottom = len(last_col) - 1
    while top <= bottom:
        if pattern:
            symbol = pattern[-1]
            pattern = pattern[:-1]
            positions = [i for i in range(top, bottom + 1) if last_col[i] == symbol]
            if positions:
                top_index = positions[0]
                bottom_index = positions[-1]
                top = lf_mapping[top_index]
                bottom = lf_mapping[bottom_index]
            else:
                return 0
        else:
            return bottom - top + 1
    return 0

text = "GCACGGGGGTCACGGCGGTGAGGTGCTGCGCCGCCCGGGCGGAGACACGGGGCCGCGCGGCGGCCGCAGCGTCGGGGCTGCGCCCGCACCAGACGAGGGCCTGCGCCCACCGGCCGAGCCCCCTCCCCAGGCGGGCCCCCCGAGCCGGGGGGGACCCGGCGCAGGGGAGTTACGGGCGCGCACCCCTGGGGCTCGGTGCGCCTGCGCATTTCGTTCGCTCCGGGGGATTCACCGAGCCGCGTGCGCACTCCGCTGGGTCGTTGCGGCACGACGCCTGGCGGTCGGGCTAGTGGCCCTAGGCAACCGGGGCCGATGCGGGCTCACCCAAGGAGGGGTGCGGTCAACGCCTCGCGGCTCGGACAACGGCGCTCGGGGTAACACCCGCCCCGTAGGCTTTCGCTCCGGGGAGCACTCCCGAGCGCTCGCCGCCTCCGCCCCGAGCCCGCAGCACAGGCCAAAGCCCGCGCCCCCTTGCCGTCTCGGGGGGGCCCGTGCACGGGCCGAGCGTGGTCGGGGCTTGCCTTGGGCTGGCCTGGTCCAGACGCCGCCTCGGCAGGCGGCCCTGGGGCGCTGGCTCCGGGTACGTCTGTGTGCAGAGGATCGCGGAGCCGCTGCCGGGGCCGCGGGGGGGGGGAGGAACCTTGGCCCGTCCCGGTTCCCTCGCGCGCTGAGGCGGCGCGGACGGGTCAGTCGACCGCCCGGACAAGCAGAGGGGTTAGGCTGCCCGGGCAAGCGACCGCCCGGGCCCGGGCGGCGAGTCCGGCGAGGACCGCAAGGCTCTCCGCCCGCGGCCCATCCGGAAAGTCACGACTCCATGCGTGTGGGGTGCGCGGGTCCGCCCACCGTCGGGCCGCCCACATGCCCCGCGCGGCGGCGGTTCAGGTAACGCGGGAGGACGTCCGGGTGCCCGTGGCGCCCGGTGCGCACGCGGCGGCAGGGGGTTGCGGGGAACTGGCCCGGCCCCCCCCGCCGGGCGCCGCGCCTGGCCGGCGTGATGCCA$"
pattern = "CCGC"
bwt = burrows_wheeler_transform(text)
print(f"BWT: {bwt}")
print(f"Occurances: {bw_matching(bwt, pattern)}")