
# classifier-calibration

Python package to measure the calibration of probabilistic classifers. Calculates the classwise expected calibration error which returns the weighted average deviation from the expected rate of occurrence for predictions across all classes in multi-class classification problems.


# Example Usage

```import sklearn.datasets
import sklearn.linear_model
import sklearn.ensemble
import pandas as pd
import numpy as np
from classifier_calibration.calibration_error import classwise_ece  
```


### Binary classification 

```# Make classification data
X, Y = sklearn.datasets.make_classification(n_samples=100000,n_informative=6,n_classes=2) 
clf = sklearn.linear_model.LogisticRegression().fit(X,Y)
predicted_probabilities = clf.predict_proba(X)
calibration_loss = classwise_ece(pred_probs=predicted_probabilities,labels=Y)
print(calibration_loss)
```

### Multi-class classification 
We implement and compare calibration and accuracy of random forest and logistic regression classifiers for the 3-class classification problem


```
# Make classification data
num_classes = 3
X, Y = sklearn.datasets.make_classification(n_samples=100000,n_informative=6,n_classes=num_classes) 
lr = sklearn.linear_model.LogisticRegression().fit(X,Y)
rf = sklearn.ensemble.RandomForestClassifier().fit(X,Y)

lr_predicted_probabilities = lr.predict_proba(X)
rf_predicted_probabilities = rf.predict_proba(X)

lr_calibration_loss, lr_bin_weights = classwise_ece(pred_probs=lr_predicted_probabilities,labels=Y,return_weights=True)
rf_calibration_loss, rf_bin_weights = classwise_ece(pred_probs=rf_predicted_probabilities,labels=Y,return_weights=True)
print(round(100*lr_calibration_loss,2),'%',round(100*rf_calibration_loss,2),'%')

# print distribution of weights across bins for each class' set of predictions
for k in range(num_classes):
    print('Logistic regression bin weights for class',k,'predictions:')
    print(lr_bin_weights[k])
    print('Random forest bin weights for class',k,'predictions:')
    print(rf_bin_weights[k])
    print()
```
