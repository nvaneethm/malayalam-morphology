
# coding: utf-8

# In[ ]:


import re
from collections import Counter
import pickle
import Levenshtein
import triee


# In[ ]:


with open('root.pkl', 'rb') as inputfile:
     root = pickle.load(inputfile)
with open('reroot.pkl', 'rb') as inputfile:
     reroot = pickle.load(inputfile)
with open('wordlist.pkl', 'rb') as inputfile:
     wordList = pickle.load(inputfile)


# In[ ]:


def findWords(root, word: str):
    wList = []
    na = ""
    for i in range(len(word)):
        na=word[:i+1]
        no = triee.findNode(root, na)
        child = no.children
        for j in child:
            if j.wordFinished:
                wr=na+j.char
                wList.append(wr)
    return list(set(wList))


# In[ ]:


def findList(root,reroot, word:str):
    forList = []
    bacList = []
    stri = ""
    freq = 0
    for i in word:
        stri += i
        #print("word:\t",stri)
        #triee.findPrefix(root, stri)
        try:
            for n in findWords(root, stri):
                forList.append(n)
            #bacList.append(triee.findWords(reroot, stri[::-1]))
        except:
            #print("exception:",stri)
            a=0
    stri = ""
    for i in word[::-1]:
        stri += i
        #print("word:\t",stri)
        #triee.findPrefix(root, stri)
        try:
            for n in findWords(reroot, stri):
                bacList.append(n)
            #forList.append(triee.findWords(root, stri))
        except:
            #print("exception:",stri)
            a=0
    
    return list(set(forList)) , list(set(bacList))


# In[ ]:


def wordSplit(root, reroot, word):
    f,r = findList(root, reroot, word)
    for i in f:
        regx = re.compile(i)
        for j in r:
            regx2 = re.compile(j)
            if regx.search(word):
                #if len(i+j) == len(word):
                if regx2.search(word[::-1]):
                    if len(i+j)>= len(word)-2 and len(i+j)<=len(word):
                        Lev=Levenshtein.ratio(i+j[::-1],word)
                        if Lev >= .95:
                            print (i,"+",j[::-1],Lev)
                    
                        


# In[ ]:


def wordSplit3(root, reroot, word):
    f,r = findList(root, reroot, word)
    combined = []
    for i in f:
        for j in r:
            if Levenshtein.ratio(i, word[:len(i)])>=.98 and Levenshtein.ratio(j[::-1], word[len(word)-len(j):])>=.98:
                Lev=Levenshtein.ratio(i+j[::-1],word)
                if Lev>.9:
                    if len(i) < len(word) and len(j) < len(word):
                        if len(i+j)>= len(word)-2 and len(i+j)<=len(word):
                            combined.append([i,j[::-1],Lev])
    a = sorted(combined,key=lambda y: y[2],reverse=True)
    #print(a)
    return a[:10]


# In[ ]:


def wordSplit1lev(root, reroot, word):
    f,r = findList(root, reroot, word)
    combined=[]
    for i in f:
        for j in r:
            Lev=Levenshtein.ratio(i+j[::-1],word)
            if Lev>.75:
                if len(i) < len(word) and len(j) < len(word):
                    if len(i+j)>= len(word)-2 and len(i+j)<=len(word):
                        combined.append([i,j[::-1],Lev])
    a = sorted(combined,key=lambda y: y[2],reverse=True)
    #print(a[:30])
    return a


# In[ ]:


def wordSplit2(root, reroot, word):
    f,r = findList(root, reroot, word)
    combined=[]
    for i in f:
        for j in r:
            Lev=Levenshtein.ratio(i+j[::-1],word)
            fr=Levenshtein.ratio(i,word)
            re=Levenshtein.ratio(j[::-1],word)
            if Lev>.75:
                if len(i) < len(word) and len(j) < len(word):
                    if len(i+j)>= len(word)-2 and len(i+j)<=len(word):
                        combined.append([i,j[::-1],Lev+fr+re])
    a = sorted(combined,key=lambda y: y[2],reverse=True)
    #print(a[:30])
    return a[:10]


# In[ ]:


def wordList4(word):
    f,r = findList(root, reroot, word)
    lf = 0.0
    lr = 0.0
    for i in f:
        if len(i) != len(word):
            Lev=Levenshtein.ratio(i,word)
            #print(i,Lev)
            if lf<Lev:
                lf = Lev
                fc = len(i)
        #print("\n")
    for i in r:
        if len(i) != len(word):
            Lev=Levenshtein.ratio(i[::-1],word)
            #print(i[::-1],Lev)
            if lr< Lev:
                lr = Lev
                rc = len(i)
        #print(lf,lr)
    if lf > lr:
        return word[:fc], word[fc:], lf
    else:
        le = len(word)-rc
        return word[:le], word[le:],lr


# In[ ]:


def testSplit(listt):
    
    for i in listt:
        print(i+"  =")
        wList = []
        wlist = wordSplit3(root,reroot,i)
        if not wlist and len(i)>6:
            print("(approx.)")
            wlist = wordSplit2(root,reroot,i)
            wlist.append(list(wordList4(i)))
        if wlist:
            for k in wlist:
                print(k)
        print("--------------")


# In[ ]:


def multiple_replace(text):
    dict={'\u0D23\u0D4D\u200D':'\u0D7A',
         '\u0D28\u0D4D\u200D':'\u0D7B',
         '\u0D30\u0D4D\u200D':'\u0D7C',
         '\u0D32\u0D4D\u200D':'\u0D7D',
         '\u0D33\u0D4D\u200D':'\u0D7E',
         '\u200a':'',
         '\u200c':'',
         '\u200d':'',
         '\u200b':'',
         '\u200e':'',
         '\u200f':''}
    
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 


# In[ ]:


testSplit(["അവളെവിടെ"])

