"""Defines a simple search engine for the Reuters-21578 corpus.

(!!!) DO NOT CHANGE ANY CODE IN THIS FILE. (!!!)
"""
from threading import Thread
import part1_sols as p1
import part3_sols as p3
import part4_sols as p4

from corpus import Corpus

class SearchEngine(object):
    """Simple search engine class for the Reuters-21578 corpus.

    This is a thin wrapper around the Corpus class that calls on functions
    from the lab exercises to implement search functionality.
    """

    def __init__(self):
        """Caches the vectorized corpus."""
        self._corp = Corpus()
        self._approx_docs = {}
        self._doc_ids = {}
        self._one_vs_one_classifier = None

    def approx_doc_matrices(self):
        """Performs latent semantic analysis on each training category doc matrix.

        Each approximation is calculated on a separate thread.
        """
        threads = []
        for category in Corpus.all_categories():
            approx_thread = Thread(target=self._approx_doc_matrix, args=(category,))
            approx_thread.start()
            threads.append(approx_thread)
        
        # Wait on each thread.
        for approx_thread in threads:
            approx_thread.join()

    def _approx_doc_matrix(self, category):
        """Launches k-rank approximation for given category matrix."""
        category_data = self._corp.complete_matrix(category, include_ids=True)
        self._doc_ids[category] = category_data[0]
        self._approx_docs[category] = p1.k_rank_approximate(
            category_data[1], SearchEngine._compute_rank_reduction(category_data[1]))

    @staticmethod
    def _compute_rank_reduction(matrix):
        """Utility method for determining the appropriate rank reduction.

        Args:
            matrix: The (n, m) matrix to rank-reduce.abs

        Returns:
            The smaller of 1/3 * m and 300.
        """
        return min(matrix.shape[0] / 3, 300)

    def train_classifiers(self):
        """Delegates to the toolbox to train each category classifier."""
        self._one_vs_one_classifier = p3.train_one_vs_one_classifier(self._approx_docs)

    def search(self, query):
        """Finds 5 distinct documents that match the query.

        Args:
            query: The user's input query.

        Returns:
            A list of 5 (id, document) tuples that best match the query.

        Raises:
            Exception if classifiers not yet trained.
        """
        return p4.find_closest_documents(
            self._corp.vectorize(query),
            self._one_vs_one_classifier,
            self._approx_docs,
            self._doc_ids)
