# coding=utf-8
# Copyright 2018 The Open AI Team Authors and The HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tokenization class for MorphPiece"""

import pickle
import regex as re
from transformers import GPT2Tokenizer
from transformers.utils import logging
from pathlib import Path

logger = logging.get_logger(__name__)
path = Path(__file__).parent

class MorphPieceBPE(GPT2Tokenizer):

    def __init__(
        self,
        vocab_file=path/'single_hash_vocab.json',
        merges_file=path/'single_hash_merges.txt',
        morpheme_file=path/'lookup_table_with_hash_single.pkl',
        errors="replace",
        unk_token="<|endoftext|>",
        bos_token="<|endoftext|>",
        eos_token="<|endoftext|>",
        pad_token=None,
        add_prefix_space=False,
        add_bos_token=False,
        **kwargs
    ):
        super().__init__(
        vocab_file,
        merges_file,
        errors,
        unk_token,
        bos_token,
        eos_token,
        pad_token,
        add_prefix_space,
        add_bos_token,
        **kwargs
        )
        
        self.morpheme_table, self.morpheme_vocab = pickle.load(open(morpheme_file,'rb')) # Haris
        self.counter_morph = dict.fromkeys(self.morpheme_table,0) # Haris
        self.counter_bpe = dict() # Haris
        self.counter_token = dict() # Haris
        self.counter_nonsplit = dict() # Haris

    def get_byte_encoding(self,token):
        return "".join(
            self.byte_encoder[b] for b in token.encode("utf-8")
        )  # Maps all our bytes to unicode strings, avoiding control tokens of the BPE (spaces in our case)
        
    def _get_bpe(self,token):
        byte_encoded_token = self.get_byte_encoding(token)
        return [bpe_token for bpe_token in self.bpe(byte_encoded_token).split(" ")]
        
    def reset_counters(self):
        self.counter_morph = dict.fromkeys(self.morpheme_table,0)
        self.counter_bpe = dict()
        self.counter_token = dict()
        self.counter_nonsplit = dict()

    def _tokenize(self, text):
        """Tokenize a string."""
        all_tokens = []
        
        pretokens = re.findall(self.pat, text)
        
        for token in pretokens:
            token_without_space = token.strip()

            if token_without_space in self.counter_token:
                self.counter_token[token_without_space]+=1
            else:
                self.counter_token[token_without_space]=1

            morph_splits = self.morpheme_table.get(token_without_space,token) # Haris
            
            if isinstance(morph_splits,list): # We got morphemes. Haris
                self.counter_morph[token_without_space] += 1 # Haris
                morph_tokens=[]
                for morpheme in morph_splits:
                    # Add space to the beginning of the morpheme if it is the first morpheme and 
                    # the original token had a space
                    # morpheme = " " + morpheme if token.startswith(" ") and i==0 else morpheme
                    byte_encoded_morpheme = self.get_byte_encoding(morpheme)
                    morph_tokens.append(byte_encoded_morpheme)
                all_tokens.extend(morph_tokens) 
            else:
                assert token == morph_splits # Haris
                bpe_tokens = self._get_bpe(token)
                if len(bpe_tokens) > 1:
                    if token_without_space in self.counter_bpe:
                        self.counter_bpe[token_without_space]+=1
                    else:
                        self.counter_bpe[token_without_space]=1
                else:
                    byte_token = self.get_byte_encoding(token)
                    if byte_token in self.counter_nonsplit:
                        self.counter_nonsplit[byte_token]+=1
                    else:
                        self.counter_nonsplit[byte_token]=1   
                all_tokens.extend(bpe_tokens)
                
        return all_tokens 

if __name__ == "__main__":
    tokenizer = MorphpieceBPE()
    text = "This is a test."
    print(tokenizer.tokenize(text))
    print(tokenizer.counter_morph)
    print(tokenizer.counter_bpe)
    print(tokenizer.counter_token)
    print(tokenizer.counter_nonsplit)