import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import joblib

def get_preprocessor():
    """Create and return the preprocessing pipeline"""
    
    # Define which columns are categorical and which are numeric
    categorical_cols = ['school', 'famsize', 'Pstatus', 'Mjob', 'Fjob', 'reason', 
                       'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 
                       'higher', 'internet', 'romantic']
    
    numeric_cols = ['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures',
                   'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2']
    
    # Also encode simple categorical ones using OneHotEncoder
    simple_categorical_cols = ['sex', 'address', 'guardian']
    
    # Create the column transformer with handle_unknown='ignore'
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False, drop='first'), 
             categorical_cols + simple_categorical_cols),
            ('num', SimpleImputer(strategy='mean'), numeric_cols)
        ],
        remainder='drop'  # Drop any remaining columns
    )
    
    return preprocessor, categorical_cols + simple_categorical_cols, numeric_cols

def preprocess_data(df, is_training=True):
    """
    Preprocess student data. 
    If is_training=True, fit the preprocessing pipeline.
    If is_training=False, use the saved pipeline from training.
    """
    # Make a copy to avoid modifying the original
    df = df.copy()
    
    preprocessor, all_categorical_cols, numeric_cols = get_preprocessor()
    
    # Separate features and target (only if G3 exists)
    if 'G3' in df.columns:
        X = df.drop('G3', axis=1)
        y = df['G3']
    else:
        X = df
        y = None
    
    # Define all required columns in the exact order
    all_required_cols = all_categorical_cols + numeric_cols
    
    # For prediction mode: fill missing columns with defaults
    if not is_training:
        # Load sample data to get default values
        df_sample = pd.read_csv('data/student_data.csv')
        
        # Fill missing categorical columns with most common value from training data
        for col in all_categorical_cols:
            if col not in X.columns:
                X[col] = df_sample[col].mode()[0]
        
        # Fill missing numeric columns with mean from training data
        for col in numeric_cols:
            if col not in X.columns:
                X[col] = df_sample[col].mean()
    
    # Convert all categorical columns to string type
    for col in all_categorical_cols:
        if col in X.columns:
            X[col] = X[col].astype(str)
    
    # Ensure columns are in the correct order for the preprocessor
    X = X[all_required_cols]
    
    if is_training:
        # Fit the preprocessor during training
        X_transformed = preprocessor.fit_transform(X)
        # Get feature names after transformation
        cat_features = list(preprocessor.named_transformers_['cat'].get_feature_names_out(all_categorical_cols))
        feature_names = cat_features + numeric_cols
        
        # Save the preprocessor
        joblib.dump(preprocessor, 'models/preprocessor.pkl')
        joblib.dump(feature_names, 'models/feature_names.pkl')
        
        X = pd.DataFrame(X_transformed, columns=feature_names)
    else:
        # Load and use the saved preprocessor
        preprocessor = joblib.load('models/preprocessor.pkl')
        feature_names = joblib.load('models/feature_names.pkl')
        
        X_transformed = preprocessor.transform(X)
        X = pd.DataFrame(X_transformed, columns=feature_names)

    return X, y
