import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from django.shortcuts import render
from main.models import Task
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import VotingRegressor
from sklearn.model_selection import train_test_split
from django.contrib.auth.decorators import login_required

@login_required(login_url='log_in')
def predict_completion_time(request):
    # Fetching tasks data
    tasks = Task.objects.filter(isDelete=False)

    # Creating a DataFrame
    dic = {
        "estimated_time": [task.estimated_time for task in tasks if task.estimated_time is not None],
        "complexity": [task.complexity for task in tasks if task.complexity is not None],
        "actual_time": [task.actual_time for task in tasks if task.actual_time is not None]
    }

    df = pd.DataFrame(dic)

    # Checking if DataFrame is not empty
    if df.empty:
        return render(request, "prediction/predict_completion.html", {"error": "No task data available for prediction."})

    # Preparing features (X) and target (y)
    x = df.iloc[:, :-1]
    y = df["actual_time"]

    # Splitting the data
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=42)

    # Models
    lr = LinearRegression()
    kn = KNeighborsRegressor(n_neighbors=3)
    sv = SVR(kernel="linear")

    # Training models
    lr.fit(x_train, y_train)
    kn.fit(x_train, y_train)
    sv.fit(x_train, y_train)

    # Voting Regressor
    prd = [("lr", lr), ("knn", kn), ("sv", sv)]
    vc = VotingRegressor(estimators=prd, weights=[8, 5, 1])
    vc.fit(x_train, y_train)

    train_score = vc.score(x_train, y_train) * 100
    test_score = vc.score(x_test, y_test) * 100
    
    print(train_score,test_score)

    if request.method == "POST":
        estimated_time = float(request.POST.get("estimated_time"))
        complexity = float(request.POST.get("complexity"))
        
        # Convert input data to DataFrame to retain feature names
        input_data = pd.DataFrame([[estimated_time, complexity]], columns=x.columns)

        # Predicting the completion time
        predicted_time = vc.predict(input_data)[0]

        context = {
            'predicted_time': predicted_time,
            'train_score': train_score,
            'test_score': test_score,
        }
        return render(request, "prediction/predict_completion.html", context)

    return render(request, "prediction/predict_completion.html")
