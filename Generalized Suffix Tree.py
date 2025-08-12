class Node:
    def __init__(self):
        self.children = {}
        self.indexes = []
        self.color = None

def insert_suffix(root, suffix, start_idx, source):
    node = root
    for char in suffix:
        if char not in node.children:
            node.children[char] = Node()
        node = node.children[char]
    node.indexes.append((start_idx, source))

def build_generalized_suffix_tree(text1, text2):
    root = Node()
    for i in range(len(text1)):
        insert_suffix(root, text1[i:], i, 1)
    for i in range(len(text2)):
        insert_suffix(root, text2[i:], i, 2)
    return root

def suffix_tree(node):
    compressed = Node()
    compressed.indexes = node.indexes[:]
    for char, child in node.children.items():
        edge_label = char
        current_child = child
        while len(current_child.children) == 1 and not current_child.indexes:
            (next_char, next_node), = current_child.children.items()
            edge_label += next_char
            current_child = next_node
        compressed_child = suffix_tree(current_child)
        compressed.children[edge_label] = compressed_child
        compressed.indexes.extend(compressed_child.indexes)
    return compressed

def color_tree(node):
    sources = set(src for _, src in node.indexes)
    for edge_label, child in node.children.items():
        child_sources = color_tree(child)
        sources.update(child_sources)
    if sources == {1}:
        node.color = 'blue'
    elif sources == {2}:
        node.color = 'red'
    else:
        node.color = 'purple'
    return sources

def find_longest_shared(node, path="", best=("", 0)):
    if node.color == 'purple' and len(path) > best[1]:
        best = (path, len(path))
    for edge_label, child in node.children.items():
        best = find_longest_shared(child, path + edge_label, best)
    return best

def find_shortest_non_shared(node, path="", best=None, terminals={"#", "$"}):
    if node.color in ('blue', 'red') and node.indexes:
        if not any(t in path for t in terminals):
            if best is None or len(path) < best[1]:
                best = (path, len(path))
    for edge_label, child in node.children.items():
        best = find_shortest_non_shared(child, path + edge_label, best)
    return best

text1 = "GCGCCCCGGGTTCCAGCCCACGCGCTAGGGCCGGTCCCCGGCCCCGGCCCCGCGTGCGGGGTGCGCGCGGCGGCTGGGCGCGAGGGACGTCGCCTCACCGGACGTCACGCACCTGGTCCGCCCTGGCCTCTCGTCACGCCCCCCTGGCGGCGGCCAGTCGCTAGCCCCGCTACGCGGAGGCGCTCACTGCAGAGCCAACGCGCCCGTAGAGGGCCCAGGGCCGGGCACATGCTCGAATTCGAGCTATAGGGGCCCCGCCCGCCCTCATCATCCGTGCGGCTCGCCCATGCTCTCCTATCGCCCGAGGGGAGGATGCGTCCGGCCCGCCCTGGCCGCCCCCGTAAAGCCTGAAGCTAGGGGCGGCCGCCGGACATCGGCATGCGGCTGAGGGGGCTCGCTGCCAGCCCAGGGCTGGGCGACTGCCCACGAACCAGTGCTGGCGACGGGGACTGGATGGCGTACCCCCCCTCCGTAGCGGCGCTACCGTCTGCCGGGGCCGGCTAGCGAAAGCGCTCTCGGCTCGCGGAGCGGCGCGGCGCCAGCGCGGCGCCCACCCCGGGGGCCTTGGAGGCCCCTGCCCCAGGAAGCCTACGGCTGTGGCCGCTCCCGTTGGGGGCTCTGGCGGCACCGATCAGCTATCGGGCGCGGGCGGCGCTTGGCGCCCGGGGTATGAGGCAGTGACACACGAAACCGCCTCGGTGAGCCACCCTGCTTCGGCCACGCGACGGCTGCGCGCTCTACGCTTCACGTGCGGGGGTCGCCGCAGCTGCGAGAGCCATGGCCTCCCAGGGGTGGGCGCCGCGGGCAGGAGGGTCCCCCGCGCGCGCGAACCTGGTACCCACGCAAGGCAGGGGGGGTGCCGCACCGCGGGCGCCCCGCCACCGCGATCGGAGGCACTTGGGGACGCCCTAAGCTCAAGCCGCCCTTGCCCCGCTGGCCTCCGGCGGCATCCCCCGGTGCGGCGAGCCGGCGACCTGACGGGCCGCCCCGGCCCGGTCCA#"
text2 = "TGGTAGCCGTGTGCGCCAGGTCCAGGGTGGCTGCTGCCGTCCCCCCCACGAGGGTGGGGCGCCACTCTGCACTCATCGCCGCGCCAGCCCGCCGGGCCCACCGCCGTTTTGTGGTGGCCAGTAGAGCCCCCGACCCGTCGGCCCCAGGAAGGGCAGTGGGGACCCGTAGGGACCGGGATCGGCCGGTGGCAATGCGGGATACACTCCCGTACTGTAGAGCGGTACCCCGTCGCGGCAAGGGGGCGCCCCGGTGAGTGAGCGGCACCCCGCCGCGAACTCGGGAGTGGCTGGGGTACCGGCGAGGGTCGCACTGAGGGATGAGATACTCAGCCGACCGGGCTCCCCCGCTCGAGCAATAGTGGGAAGGGCCGCCCTGGGACCAATGCACCCCCCCCTCCCTTCGGGGGTAGAGCCTCGGCCGGATCGTCGCCCTACCCTCGCGCCGCCGGCGCGTCCGAGCACCGGCAATCGTGGAGGTCGGATGTGATAAGGAGGGGTTAACTCGGGGGCGGAGGTTCGGCGGGCCCGGGTCCGCGGCACTGCACCGCACCATCCACGTGGGGCTCGGGGTCCGGACTGGCACTAAAACCCCATGCCCCTGCGCGGTGCGGGTCCGCCGGCCGGAGTCGCTACCGCCACCCAATTACGGCGCCATCCGGGGGGCGGCGAGGCGCCCGCCGCCGCCGCCGTGGTCTTATAGCAGCGGGCCCGCAGGAGGGCCAGCGGGCCGGCGCGGGTGACGGCAACGGATTGGCCGGGCTGCCGGACCGGCACTGGGGCACTCGGGTCCAGCTGACCGCCCAAGTCGCTCCGGGCCGCGACCCGCTCCCTGCCCTGGGGCTATGCGCCTTCTCCCCCTGAGGGAACGGGACACGGGGTGCGGGCGTCGGGCGTCAACGCCGGTGGCTCGATCTCCAACGTGAGCGCGCAGTTGAGCGCGTCTACACTTCGGCCTCCGTCCCGGCTCACAGTCCTAGAGTAGCGCGTTACGGGGAGGTGC$"

root = build_generalized_suffix_tree(text1, text2)
tree_root = suffix_tree(root)
color_tree(tree_root)
longest_shared, _ = find_longest_shared(tree_root)
shortest_non_shared, _ = find_shortest_non_shared(tree_root)

print(f"Longest shared substring: {longest_shared}")
print(f"Shortest non-shared substring: {shortest_non_shared}")
