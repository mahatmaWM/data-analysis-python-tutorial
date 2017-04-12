import os
import numpy as np
from scipy.linalg import orth


class PPCA():
    def __init__(self):
        self.rawdata = None
        self.newdata = None
        self.W = None
        self.means = None
        self.stds = None

    def _standardize(self, X):
        if self.means is None or self.stds is None:
            raise RuntimeError("Fit model first")
        return (X - self.means) / self.stds

    def fit(self, data, d=None, tol=1e-10, min_obs=1, verbose=False):
        # step1：根据min_obs来决定需要保留下来的维度
        self.rawdata = data
        self.rawdata[np.isinf(self.rawdata)] = np.max(self.rawdata[np.isfinite(self.rawdata)])
        valid_columns = np.sum(~np.isnan(self.rawdata), axis=0) >= min_obs
        data = self.rawdata[:, valid_columns].copy()
        N = data.shape[0]
        D = data.shape[1]

        # step2：按列标准化剩余数据，并将缺省值赋值0
        self.means = np.nanmean(data, axis=0)
        self.stds = np.nanstd(data, axis=0)
        data = self._standardize(data)
        observed = ~np.isnan(data)
        missing = np.sum(~observed)
        data[~observed] = 0

        # 初始化，并计算正向变换、反向变换后的误差，以此决定效果
        if d is None:
            d = data.shape[1]

        if self.W is None:
            W = np.random.randn(D, d)
        else:
            W = self.W
            
        WTW = np.dot(W.T, W)
        X = np.dot(np.dot(data, W), np.linalg.inv(WTW))
        recon = np.dot(X, W.T)
        recon[~observed] = 0
        # ss评价重构回去的误差
        ss = np.sum((recon - data) ** 2) / (N * D - missing)

        v0 = np.inf
        counter = 0

        # 开始EM迭代
        while True:
            # print(WTW, ss)
            M_inv = np.linalg.inv(np.eye(d) + WTW / ss)

            # e-step
            ss0 = ss
            if missing > 0:
                proj = np.dot(X, W.T)
                data[~observed] = proj[~observed]
            X = np.dot(np.dot(data, W), M_inv) / ss

            # m-step
            XX = np.dot(X.T, X)
            W = np.dot(np.dot(data.T, X), np.linalg.pinv(XX + N * M_inv))  # pseudo-inverse
            WTW = np.dot(W.T, W)
            recon = np.dot(X, W.T)
            recon[~observed] = 0
            ss = (np.sum((recon - data) ** 2) + N * np.sum(WTW * M_inv) + missing * ss0) / (N * D)

            # check convergence
            det = np.log(np.linalg.det(M_inv))
            if np.isinf(det):
                det = np.abs(np.linalg.slogdet(M_inv)[1])
            v1 = N * (D * np.log(ss) + np.trace(M_inv) - det) + np.trace(XX) - missing * np.log(ss0)
            diff = np.abs(v1 / v0 - 1)
            if verbose:
                print(diff)
            if (diff < tol) and (counter > 5):
                break

            counter += 1
            v0 = v1

        # 迭代完成，为准备输出结果
        W = orth(W)
        vals, vecs = np.linalg.eig(np.cov(np.dot(data, W).T))
        order = np.flipud(np.argsort(vals))
        vecs = vecs[:, order]
        vals = vals[order]

        W = np.dot(W, vecs)

        # attach objects to class
        self.W = W
        self.newdata = data
        self.eig_vals = vals
        self._calc_var()

        # import IPython
        # IPython.embed()
        # assert False

    def transform(self, data=None):
        if self.W is None:
            raise RuntimeError('Fit the data model first.')
        if data is None:
            return np.dot(self.newdata, self.W)
        return np.dot(data, self.W)

    def _calc_var(self):
        if self.newdata is None:
            raise RuntimeError('Fit the data model first.')

        data = self.newdata.T

        # variance calc
        var = np.nanvar(data, axis=1)
        total_var = var.sum()
        self.var_exp = self.eig_vals.cumsum() / total_var

    def save(self, fpath):
        np.save(fpath, self.W)

    def load(self, fpath):
        assert os.path.isfile(fpath)
        self.W = np.load(fpath)

    def getnewdata(self):
        return self.newdata


from sklearn import decomposition
from sklearn import datasets

np.random.seed(5)
iris = datasets.load_iris()
X = iris.data
# print(X)
# pca = decomposition.PCA(n_components=3)
# pca.fit(X)
# X = pca.transform(X)
# print(X)

X_with_miss = X.copy()
X_with_miss[X_with_miss == 2.5] = np.nan
# print(X_new)



ppca = PPCA()
ppca.fit(X_with_miss, d=3, min_obs=5, verbose=0)
X_with_miss = ppca.transform()
print(X_with_miss)
