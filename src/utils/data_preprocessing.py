
import pandas as pd

def load_and_preprocess_data(file_path):
    try:
        # Load CSV
        df = pd.read_csv(file_path)
        
        # Handle missing values
        df['Satisfaction Level'] = df['Satisfaction Level'].fillna('Neutral')
        
        # Ensure numerical columns are correct type
        numerical_columns = ['Age', 'Total Spend', 'Items Purchased', 'Average Rating', 'Days Since Last Purchase']
        for col in numerical_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Ensure boolean column
        df['Discount Applied'] = df['Discount Applied'].astype(bool)
        
        return df
    
    except Exception as e:
        raise ValueError(f"Error loading and preprocessing data: {str(e)}")