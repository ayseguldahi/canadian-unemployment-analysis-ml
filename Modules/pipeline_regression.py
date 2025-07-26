import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score

def preprocess_data(df_cleaned, target_column):
    X = df_cleaned.drop(columns=[target_column])
    y = df_cleaned[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def create_pipeline(model):
   
    return Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', model)
    ])

def evaluate_models(X_train, X_test, y_train, y_test):

    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(),
        'Lasso Regression': Lasso(),
        'Random Forest': RandomForestRegressor(random_state=42),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'KNN': KNeighborsRegressor()
    }

    results = [] 
    for name, model in models.items():
        pipeline = create_pipeline(model)
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        # Append the result as a dictionary
        results.append({
            'Model': name,
            'MSE': mse,
            'R2': r2
        })
    
    return results

def hyperparameter_tuning(X_train, y_train):
    
    param_grid = {
        'Ridge Regression': {'regressor__alpha': [0.1, 1.0, 10.0]},
        'Lasso Regression': {'regressor__alpha': [0.01, 0.1, 1.0]},
        'Random Forest': {'regressor__n_estimators': [50, 100, 200]},
        'Decision Tree': {'regressor__max_depth': [3, 5, 10, None]},
        'KNN': {'regressor__n_neighbors': [3, 5, 10, 20]}
    }

    # Map model names to their actual classes
    model_mapping = {
        'Ridge Regression': Ridge(),
        'Lasso Regression': Lasso(),
        'Random Forest': RandomForestRegressor(random_state=42),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'KNN': KNeighborsRegressor()
    }

    best_params = {}
    for model_name, params in param_grid.items():
        # Create pipeline for the current model
        model = create_pipeline(model_mapping[model_name])
        grid_search = GridSearchCV(model, params, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        best_params[model_name] = grid_search.best_params_

    return best_params
