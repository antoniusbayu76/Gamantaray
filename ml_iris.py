import pandas as pd #manipulasi data
import matplotlib.pyplot as plt #grafik
import sklearn #dataset
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier

bunga = datasets.load_iris()

#memanggil dataset
# print(type(bunga))
# print(bunga.keys())
# print(type(bunga.data), type(bunga.target))
# print(bunga.data.shape)
# print(bunga.target_names)

x = bunga.data #training dataset
y = bunga.target #target dataset
df = pd.DataFrame(x, columns=bunga.feature_names) #konversi dataset ke dataframe
print(df.head())

#memanggil KNN Classifier
knn = KNeighborsClassifier(n_neighbors=6,weights='uniform',algorithm='auto', metric='euclidean')
#Fitting model
x_train = bunga['data']
y_train = bunga['target']
knn.fit(x_train,y_train)

#Melakukan prediksi
Data = [[5.2, 3.6, 1.6, 0.4]] #data yang akan diprediksi (panjang sepal,lebar sepal,panjang petal,lebar petal)
y_pred = knn.predict(Data) #dasar prediksi
print("Hasil Prediksi : Jenis Bunga ", y_pred) #0(Setosa) 1(Versicolor) 2(Virginica)

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------