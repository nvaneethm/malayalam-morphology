# MALAYALAM MORPHOLOGICAL ANALYZER
## SANDHI SPLITTER

Trie consists of nodes and edges which grows as different word pattern arrives. Each node in ourtrie structure stores
i. Character, for storing the letter: Char
ii.Children, for storing the child nodes: List
iii. Word_finished, flag value for future processing: Boolean
Two orthogonal tries are built.  One as input words given as it is and second trie is build withinput words reversed. The need for the two tries are, first one is used to find the common prefixesand the second one is used to find the common suffix.


The input word is traversed iteratively traversed (character-by-character, appending in eachiteration) through the trie structures checking whether it completes a word, the complete wordsare identified using the Word_finished flag. The complete words identified in the process arekept in a list. The same is done with the reversed form of word and corresponding trie structure.Complete words from both the lists are taken and the cross product of the lists are comparedwith the actual input word. Combinations which has a match greater than a threshold of 85% areselected as possible morphemes. Which is then to be finalized by checking the Sandhi rules. Thecomparison is done using the levenshtein distance, which is a metric that measures how manysingle-character edits are required to change from one string to another.
