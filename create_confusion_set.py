from utils import *



if __name__ == "__main__":

    full_vocab = load_vocab("./all-vietnamese-syllables.txt")
    common_vocab = load_vocab("./common-vietnamese-syllables.txt")
    full_vocab_telex_dict = {x: decompose_to_telex(x) for x in full_vocab}
    create_confusion_set(full_vocab_telex_dict, m_edit_distance_1, MAX_SET=50)