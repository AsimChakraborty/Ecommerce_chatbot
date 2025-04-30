
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def create_segmentation_agent(df):
    # Validate required columns
    required_columns = ['Age', 'Total Spend', 'Items Purchased', 'Average Rating', 'Days Since Last Purchase']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    def segment_customers():
        # Preparing features for clustering
        features = ['Age', 'Total Spend', 'Items Purchased', 'Average Rating', 'Days Since Last Purchase']
        X = df[features].copy()
        
        # Handle missing or invalid values
        X = X.fillna(X.mean())
        
        # Standardizing features
        X = (X - X.mean()) / X.std()
        
        # Applying KMeans clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        df['Segment'] = kmeans.fit_predict(X)
        
        # Determine which cluster is High-Value, Mid-Value, Low-Value based on Total Spend
        cluster_means = df.groupby('Segment')['Total Spend'].mean().sort_values(ascending=False)
        segment_labels = {
            cluster_means.index[0]: 'High-Value',
            cluster_means.index[1]: 'Mid-Value',
            cluster_means.index[2]: 'Low-Value'
        }
        df['Segment'] = df['Segment'].map(segment_labels)
        
        return df
    
    # Query 1: Characteristics of High-Value customers
    def analyze_high_value_characteristics():
        high_value = df[df['Segment'] == 'High-Value']
        characteristics = high_value[['Age', 'Total Spend', 'Items Purchased', 'Average Rating', 'Days Since Last Purchase']].mean().to_dict()
        return {
            'Average Age': round(characteristics['Age'], 2),
            'Average Total Spend': round(characteristics['Total Spend'], 2),
            'Average Items Purchased': round(characteristics['Items Purchased'], 2),
            'Average Rating': round(characteristics['Average Rating'], 2),
            'Average Days Since Last Purchase': round(characteristics['Days Since Last Purchase'], 2)
        }

    # Query 2: Compare Mid-Value and Low-Value customers in spending
    def compare_mid_low_spending():
        mid_value_spend = df[df['Segment'] == 'Mid-Value']['Total Spend'].mean()
        low_value_spend = df[df['Segment'] == 'Low-Value']['Total Spend'].mean()
        return {
            'Mid-Value Average Spend': round(mid_value_spend, 2),
            'Low-Value Average Spend': round(low_value_spend, 2),
            'Difference': round(mid_value_spend - low_value_spend, 2)
        }

    # Query 3: Analyze satisfaction levels of High-Value customers
    def analyze_high_value_satisfaction():
        high_value = df[df['Segment'] == 'High-Value']
        satisfaction_stats = {
            'Mean Rating': round(high_value['Average Rating'].mean(), 2),
            'Median Rating': round(high_value['Average Rating'].median(), 2),
            'Std Dev Rating': round(high_value['Average Rating'].std(), 2),
            'Satisfaction Level Distribution': high_value['Satisfaction Level'].value_counts().to_dict()
        }
        return satisfaction_stats

    # Query 4: Cities with the most Low-Value customers
    def top_cities_low_value():
        if 'City' not in df.columns:
            return "Error: 'City' column not found in DataFrame."
        low_value = df[df['Segment'] == 'Low-Value']
        city_counts = low_value['City'].value_counts().head(5).to_dict()
        return city_counts

    # Query 5: Average rating for Mid-Value customers
    def mid_value_avg_rating():
        mid_value = df[df['Segment'] == 'Mid-Value']
        return round(mid_value['Average Rating'].mean(), 2)
    

    # Query 6: Number of customers in each segment
    def segment_counts():
        return df['Segment'].value_counts().to_dict()
    
    # Query 7: Membership analysis
    def membership_analysis():
        # Check if the customer is a member or not
        if 'Membership' in df.columns:
            membership_counts = df['Membership'].value_counts().to_dict()
            return membership_counts
        else:
            return "Error: 'Membership' column not found in DataFrame."
    #query 8: Unique values for categorical columns    
    def unique_values():
        # Get unique values for categorical columns
        categorical_columns = ['Satisfaction Level', 'Membership']
        unique_values = {col: df[col].unique().tolist() for col in categorical_columns if col in df.columns}
        return unique_values    
    # Query 9: Discount analysis
    def discount_analysis():
        # Check if the discount column exists
        if 'Discount Applied' in df.columns:
            discount_counts = df['Discount Applied'].value_counts().to_dict()
            return discount_counts
        else:
            return "Error: 'Discount Applied' column not found in DataFrame."
    #qery 10: Summary of customer activity based on membership
    def summary_of_customer_activity_base_on_membership():
        # Check if the customer is a member or not
        if 'Membership' in df.columns:
            membership_counts = df['Membership'].value_counts().to_dict()
            return membership_counts
        else:
            return "Error: 'Membership' column not found in DataFrame."     

    return {
        'segment_customers': segment_customers,
        'analyze_high_value_characteristics': analyze_high_value_characteristics,
        'compare_mid_low_spending': compare_mid_low_spending,
        'analyze_high_value_satisfaction': analyze_high_value_satisfaction,
        'top_cities_low_value': top_cities_low_value,
        'mid_value_avg_rating': mid_value_avg_rating,
        'segment_counts': segment_counts,
        'membership_analysis': membership_analysis,
        'unique_values': unique_values,
        'discount_analysis': discount_analysis,
        'summary_of_customer_activity_base_on_membership': summary_of_customer_activity_base_on_membership
    
    }