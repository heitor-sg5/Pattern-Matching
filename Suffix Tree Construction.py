class Node:
    def __init__(self):
        self.children = {}
        self.indexes = []

def suffix_tree_construction(text):
    root = Node()
    for i in range(len(text)):
        current_node = root
        for j in range(i, len(text)):
            symbol = text[j]
            if symbol in current_node.children:
                current_node = current_node.children[symbol]
            else:
                new_node = Node()
                current_node.children[symbol] = new_node
                current_node = new_node
        current_node.indexes.append(i)
    return root

def suffix_tree(node):
    compressed_node = Node()
    for edge_label, child in node.children.items():
        current_label = edge_label
        current_child = child
        while len(current_child.children) == 1 and not current_child.indexes:
            (next_label, next_child), = current_child.children.items()
            current_label += next_label
            current_child = next_child
        compressed_child = suffix_tree(current_child)
        compressed_node.children[current_label] = compressed_child
        compressed_child.indexes = current_child.indexes
    return compressed_node

def find_longest_repeated_substring(node, path=""):
    if len(node.children) == 0:
        return ("", 0)
    longest_substring = ""
    max_length = 0
    if len(node.children) > 1 or len(node.indexes) > 1:
        longest_substring = path
        max_length = len(path)
    for edge_label, child in node.children.items():
        sub_str, sub_len = find_longest_repeated_substring(child, path + edge_label)
        if sub_len > max_length:
            longest_substring = sub_str
            max_length = sub_len
    return (longest_substring, max_length)

text = "GCACGGGGGTCACGGCGGTGAGGTGCTGCGCCGCCCGGGCGGAGACACGGGGCCGCGCGGCGGCCGCAGCGTCGGGGCTGCGCCCGCACCAGACGAGGGCCTGCGCCCACCGGCCGAGCCCCCTCCCCAGGCGGGCCCCCCGAGCCGGGGGGGACCCGGCGCAGGGGAGTTACGGGCGCGCACCCCTGGGGCTCGGTGCGCCTGCGCATTTCGTTCGCTCCGGGGGATTCACCGAGCCGCGTGCGCACTCCGCTGGGTCGTTGCGGCACGACGCCTGGCGGTCGGGCTAGTGGCCCTAGGCAACCGGGGCCGATGCGGGCTCACCCAAGGAGGGGTGCGGTCAACGCCTCGCGGCTCGGACAACGGCGCTCGGGGTAACACCCGCCCCGTAGGCTTTCGCTCCGGGGAGCACTCCCGAGCGCTCGCCGCCTCCGCCCCGAGCCCGCAGCACAGGCCAAAGCCCGCGCCCCCTTGCCGTCTCGGGGGGGCCCGTGCACGGGCCGAGCGTGGTCGGGGCTTGCCTTGGGCTGGCCTGGTCCAGACGCCGCCTCGGCAGGCGGCCCTGGGGCGCTGGCTCCGGGTACGTCTGTGTGCAGAGGATCGCGGAGCCGCTGCCGGGGCCGCGGGGGGGGGGAGGAACCTTGGCCCGTCCCGGTTCCCTCGCGCGCTGAGGCGGCGCGGACGGGTCAGTCGACCGCCCGGACAAGCAGAGGGGTTAGGCTGCCCGGGCAAGCGACCGCCCGGGCCCGGGCGGCGAGTCCGGCGAGGACCGCAAGGCTCTCCGCCCGCGGCCCATCCGGAAAGTCACGACTCCATGCGTGTGGGGTGCGCGGGTCCGCCCACCGTCGGGCCGCCCACATGCCCCGCGCGGCGGCGGTTCAGGTAACGCGGGAGGACGTCCGGGTGCCCGTGGCGCCCGGTGCGCACGCGGCGGCAGGGGGTTGCGGGGAACTGGCCCGGCCCCCCCCGCCGGGCGCCGCGCCTGGCCGGCGTGATGCCA$"
suffix_trie_root = suffix_tree_construction(text)
suffix_tree_root = suffix_tree(suffix_trie_root)
longest_substr, length = find_longest_repeated_substring(suffix_tree_root)
print(f"Substring: {longest_substr}\nLength: {length}")
