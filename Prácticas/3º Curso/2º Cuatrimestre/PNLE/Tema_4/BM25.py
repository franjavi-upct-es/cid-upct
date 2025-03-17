#IMPLEMENTACIÓN DEL BM25 - OKAPI
# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted
from sklearn.feature_extraction.text import _document_frequency
from sklearn.preprocessing import normalize

class BM25Transformer(TfidfTransformer):
    """
    Parameters
    ----------
    use_idf : boolean, optional (default=True)
    k1 : float, optional (default=1.2)
    b : float, optional (default=0.75)
    References
    ----------
    Okapi BM25: a non-binary model - Introduction to Information Retrieval
    http://nlp.stanford.edu/IR-book/html/htmledition/okapi-bm25-a-non-binary-model-1.html
    """
    def __init__(self,k=1.2,b=0.75, norm="l2", use_idf=True, smooth_idf=True,
                 sublinear_tf=False):
        self.k = k
        self.b = b
        ######### tfidf ###########
        self.norm = norm
        self.use_idf = use_idf
        self.smooth_idf = smooth_idf
        self.sublinear_tf = sublinear_tf

    def fit(self, X, y=None):
        """Learn the idf vector (global term weights)

        Parameters
        ----------
        X : sparse matrix, [n_samples, n_features]
            a matrix of term/token counts
        """
        XA = X.toarray()
        self.avdl = XA.sum()/XA.shape[0] 

        super().fit(X)
        return self

    def transform(self, X, copy=True):
        """Transform a count matrix to a tf or tf-idf representation.

        Parameters
        ----------
        X : sparse matrix of (n_samples, n_features)
            A matrix of term/token counts.

        copy : bool, default=True
            Whether to copy X and operate on the copy or perform in-place
            operations.

        Returns
        -------
        vectors : sparse matrix of shape (n_samples, n_features)
            Tf-idf-weighted document-term matrix.
        """
        cur_tf =  X.toarray() #[N,M] 
        norm_lenght = 1 - self.b + self.b*(X.toarray().sum(-1)/self.avdl) #[N] #N表示数据的条数
        norm_lenght = norm_lenght.reshape([norm_lenght.shape[0],1]) #[N,1]
        X = (self.k+1)*cur_tf /(cur_tf +self.k*norm_lenght)

        if not sp.issparse(X):
            X = sp.csr_matrix(X, dtype=np.float64)

        if self.sublinear_tf:
            np.log(X.data, X.data)
            X.data += 1

        if self.use_idf:
            # idf_ being a property, the automatic attributes detection
            # does not work as usual and we need to specify the attribute
            # name:
            check_is_fitted(self, attributes=["idf_"], msg="idf vector is not fitted")

            # *= doesn't work
            X = X.multiply(self.idf_)

        if self.norm:
            X = normalize(X, norm=self.norm, copy=False)

        return X