import numpy as np

class RotationEffect():

    @classmethod
    def rotate(cls, image, angle):
        image_ = np.zeros_like(image)
        
        Xd = cls.criar_indices(0, image.shape[0], 0, image.shape[1])
        Xd = np.vstack ( (Xd, np.ones( Xd.shape[1]) ))

        R = cls.rotation_matrix(angle)
        T = np.array([[1, 0, -1*image.shape[0]/2], [0, 1, -1*image.shape[1]/2], [0, 0, 1]])
        T2 = np.array([[1, 0, image.shape[0]/2], [0, 1, image.shape[1]/2], [0, 0, 1]])

        X = T2 @ np.linalg.inv(R) @ T @ Xd

        Xd = Xd.astype(int)
        X = X.astype(int)

        filtro = (X[0,:] < image_.shape[0]) & (X[0,:] >= 0)  & (X[1,:] < image_.shape[1]) & (X[1,:] >= 0)
        Xd = Xd[:, filtro]
        X = X[:, filtro]

        image_[Xd[0,:], Xd[1,:], :] = image[X[0,:], X[1,:], :]  

        return image_
        
    

    def criar_indices(min_i, max_i, min_j, max_j):
        import itertools
        L = list(itertools.product(range(min_i, max_i), range(min_j, max_j)))
        idx_i = np.array([e[0] for e in L])
        idx_j = np.array([e[1] for e in L])
        idx = np.vstack( (idx_i, idx_j) )
        return idx
    
    def rotation_matrix(angle):
        import math
        angle = math.radians(angle)
        R = np.array([[math.cos(angle), -math.sin(angle), 0], [math.sin(angle), math.cos(angle), 0], [0, 0, 1]])
        return R