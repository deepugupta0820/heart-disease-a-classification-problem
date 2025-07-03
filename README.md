# HeartDiseasePrediction-using-various-ML_Algorithms

## Introduction

This project is a machine learning-based web application designed to predict the risk of heart disease using various classifiers. Patients can enter basic health parameters such as age, gender, chest pain type, cholesterol level, and other medical information.

The web app also allows users to generate and print a diagnostic report, making it easy to track and share health status over time.

## Exploratory Analysis

The dataset included 13 predictor variables: Age, Sex, Chest pain type, Resting blood pressure, Serum cholestoral, Fasting blood sugar, Resting electrocardiographic results, Maximum heart rate achieved, Exercise induced angina, Oldpeak, The slope of the peak exercise ST segment, Number of major vessels , Thal. Key observations from exploratory analysis:

- No NaN(missing) values were found in the dataset.
- Some duplicates were found in the dataset and were removed.
- Outliers were detected and capped to minimize their impact on the analysis.

## Classifier Scores

| Classifier                   | Score     |
|------------------------------|-----------|
| Logistic Regression          | 0.901639  |
| KNN Classifier               | 0.704918  |
| Support Vector Classifier    | 0.852459  |
| Decision Trees Classifier    | 0.786885  |
| Random Forest Classifier     | 0.868852  |

## Conclusion

The Logistic Regression achieved the highest accuracy of 90.16% and then Random Forest Classifier of 86.88% accuracy. This indicates that the Logistic Regression and Random Forest are well-suited for predicting heart disease based on the features included in our dataset.
