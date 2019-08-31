from gensim.models import KeyedVectors
import numpy as np
from nltk.corpus   import stopwords
from nltk.tokenize import word_tokenize



class QueryExpansion:
    """Pre-retrieval kNN based approach for query expansion.
    Args:
        stopwords (list): List of words, that we want to remove from the tokenized text.
        wv (Word2VecKeyedVectors): Word embeddings.
    """

    def __init__(self, stopwords, wv):
        self.stopwords = stopwords
        self.wv = wv

    def tokenize(self, text):
        """Tokenizes, lowers words and removes stopwords from the document.
        Args:
            text (str): Text that we want to tokenize. 
        Returns:
            filtered_tokens (list): List of low case tokens wich does not contain stop words.
        """
        tokens = word_tokenize(text)
        filtered_tokens = [w.lower() for w in tokens if not w in self.stopwords]
        return filtered_tokens

    def extend_tokens(self, token_list):
        """Extends token list summing consecutive vector pairs.
        Args: 
            token_list (list): List of tokens that we want to extend.
        Returns:
            extension (list): List of extensions.
        """
        tokens = []
        for token in token_list:
            # check if the token is in the vocabulary
            if token in self.wv.vocab.keys():
                tokens.append(token)
        extension = set()
        for i in range(len(tokens)-1):
            new_token = self.wv.most_similar(positive=[tokens[i], tokens[i+1]])[0][0]
            extension.add(new_token)
        extension = list(extension)
        return extension
 
    def get_candidate_expansion_terms(self, tokens, k):
        """Gets the candidates for expansions based on kNN.
        Args: 
            tokens (list): List of tokens that we want to expand.
            k (int): Number of nearest neighbours.
        Returns:
            candidates (list): List of candidates.
        """
        candidates = set()
        for token in tokens:
            # check if the token is in the vocabulary
            if token in self.wv.vocab.keys():
                result = self.wv.similar_by_word(token)
                limit = k if len(result) > k else len(result)
                # iterate through the most similar words
                for i in range(limit):
                    candidates.add(result[i][0])
        # return list of candidates
        candidates = list(candidates)
        return candidates


    def similarity(self, token, token_list):
        """Calculates the similarity between token and list of tokens.
        Args: 
            token (str): String for wich we are calculating similarity.
            token_list (list): List of tokens to wich we are calculating similarity of token.
        Returns:
            avreage_similarity (float): Number that signifes the similarity of token to token list words.
        """
        similarity = 0
        num_of_tokens = 0
        for toks in token_list:
            # check if the token is in the vocabulary
            if toks in self.wv.vocab.keys():
                num_of_tokens += 1
                similarity += self.wv.similarity(toks, token)
        avreage_similarity = similarity/num_of_tokens
        return avreage_similarity

    def get_similarity_pairs(self,tokens, candidates):
        """Calculates similarity to tokens for list of candidates.
        Args: 
            tokens (list): List of tokens to wich similarity is calculated
            candidates (list): List of tokens for wich similarity is calculated.
        Returns:
            similarity_pairs (list): List of tuples. Tuples are pairs of candidates and their similarity to tokens.
        """
        similarity_pairs = []
        for candidate in candidates:
            sim = self.similarity(candidate, tokens)
            similarity_pairs.append((candidate, sim))
        # return the list of expansion terms with their similarities
        return similarity_pairs

    def pre_retrieval_KNN(self, query, k, n):
        """Find n most similar tokens to the given query
        Args: 
            query (string): User query we want to expand.
            wv (): 
            n (int): Number of candidates (with the highest simiarity) that is returned.
        Returns:
            similarity_pairs (list): List of n similarity pairs with the highest similarity to query tokens.
        """
        tokens = self.tokenize(query)
        candidates = self.get_candidate_expansion_terms(tokens, k)
        candidates_sim = self.get_top_expansion_terms(tokens, candidates)
        def takeSecond(elem):
            return elem[1]
        sort = sorted(candidates_sim, key=takeSecond)[::-1]
        return sort[:n]