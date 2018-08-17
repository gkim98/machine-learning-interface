# Classification Model Interface
When I was trying to find the optimal set of features for a classification model, I found myself plugging them in manually one-by-one. So I decided to create an interface for scikit-learn that will automatically train and evaluate models on different sets of features.

![alt text](/img/classification_interface.png)

## Future Work
* capabilities for hyperparameter tuning
* more flexibility in defining feature subsets
* cross-validation options