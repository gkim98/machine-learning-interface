"""
    This will compile ideas from other model scripts into a general model that can take any features
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc
from sklearn import preprocessing

GRID_DEFAULT = {
    'C': [0.1,1, 10, 100, 1000], 
    'gamma': [1,0.1,0.01,0.001,0.0001], 
    'kernel': ['rbf']
} 


"""
    Trains and evaluates model based on given features
    
    input:
        - df: data for the model
        - pred_var: name of the target variable
        - cont_vars: continuous feature variables
        - cat_vars: categorical feature variables
        - algorithm: type of algorithm for training model (svm, rf, lr)
        - hyp_params: parameters for grid search
        - folds: folds for cross-validation
        - iterations: repititions of kfold cross-validation
    output:
        - F-score of model
        - dictionary of metrics
"""
def general_model(df, pred_var, cont_vars=[], cat_vars=[], algorithm='rf', folds=5, iterations=3):
    df = prepare_df(df, pred_var, cont_vars, cat_vars)

    avg_pos_prec = 0
    avg_pos_rec = 0
    avg_neg_prec = 0
    avg_neg_rec = 0
    auc_score = 0

    # maps algorithm parameter to algorithm function
    alg_map = {
        'svm': train_svm_model,
        'rf': train_rf_model,
        'lr': train_lr_model
    }

    # treats every non-target variable as a feature
    feat_vars = [var for var in list(df.columns) if var != pred_var]

    X = df[feat_vars].values
    y = df[pred_var].values

    # keeps track of feature importance/coefficients
    feat_info = np.zeros((1, len(df[feat_vars].columns)))

    rskf = RepeatedStratifiedKFold(n_splits=folds, n_repeats=iterations)
    for train_index, test_index in rskf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        (tn, fp, fn, tp), weights, temp_auc = alg_map[algorithm](X_train, y_train, X_test, y_test)

        if algorithm != 'svm' : feat_info += weights
        auc_score += temp_auc

        if (tp + fp) != 0: avg_pos_prec += tp / (tp + fp)
        avg_pos_rec += tp / (tp + fn)
        avg_neg_prec += tn / (tn + fn)
        avg_neg_rec += tn / (tn + fp)

    # calculates average precision and recall
    avg_pos_prec /= (folds * iterations)
    avg_pos_rec /= (folds * iterations)
    avg_neg_prec /= (folds * iterations)
    avg_neg_rec /= (folds * iterations)
    auc_score /= (folds * iterations)

    # gets average of weights and displays
    if algorithm != 'svm':
        if algorithm == 'lr' : weights = weights[0]
        feat_info /= (folds * iterations)
        feat_importance_df = pd.DataFrame({"Feature": df[feat_vars].columns, "Weight": np.transpose(weights)})

    # calculate fscore
    fscore = (2 * avg_pos_prec * avg_pos_rec) / (avg_pos_prec + avg_pos_rec)

    return fscore, auc_score, feat_importance_df



"""
    Model training for different algorithms
"""
# trains one iteration of svm model
def train_svm_model(X_train, y_train, X_test, y_test):
    # trains model
    model = GridSearchCV(SVC(), GRID_DEFAULT, refit=True)
    model.fit(X_train, y_train)

    # make predictions and evaluate
    predictions = model.predict(X_test)
    metrics = confusion_matrix(y_test, predictions).ravel()

    # finds AUC
    auc_score = calc_auc(y_test, predictions)

    return metrics, None, auc_score

# trains one iteration of random forest model
def train_rf_model(X_train, y_train, X_test, y_test):
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # displays feature importances
    feat_importances = model.feature_importances_

    predictions = model.predict(X_test)
    metrics = confusion_matrix(y_test, predictions).ravel()

    auc_score = calc_auc(y_test, predictions)

    return metrics, feat_importances, auc_score


# trains one iteration of 
def train_lr_model(X_train, y_train, X_test, y_test):
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # displays coefficients of the features
    coefficients = np.asarray(model.coef_)

    predictions = model.predict(X_test)
    metrics = confusion_matrix(y_test, predictions).ravel()

    auc_score = calc_auc(y_test, predictions)

    return metrics, coefficients, auc_score

# calculates auc
def calc_auc(y_test, predictions):
    fpr, tpr, _ = roc_curve(y_test, predictions, pos_label=1)
    auc_score = auc(fpr, tpr)
    return auc_score



"""
    Prepares a dataframe for general_model

    input:
        - df: untouched dataframe
        - target_var: target variable
        - cont_vars: continuous variables as list
        - cat_vars: categorical variables as list
    output:
        - dataframe ready to feed through general_model
"""
def prepare_df(df, target_var, cont_vars=[], cat_vars=[]):
    total_vars = cont_vars + cat_vars + [target_var]
    model_df = df[total_vars]
    cleaned_df = model_df.dropna(subset=total_vars)

    # turns categorical variables into dummy variables
    for var in cat_vars:
        temp_dummy = pd.get_dummies(cleaned_df[var], drop_first=True)
        cleaned_df = pd.concat([cleaned_df.drop([var], axis=1), temp_dummy], axis=1)

    # normalize the data
    for var in cont_vars:
        cleaned_df[var] = preprocessing.scale(cleaned_df[var])

    return cleaned_df