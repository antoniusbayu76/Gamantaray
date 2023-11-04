import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets

bunga = datasets.load_iris()

x = bunga.data[:, :2]
y = bunga.target

cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

knn = neighbors.KNeighborsClassifier(n_neighbors=6,weights='uniform')
knn.fit(x,y)

x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min,x_max), np.arange(y_min,y_max))

z = knn.predict(np.c_[xx.ravel(),yy.ravel()])
z = z.reshape(xx.shape)
plt.figure()
plt.pcolormesh(xx,yy,z,cmap=cmap_light)


plt.scatter(x[:, 0], x[:, 1], c=y, cmap=cmap_bold,edgecolor='k',s=20)
plt.xlim(xx.min(),xx.max())
plt.ylim(yy.min(),yy.max())
plt.title("Klasifikasi Bunga Iris")
plt.show()