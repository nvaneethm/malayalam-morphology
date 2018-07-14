
# coding: utf-8


#node
class TrieNode(object):
    def __init__(self, char:str):
        self.char = char
        self.children = []
        self.wordFinished = False
        self.counter = 1



#adding a word
def addword(root, word:str):
    node = root
    #print(word)
    for char in word:
        found_in_child = False
        for child in node.children:
            if child.char == char:
                found_in_child = True
                child.counter += 1
                node = child
                break
        
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            node = new_node
            #print(node.char)
    node.wordFinished = True




from typing import Tuple
def findPrefix(root, prefix: str) -> Tuple[bool, int]:
    node = root
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        for child in node.children:
            if child.char == char:
                print(child.counter,char)
                char_not_found = False
                node = child
                break
        if char_not_found:
            return False, 0
    return True , node.counter


# In[5]:


#f = open('untitled.txt', encoding='utf-8') 
import re
def getWords(text):
    return re.compile('\w+').findall(text)


# In[6]:


newroot = TrieNode("-")
a = []
def readWords(filename: str):
    with open(filename , encoding='utf-8') as f:
          for line in f:
            for k in getWords(line):
                addword(newroot, k.lower())



# function to find the last node
def findNode(root, prefix: str):
    node = root
    wor = prefix
    if not root.children:
        return 0
    for char in prefix:
        char_not_found = True
        for child in node.children:
            if child.char == char:
                char_not_found = False
                node = child
                break
                wor += char
        if char_not_found:
            return 0
    return node


# In[28]:


#node with largest countr value
def largeNode(root):
    count = 0
    for child in root.children:
        if child.counter >= count:
            larg_node = child
            count = child.counter
    return larg_node


# In[52]:


#finding words 
def findWords(root, word: str):
    word_in_node = findNode(root, word)
    stri = word
    while True:
            if not word_in_node.wordFinished:
                word_in_node = largeNode(word_in_node)
                stri += word_in_node.char 
                
            else:
                return stri

            


#adding words in reverse order
def addwordReverse(root, word: str):
    str = ""
    for i in word:
        str = i + str
    addword(root, str)

#to check whether a word is complete
def isComplete(root, word:str):
    if findNode(root, word).wordFinished:
        return True
    else:
        return False

