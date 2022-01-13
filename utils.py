import os
from typing import Callable, List, Dict

TelexDict = Dict[str, str]

double_telex_composition = {
    "ướ": ['uo', "w", "s"], "ườ": ['uo','w','f'],
    "ưỡ": ['uo', "w", "x"], "ưở": ['uo','w','r'],
    "ượ": ['uo', "w", "j"], "ươ": ['uo', "w"] }
single_telex_composition = {
    "á": ["a","s"], "à": ["a","f"],
    "ạ": ["a","j"], "ả": ["a","r"],
    "ã": ["a","x"], "â": ["a","a"],
    "ấ": ["a","a","s"],"ầ": ["a","a","f"],
    "ậ": ["a","a","j"],"ẩ": ["a","a","r"],
    "ẫ": ["a","a","x"],"ă": ["a","w"],
    "ắ": ["a","w","s"],"ằ": ["a","w","f"],
    "ặ": ["a","w","j"],"ẳ": ["a","w","r"],
    "ẵ": ["a","w","x"],"í": ["i","s"],
    "ì": ["i","f"],"ỉ": ["i","r"],
    "ĩ": ["i","x"],"ị": ["i","j"],
    "ú": ["u","s"],"ù": ["u","f"],
    "ủ": ["u","r"],"ũ": ["u","x"],
    "ụ": ["u","j"],"ư": ["u","w"],
    "ứ": ["u","w","s"],"ừ": ["u","w","f"],
    "ử": ["u","w","r"],"ữ": ["u","w","x"],
    "ự": ["u","w","j"],"é": ["e","s"],
    "è": ["e","f"],"ẻ": ["e","r"],
    "ẽ": ["e","x"],"ẹ": ["e","j"],
    "ê": ["e","e"],"ế": ["e","e","s"],
    "ề": ["e","e","f"],"ể": ["e","e","r"],
    "ễ": ["e","e","x"],"ệ": ["e","e","j"],
    "ó": ["o","s"],"ò": ["o","f"],
    "ỏ": ["o","r"],"õ": ["o","x"],
    "ọ": ["o","j"],"ô": ["o","o"],
    "ố": ["o","o","s"],"ồ": ["o","o","f"],
    "ổ": ["o","o","r"],"ỗ": ["o","o","x"],
    "ộ": ["o","o","j"],"ơ": ["o","w"],
    "ớ": ["o","w","s"],"ờ": ["o","w","f"],
    "ở": ["o","w","r"],"ỡ": ["o","w","x"],
    "ợ": ["o","w","j"],'đ': ['d','d'],
    "ý": ["y","s"],"ỳ": ["y","f"],
    "ỷ": ["y","r"],"ỹ": ["y","x"],
    "ỵ": ["y","j"] 
    }
double_telex_pattern = ["ươ","ướ","ườ","ưở","ưỡ","ượ"]
single_telex_pattern = single_telex_composition.keys()

def remove_duplicate(mylist):
    return list(dict.fromkeys(mylist))

def load_vocab(path):
    """
    Load vocabulary list from txt file
    ----------
    Args:
        path: file path to vocab
    Returns:
        Python set of vocabulary
    """
    # assert os.exist(path), "Invalid path"

    vocab_list = []
    with open(path, "r") as vf:
        lines = vf.readlines()
        print(f"Reading file...")
        for line in lines:
            word = line.strip()
            vocab_list.append(word)
        # remove_duplicate(vocab_list)
        nw = len(vocab_list)
        print(f"Total {nw} word in vocab")
    return set(vocab_list)

def decompose_to_telex(word):
    """
    Decompose a word to telex components
    Args:
        word: Vietnamese word
    Returns:
        {
            base: str
            diact: str
            extra: str
        }
    """
    word_composition: TelexDict = {
        "base":  "",
        "diact": "",
        "extra": ""
    }
    
    for dtp in double_telex_pattern:
        if dtp in word:
            dtc = double_telex_composition[dtp]
            base, extra, diact = dtc[0], "", ""
            if len(dtc) == 3:
                extra = dtc[1]
                diact = dtc[2]
            else:
                if dtc[1] in "sfrxj":
                    diact = dtc[1]
                else:
                    extra = dtc[1]
            baseword = word.replace(dtp, base)
            word_composition["base"] = baseword
            word_composition["diact"] = diact
            word_composition["extra"] = extra
            return word_composition
    for dtp in single_telex_pattern:
        if dtp in word:
            dtc = single_telex_composition[dtp]
            base, extra, diact = dtc[0], "", ""
            if len(dtc) == 3:
                extra = dtc[1]
                diact = dtc[2]
            else:
                if dtc[1] in "sfrxj":
                    diact = dtc[1]
                else:
                    extra = dtc[1]
            baseword = word.replace(dtp, base)
            word_composition["base"] = baseword
            word_composition["diact"] = diact
            word_composition["extra"] = extra
            return word_composition
    return word_composition
        
def create_confusion_set(vocab: Dict[str, TelexDict], 
            heuristic_f: Callable[[TelexDict, TelexDict], bool],
            MAX_SET=100 ) -> Dict[str, List]:
    """
    Create a confusion set based on heuristiscal functions.
    ----------
    Args:
        vocab: list of vocabulary
        heuristic_f: (original, confuse) -> boolean
    Returns:
       Python dictionary, { "word": ["confusion", "set"], ... }
    """
    confusion_set = dict.fromkeys(vocab.keys())
    for word in confusion_set:
        confusion_list = []
        for another_word in vocab:
            if word == another_word: continue
            is_ok = heuristic_f(vocab[word], \
                            vocab[another_word])
            if is_ok: 
                confusion_list.append(another_word)
        confusion_set[word] = confusion_list
    return confusion_set




#################### HEURISTICS ####################

def m_edit_distance_1(word: TelexDict, another: TelexDict) -> bool:
    return minimum_edit_distance(word, another, 1)

def m_edit_distance_2(word: TelexDict, another: TelexDict) -> bool:
    return minimum_edit_distance(word, another, 2)


def minimum_edit_distance(word: TelexDict, another: TelexDict, max_edit_distance = 3) -> bool:
    base1, diact1, extra1 = word["base"], word["diact"], word["extra"]
    base2, diact2, extra2 = another["base"], another["diact"], another["extra"]
    edit_distance = DP5(base1, base2)
    if diact1 != diact2: edit_distance += 1
    if extra1 != extra2: edit_distance += 1
    return edit_distance < max_edit_distance

def DP5(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], 
                        distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]
