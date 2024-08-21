import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models  import Task


@login_required(login_url='log_in')
def predict_completion_time(request):
    # Load tasks data from the database
    tasks = Task.objects.filter(isDelete=False)
    
    # Create a DataFrame for the regression model
    data = {
        'estimated_time': [task.estimated_time for task in tasks],
        'complexity': [task.complexity for task in tasks],
        'actual_time': [task.actual_time for task in tasks if task.actual_time is not None]
    }

    # Only include tasks that have actual times recorded
    df = pd.DataFrame(data).dropna()

    # If there's enough data, train the model
    if not df.empty:
        reg = LinearRegression()
        reg.fit(df[['estimated_time', 'complexity']], df['actual_time'])

        # Predict completion time based on form inputs (or any specific task data)
        if request.method == 'POST':
            estimated_time = float(request.POST['estimated_time'])
            complexity = int(request.POST['complexity'])

            # Make a prediction
            predicted_time = reg.predict([[estimated_time, complexity]])

            # Render the result in the template
            return render(request, 'prediction/predict_completion.html', {'predicted_time': predicted_time[0]})

    return render(request, 'prediction/predict_completion.html')
