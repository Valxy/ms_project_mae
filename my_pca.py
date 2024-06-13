from sklearn.decomposition import PCA
import numpy as np
import numpy as np
from scipy.interpolate import interp1d

def fill_nans_with_interpolation(vector):
    
    nan_indices = np.where(np.isnan(vector))[0]

    if not nan_indices.size:
        return vector

    f = interp1d(np.arange(len(vector))[~np.isnan(vector)], vector[~np.isnan(vector)], kind='linear', bounds_error=False, fill_value="extrapolate")
    fill_value = np.nanmean(vector)

    vector[nan_indices] = fill_value


    return vector


def dot_without_nan(X1 ,X2):
    nan_indices = np.isnan(X1)
    #ratio = nan_indices.sum(axis = 1) / nan_indices.shape[1] + 1

    X2_filtered = X2[~nan_indices.any(axis=0), :]
    X1_filtered = X1[:, ~nan_indices.any(axis=0)]

    # result = np.dot(X1_filtered, X2_filtered) * ratio.reshape(-1,1)
    # result = np.dot(X1_filtered, X2_filtered) *200

    result = np.dot(X1_filtered, X2_filtered)
    # print(result)
    return result

def dot_with_fill_mean(X1 ,X2):
    nan_indices = np.isnan(X1)

    # X1_filtered = X1[:, ~nan_indices.any(axis=0)]
    s = np.nanmean(X1, axis=1)
    for i in  range(len(s)):
        X1[i,nan_indices[i]] =  s[i]
    print('111111')
    result = np.dot(X1, X2)
    return result

def dot_with_fill_interpolation(X1 ,X2):

    # X1_filtered = X1[:, ~nan_indices.any(axis=0)]
    for i in range(X1.shape[0]):
        X1[i, :] = fill_nans_with_interpolation(X1[i, :])
    print('dot_with_fill_interpolation')
    result = np.dot(X1, X2)
    return result


def dot_with_fill_row_mean(X1 ,X2):
    mask = np.isnan(X1)

    # X1_filtered = X1[:, ~nan_indices.any(axis=0)]
    # s = np.nanmean(X1, axis=1)
    # for i in  range(len(s)):
    #     X1[i,nan_indices[i]] =  s[i]
    image_means = np.nanmean(X1, axis=( 2))

    other_X_fill_with_mean = X1.copy()
    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            for k in range(X1.shape[3]):
                other_X_fill_with_mean[i, j, :, k][mask[i, j, :, k] == 1] = image_means[i, j,k]

    print('dot_with_fill_row_mean')
    result = np.dot(other_X_fill_with_mean, X2)
    return result

class MyPCA(PCA):
    def transform(self, X):
        if self.mean_ is not None:
            X = X - self.mean_
        X_transformed = dot_without_nan(X , self.components_.T)
        # X_transformed = np.dot(X, self.components_.T)
        if self.whiten:
            X_transformed /= np.sqrt(self.explained_variance_)
        return X_transformed



