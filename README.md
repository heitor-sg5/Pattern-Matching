# Combinational Sequence Matching

This repository implements foundational string algorithms used for efficient sequence analysis, storage, and retrieval in bioinformatics. It includes construction of the Burrows-Wheeler Transform (BWT), suffix arrays, and methods for exact and approximate pattern matching using BWT-based indexes. These tools are essential for tasks such as read mapping, variant detection, and genome assembly.

---

## 🧬 What is Sequence Matching?

In modern genomics, analyzing DNA sequences involves searching for specific patterns (e.g., genes, motifs, or variants) within large genomes. Directly scanning sequences is computationally expensive due to the enormous size of genomic data. 

BWT is a reversible text transformation that rearranges sequence characters to group similar substrings together, enabling highly efficient compression and fast pattern searching. By combining BWT with suffix arrays and specialized data structures like checkpoints, we can perform exact and approximate pattern matching in logarithmic time. Approximate pattern matching allows detection of sequences with a limited number of mismatches, crucial for identifying biological variants like SNPs (single nucleotide polymorphisms) or sequencing errors in reads.

---

## 📁 Files in This Repository

- `preffix_trie_matching.py`: Builds a prefix trie from input patterns and finds all occurrences of these patterns in the given text.
- `suffix_tree.py`: Constructs a suffix tree for a text and identifies the longest repeated substring within it.
- `generalized_suffix_tree.py`: Builds a suffix tree for two strings combined and outputs their longest common substring and shortest unique substring using color-coded paths.
- `suffix_array_matching.py`: Creates a suffix array for a text and uses double binary search to find all occurrences of a pattern efficiently.
- `bwt_matching.py`: Computes the BWT of a text and counts occurrences of a pattern using last-to-first column mapping.
- `better_bwt_matching.py`:  Implements an optimized BWT pattern matcher using checkpoints, suffix arrays, and counting arrays to efficiently locate pattern positions.
- `approximate_bwt_pattern_matching.py`: Extends better BWT matching with recursion to allow mismatches and find approximate occurrences of multiple patterns in the text.

## ⚙️ How to Use

### 1. Prepare Input

The inputs for the algorithms are one or two strings Text and a list of string patterns, depending on script being used:

- `suffix_tree.py` requires one string Text, while `generalized_suffix_tree.py` uses two.
- `suffix_array_matching.py`, `bwt_matching.py`, and `better_bwt_matching.py` require a string Text and a string Pattern
- `preffix_trie_matching.py` and `approximate_bwt_pattern_matching.py` both use a string Text and a list of strings Patterns, however, `approximate_bwt_pattern_matching.py` takes reads from a file `kmers_output.txt`.

### 2. Run the Algorithms

Each script will produce:

- Lists of positions where given patterns occur in the input text, for pattern matching scripts like `preffix_trie_matching.py`, `suffix_array_matching.py`, `bwt_matching.py`, and `better_bwt_matching.py`.
- The BWT string itself as output from `bwt_matching.py` and `better_bwt_matching.py`.
- The longest repeated substring found in the input text for `suffix_tree.py`.
- The longest shared substring and shortest non-shared substring between two input strings from `generalized_suffix_tree.py`.
- For `approximate_bwt_pattern_matching.py`, the positions of approximate matches (allowing mismatches, d) of multiple query patterns in the input text.

---

#### Preffix Trie Matching

  bash
```preffix_trie_matching.py```

#### Suffix Tree Construction

  bash
```suffix_tree.py```

#### Generalized Suffix Tree Construction

  bash
```generalized_suffix_tree.py```

#### Suffix Array Matching

  bash
```suffix_array_matching.py```

#### BWT Matching

  bash
```bwt_matching.py```

#### Better BWT Matching

  bash
```better_bwt_matching.py```

#### Approximate Pattern Matching

  bash
```approximate_bwt_pattern_matching.py```

Parameters Text, Pattern(s) and mismatches (d) can be changed at bottom of each script. However, `approximate_bwt_pattern_matching.py` will use Patterns from a local text file `kmers_output.txt`.

---

## 🧠 Algorithm Overviews

### Preffix Trie Matching 

- Constructs a trie (prefix tree) from a list of input patterns, representing all patterns as paths in the trie.
- For each position in the text, attempts to match a prefix of the text against any pattern in the trie by traversing nodes.
- Outputs all starting positions in the text where any pattern from the list occurs.
- Time complexity: O(n * m)

### Suffix Tree Construction

- Builds a suffix trie for a given text by inserting all suffixes starting at every position.
- Compresses the trie into a suffix tree by merging unary paths, resulting in edge-labeled nodes that represent substrings.
- Recursively traverses the suffix tree to find the longest substring that appears more than once in the text.
- Outputs the longest repeated substring and its length.
- Time complexity: O(n^2)

### Generalized Suffix Tree Construction

- Builds a generalized suffix tree by inserting all suffixes of two input strings into a shared trie structure, labeling each suffix by its source string.
- Compresses the trie into a suffix tree by merging unary paths into edge-labeled nodes
- Colors nodes based on whether substrings occur only in the first string (blue), only in the second string (red), or both (purple).
- Finds the longest substring shared by both strings (purple nodes) and the shortest substring unique to either string (blue or red nodes).
- Time complexity: O(n^2)

### Suffix Array Matching

- Builds a suffix array by sorting all suffixes of the input text lexicographically and storing their starting indices.
- Uses binary search twice on the suffix array to find the first and last occurrences of the pattern efficiently.
- Returns all starting positions in the text where the pattern occurs, based on the range found in the suffix array.
- Time complexity: O(n * log n)

### BWT Matching

- Constructs the BWT of the input text by generating all cyclic rotations, sorting them lexicographically, and concatenating the last characters of each sorted rotation.
- Builds the last-to-first mapping by tracking the rank of each character occurrence in the last column (BWT) and matching it to the corresponding rank in the first column (sorted BWT).
- Implements backward search on the BWT using the LF mapping to count the number of occurrences of a given pattern in the original text.
- Returns the count of pattern occurrences based on the narrowing top-bottom interval in the BWT matrix during backward search.
- Time complexity: O(n^2 * log n)

### Better BWT Matching

- Builds suffix array by sorting all suffixes lexicographically to store starting indices (same as suffix array matching).
- Uses checkpoints to store cumulative counts of each character in the BWT at fixed intervals, enabling faster rank queries.
- Implements a rank function that efficiently counts occurrences of a symbol up to a position using checkpoints.
- Performs backward search on the BWT using first occurrence indices and rank queries via checkpoints to find the pattern’s match range.
- Returns sorted list of all matching positions in the original text (from suffix array) and the number of occurrences.
- Time complexity: (m * log n)

### Approximate BWT Matching

- Builds suffix array and BWT of the text.
- Uses checkpoints and first occurrence maps for efficient rank queries on BWT.
- Implements a recursive backtracking search on the BWT to allow up to d mismatches in the pattern.
- For each symbol in the pattern (processed backwards), tries exact matches and, if mismatches remain, explores all possible alternative symbols.
- Collects all suffix array positions corresponding to approximate matches.
- Outputs all occurrences of each pattern allowing up to d mismatches.
- Time complexity: (m * log n) for small values of d (e.g. d = 1)

---

## 🧪 Example Output

Pattern 'AAAGGGCTAT' occurs at positions: [169]
Pattern 'AGCAAAGGGC' occurs at positions: [104]
Pattern 'AGGGCTATGA' occurs at positions: [131, 171]
Pattern 'ATCCGAGCCA' occurs at positions: [177]
Pattern 'ATGCGCCGGA' occurs at positions: [90, 195]
Pattern 'CAAAGGGCTA' occurs at positions: [168]
Pattern 'CACTCGGGGA' occurs at positions: [53]
Pattern 'CACTGGCCTC' occurs at positions: [159]
Pattern 'CAGCAAAGGG' occurs at positions: [103]
Pattern 'CCCGGCATCA' occurs at positions: [101]
Pattern 'CGGTCGCGGT' occurs at positions: [187]
Pattern 'CGTGGTGTGT' occurs at positions: [198]
Pattern 'CTGGCCTCTT' occurs at positions: [57]
Pattern 'CTGGCTTTCG' occurs at positions: [33, 144]
Pattern 'CTGTCACTGG' occurs at positions: [67]
Pattern 'CTTGGCCGCG' occurs at positions: [31, 80]
Pattern 'CTTTCGCTGT' occurs at positions: [61]
Pattern 'GACGGTCGCG' occurs at positions: [185]
Pattern 'GAGCCAGGCT' occurs at positions: [103]
Pattern 'GATCCGAGCC' occurs at positions: [176]
Pattern 'GCTCCTACGT' occurs at positions: [66]
Pattern 'GCTGTCACTG' occurs at positions: [66]
Pattern 'GCTTTCGCTG' occurs at positions: [60]
Pattern 'GGGCTATGAG' occurs at positions: [58, 172]
Pattern 'GGTCGCGGTC' occurs at positions: [188, 194]
Pattern 'GTCGCGGTCC' occurs at positions: [189]
Pattern 'GTGGTGTGTT' occurs at positions: [67, 144]
Pattern 'TAACACTCGG' occurs at positions: [115]
Pattern 'TACGTCCCAG' occurs at positions: [115]
Pattern 'TTCGCTGTCA' occurs at positions: [63, 195]
Pattern 'TTGCCTGTTT' occurs at positions: [17, 73]
Pattern 'TTGGCCGCGA' occurs at positions: [32, 81]
Pattern 'TTTCGCTGTC' occurs at positions: [62]

---

## 👤 Author

Heitor Gelain do Nascimento
Email: heitorgelain@outlook.com
GitHub: @heitor-sg5

---

## 📚 References

Bioinformatics Algorithms: An Active Learning Approach (Chapter 9) by
Phillip Compeau & Pavel Pevzner
https://bioinformaticsalgorithms.com
