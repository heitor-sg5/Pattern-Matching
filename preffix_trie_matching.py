def construct_trie(patterns):
    trie = [{}]
    for pattern in patterns:
        current_node = 0
        for symbol in pattern:
            if symbol in trie[current_node]:
                current_node = trie[current_node][symbol]
            else:
                trie.append({})
                new_node = len(trie) - 1
                trie[current_node][symbol] = new_node
                current_node = new_node
    return trie

def prefix_trie_matching(text, trie):
    index = 0
    symbol = text[index]
    v = 0
    while True:
        if not trie[v]:
            return True
        elif symbol in trie[v]:
            v = trie[v][symbol]
            index += 1
            if index < len(text):
                symbol = text[index]
            else:
                symbol = None
        else:
            return False  

def trie_matching(text, patterns):
    trie = construct_trie(patterns)
    positions = []
    for i in range(len(text)):
        if prefix_trie_matching(text[i:], trie):
            positions.append(i + 1)
    return positions

Text = "AATCGGGTTCAATCGGGGT"
Patterns = ["ATCG", "GGGT"]
result = trie_matching(Text, Patterns)
print(" ".join(map(str, result)))
