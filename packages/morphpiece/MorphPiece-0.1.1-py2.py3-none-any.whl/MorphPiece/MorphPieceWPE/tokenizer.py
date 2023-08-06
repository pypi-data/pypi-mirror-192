from transformers import BertTokenizer, WordpieceTokenizer
from transformers.models.bert.tokenization_bert import load_vocab
import pickle
from transformers.utils import logging
from pathlib import Path

logger = logging.get_logger(__name__)
path = Path(__file__).parent

class MorphPieceWPE(BertTokenizer):

    def __init__(
        self,
        vocab_file=path/'with_morph_vocab.txt',
        no_morph_vocab=path/'no_morph_vocab.txt',
        lookup_table=path/'lookup_dict.pkl',
        do_lower_case=True,
        do_basic_tokenize=True,
        never_split=None,
        unk_token="[UNK]",
        sep_token="[SEP]",
        pad_token="[PAD]",
        cls_token="[CLS]",
        mask_token="[MASK]",
        tokenize_chinese_chars=True,
        strip_accents=None,
        **kwargs,
    ):
        super().__init__(
            vocab_file=vocab_file,
            do_lower_case=do_lower_case,
            do_basic_tokenize=do_basic_tokenize,
            never_split=never_split,
            unk_token=unk_token,
            sep_token=sep_token,
            pad_token=pad_token,
            cls_token=cls_token,
            mask_token=mask_token,
            tokenize_chinese_chars=tokenize_chinese_chars,
            strip_accents=strip_accents,
            **kwargs,
        )

        self.no_morph_vocab = load_vocab(no_morph_vocab) # Haris
        self.morpheme_table = pickle.load(open(lookup_table,'rb')) # Haris
        self.morphpiece_tokenizer = WordpieceTokenizer(vocab=self.no_morph_vocab, unk_token=self.unk_token)
        
        self.counter_morph = dict.fromkeys(self.morpheme_table,0) # Haris
        self.counter_bpe = dict() # Haris
        self.counter_token = dict() # Haris
        self.counter_nonsplit = dict() # Haris

    def _tokenize(self, text):
        split_tokens = []
        if self.do_basic_tokenize:
            for token in self.basic_tokenizer.tokenize(text, never_split=self.all_special_tokens):

                morph_splits = self.morpheme_table.get(token,None) # Haris
                
                # If the token is part of the never_split set
                if token in self.basic_tokenizer.never_split:
                    split_tokens.append(token)
                elif morph_splits is not None: # Haris
                    split_tokens.extend(morph_splits) # Haris
                else:
                    split_tokens += self.morphpiece_tokenizer.tokenize(token)
        else:
            morph_splits = self.morpheme_table.get(token,None) # Haris
            if morph_splits is not None: # Haris
                split_tokens.extend(morph_splits) # Haris
            else: # Haris
                split_tokens = self.morphpiece_tokenizer.tokenize(text)
        return split_tokens