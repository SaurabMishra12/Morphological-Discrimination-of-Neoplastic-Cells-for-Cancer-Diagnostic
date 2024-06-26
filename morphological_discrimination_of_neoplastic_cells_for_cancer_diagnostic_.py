# -*- coding: utf-8 -*-
"""Morphological Discrimination of Neoplastic Cells for Cancer Diagnostic..ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oBvjifE53r9xJmme-N2HVTebGgk1DfYg

## **Morphological Discrimination of Neoplastic Cells for Cancer Diagnostic.**

*Early diagnosis of cancer focuses on detecting symptomatic patients as early as possible so they have the best chance for successful treatment. When cancer care is delayed or inaccessible there is a lower chance of survival, greater problems associated with treatment and higher costs of care. Early diagnosis improves cancer outcomes by providing care at the earliest possible stage and is therefore an important public health strategy in all settings.*
                         **-source WHO**


 Here, we are building and training a model using human cell records, and classify cells to whether the samples are benign or malignant.
"""

# Commented out IPython magic to ensure Python compatibility.
#importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from sklearn.model_selection import train_test_split
import scipy.optimize as opt
from sklearn import preprocessing
# %matplotlib inline
import seaborn as sns

"""# Loading the Dataset

The dataset used here is publicly available from the UCI Machine Learning Repository (Asuncion and Newman, 2007)[http://mlearn.ics.uci.edu/MLRepository.html]. The dataset consists of several hundred human cell sample records, each of which contains the values of a set of cell characteristics. The fields in each record are:

|Field name|Description|
|--- |--- |
|ID|Clump thickness|
|Clump|Clump thickness|
|UnifSize|Uniformity of cell size|
|UnifShape|Uniformity of cell shape|
|MargAdh|Marginal adhesion|
|SingEpiSize|Single epithelial cell size|
|BareNuc|Bare nuclei|
|BlandChrom|Bland chromatin|
|NormNucl|Normal nucleoli|
|Mit|Mitoses|
|Class|Benign or malignant|

<br>
<br>
"""

cell_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/Module%203/data/cell_samples.csv")
cell_df.head(11)

sns.scatterplot(x="UnifShape", y="UnifSize", hue="Class", data=cell_df)

ax = cell_df[cell_df['Class'] == 4][0:50].plot(kind='scatter', x='Clump', y='UnifSize', color='DarkBlue', label='malignant');
cell_df[cell_df['Class'] == 2][0:50].plot(kind='scatter', x='Clump', y='UnifSize', color='Yellow', label='benign', ax=ax);
plt.show()

"""## Data pre-processing and selection"""

cell_df.dtypes

# converting object to int64
cell_df = cell_df[pd.to_numeric(cell_df['BareNuc'], errors='coerce').notnull()]
cell_df['BareNuc'] = cell_df['BareNuc'].astype('int')
cell_df.dtypes

feature_df = cell_df[['Clump', 'UnifSize', 'UnifShape', 'MargAdh', 'SingEpiSize', 'BareNuc', 'BlandChrom', 'NormNucl', 'Mit']]
X = np.asarray(feature_df)
X[0:5]

y = np.asarray(cell_df['Class'])
y [0:5]

"""## Train/Test dataset"""

X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=4)
print ('Train set:', X_train.shape,  y_train.shape)
print ('Test set:', X_test.shape,  y_test.shape)

"""# **Modeling**"""

from sklearn import svm
clf = svm.SVC(kernel='rbf')
clf.fit(X_train, y_train)

yhat = clf.predict(X_test)
yhat [0:5]

"""<h2 id="evaluation">Evaluation</h2>"""

from sklearn.metrics import classification_report,confusion_matrix
import itertools

def plot_confusion_matrrix(cm,classes,normalize =False,title='Confusion matrix,cmap=plt.cm.Blues'):
    if normalize:
        cm= cm.astype('float') / cm.sum(axis=1)[:,np.newaxis]
        print("Normalized confusion Matrix")
    else:
        print('Confusion Matrix, without normalization')
    print(cm)

    plt.imshow(cm,interpolation='nearest',cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks,classes,rotation=45)
    plt.yticks(tick_marks,classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

#compute confusion matrix
cnf_matrix =confusion_matrix(y_test,yhat,labels=[2,3])

np.set_printoptions(precision=2)

print(classification_report(y_test,yhat))

#plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrrix(cnf_matrix,classes=['Benign(2)','Malignant(3)'],normalize=False,title='Confusion matrix')

from sklearn.metrics import f1_score
f1_score(y_test, yhat, average='weighted')

from sklearn.metrics import jaccard_score
jaccard_score(y_test, yhat,pos_label=2)

#setting kernel =linear
clf2 =svm.SVC(kernel='linear')
clf2.fit(X_train,y_train)
yhat2=clf2.predict(X_test)
from sklearn.metrics import jaccard_score
jaccard_score(y_test, yhat,pos_label=2)

#setting kernel =sigmoid
clf3 =svm.SVC(kernel='sigmoid')
clf3.fit(X_train,y_train)
yhat2=clf3.predict(X_test)
from sklearn.metrics import jaccard_score
jaccard_score(y_test, yhat,pos_label=2)

from sre_constants import SUCCESS

import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed
import pandas as pd

# Define the prediction function
def predict(Clump, UnifSize, UnifShape, MargAdh, SingEpiSize, BareNuc, BlandChrom, NormNucl, Mit):
  # Convert the input data to a NumPy array
  input_data = np.asarray([[Clump, UnifSize, UnifShape, MargAdh, SingEpiSize, BareNuc, BlandChrom, NormNucl, Mit]])

  # Predict the class
  prediction =clf.predict(input_data)

  #prediction interface
  if prediction[0] == 2:
    return "Benign"
  else:
    return "Malignant"

# Creating the dashboard
interact(predict, Clump=(1, 10), UnifSize=(1, 10), UnifShape=(1, 10), MargAdh=(1, 10), SingEpiSize=(1, 10), BareNuc=(1, 10), BlandChrom=(1, 10), NormNucl=(1, 10), Mit=(1, 10))

#saving the model

import pickle

# Save the model to a file
with open('cell_model.pkl', 'wb') as f:
  pickle.dump(clf, f)

# Load the model from the file
with open('cell_model.pkl', 'rb') as f:
  loaded_model = pickle.load(f)



"""# New section"""