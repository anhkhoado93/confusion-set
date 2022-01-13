from utils import *
import pickle
import os


if __name__ == "__main__":
    cwd = os.getcwd()
    fvp = os.path.join(cwd, "confusion-set/all-vietnamese-syllables.txt")
    fvp2 = os.path.join(cwd, "confusion-set/common-vietnamese-syllables.txt")
    full_vocab = load_vocab(fvp)
    common_vocab = load_vocab(fvp2)
    full_vocab_telex_dict = {x: decompose_to_telex(x) for x in full_vocab}
    a = create_confusion_set(full_vocab_telex_dict, m_edit_distance_1, MAX_SET=50)
    with open('confusion_set.pickle', 'wb') as handle:
        pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)
