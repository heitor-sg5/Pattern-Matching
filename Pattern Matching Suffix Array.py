def suffix_array(text):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort(key=lambda x: x[0])
    return [pos for _, pos in suffixes]

def pattern_matching_with_suffix_array(text, pattern, sa):
    n = len(text)
    min_index = 0
    max_index = n - 1
    while min_index <= max_index:
        mid_index = (min_index + max_index) // 2
        suffix = text[sa[mid_index]:]
        if pattern > suffix:
            min_index = mid_index + 1
        else:
            max_index = mid_index - 1
    first = min_index
    if not text[sa[first]:].startswith(pattern):
        return None
    min_index = first
    max_index = n - 1
    while min_index <= max_index:
        mid_index = (min_index + max_index) // 2
        suffix = text[sa[mid_index]:]
        if suffix.startswith(pattern):
            min_index = mid_index + 1
        else:
            max_index = mid_index - 1
    last = max_index
    return (first, last)

def matches_from_range(sa, first_last):
    if first_last:
        return sorted([sa[i] + 1 for i in range(first_last[0], first_last[1] + 1)])
    return []

text = "GCACGGGGGTCACGGCGGTGAGGTGCTGCGCCGCCCGGGCGGAGACACGGGGCCGCGCGGCGGCCGCAGCGTCGGGGCTGCGCCCGCACCAGACGAGGGCCTGCGCCCACCGGCCGAGCCCCCTCCCCAGGCGGGCCCCCCGAGCCGGGGGGGACCCGGCGCAGGGGAGTTACGGGCGCGCACCCCTGGGGCTCGGTGCGCCTGCGCATTTCGTTCGCTCCGGGGGATTCACCGAGCCGCGTGCGCACTCCGCTGGGTCGTTGCGGCACGACGCCTGGCGGTCGGGCTAGTGGCCCTAGGCAACCGGGGCCGATGCGGGCTCACCCAAGGAGGGGTGCGGTCAACGCCTCGCGGCTCGGACAACGGCGCTCGGGGTAACACCCGCCCCGTAGGCTTTCGCTCCGGGGAGCACTCCCGAGCGCTCGCCGCCTCCGCCCCGAGCCCGCAGCACAGGCCAAAGCCCGCGCCCCCTTGCCGTCTCGGGGGGGCCCGTGCACGGGCCGAGCGTGGTCGGGGCTTGCCTTGGGCTGGCCTGGTCCAGACGCCGCCTCGGCAGGCGGCCCTGGGGCGCTGGCTCCGGGTACGTCTGTGTGCAGAGGATCGCGGAGCCGCTGCCGGGGCCGCGGGGGGGGGGAGGAACCTTGGCCCGTCCCGGTTCCCTCGCGCGCTGAGGCGGCGCGGACGGGTCAGTCGACCGCCCGGACAAGCAGAGGGGTTAGGCTGCCCGGGCAAGCGACCGCCCGGGCCCGGGCGGCGAGTCCGGCGAGGACCGCAAGGCTCTCCGCCCGCGGCCCATCCGGAAAGTCACGACTCCATGCGTGTGGGGTGCGCGGGTCCGCCCACCGTCGGGCCGCCCACATGCCCCGCGCGGCGGCGGTTCAGGTAACGCGGGAGGACGTCCGGGTGCCCGTGGCGCCCGGTGCGCACGCGGCGGCAGGGGGTTGCGGGGAACTGGCCCGGCCCCCCCCGCCGGGCGCCGCGCCTGGCCGGCGTGATGCCA$"
sa = suffix_array(text)
pattern = "CCGC"
first_last = pattern_matching_with_suffix_array(text, pattern, sa)

print(f"Suffix array: {sa}")
positions = matches_from_range(sa, first_last)
print(f"First and last indices: {first_last}")
print(f"Genome positions: {positions}")
