
# from src.agents.data_analyst_agent import create_data_analyst_agent
# from src.agents.segmentation_agent import create_segmentation_agent
# from src.agents.recommendation_agent import create_recommendation_agent
# from src.llm.gemini_integration import initialize_llm
# import pandas as pd

# def initialize_multi_agent_system(df):
#     try:
#         # Initialize LLM
#         llm = initialize_llm()
        
#         # Initialize segmentation agent
#         segmentation = create_segmentation_agent(df)
        
#         # Segment customers
#         segmented_df = segmentation['segment_customers']()
        
#         # Initialize data analyst and recommendation agents with segmented DataFrame
#         data_analyst = create_data_analyst_agent(llm, segmented_df)
#         recommender = create_recommendation_agent(llm, segmented_df)
        
#         # Define query mapping for segment_agent's functions
#         query_mapping = {
#             "characteristics of high-value customers": segmentation['analyze_high_value_characteristics'],
#             "mid-value customers differ from low-value customers in spending": segmentation['compare_mid_low_spending'],
#             "satisfaction levels of high-value customers": segmentation['analyze_high_value_satisfaction'],
#             "cities have the most low-value customers": segmentation['top_cities_low_value'],
#             "average rating for mid-value customers": segmentation['mid_value_avg_rating'],
#             "how many customers are in each segment": segmentation['segment_counts']
#         }
        
#         def process_query(query, customer_id=None):
#             try:
#                 # Normalize query for matching
#                 query_lower = query.lower().strip()
                
#                 # Route recommendation queries
#                 if "recommend" in query_lower and customer_id:
#                     return recommender(customer_id)
                
#                 # Route specific segment queries to segment_agent
#                 for key, func in query_mapping.items():
#                     if key in query_lower:
#                         return func()
                
#                 # Route other analytical queries to data_analyst
#                 if "analyze" in query_lower or "summary" in query_lower or "what" in query_lower or "how" in query_lower:
#                     return data_analyst(query)
                
#                 # Default response for unclear queries
#                 return "Please specify if you want recommendations (provide customer ID) or data analysis."
            
#             except Exception as e:
#                 return f"Error processing query: {str(e)}"
        
#         return process_query, segmented_df
    
#     except Exception as e:
#         return lambda query, customer_id=None: f"Error initializing system: {str(e)}", df




from src.agents.data_analyst_agent import create_data_analyst_agent
from src.agents.segmentation_agent import create_segmentation_agent
from src.agents.recommendation_agent import create_recommendation_agent
from src.llm.gemini_integration import initialize_llm
import pandas as pd
import re

def initialize_multi_agent_system(df):
    try:
        # Initialize LLM
        llm = initialize_llm()
        
        # Initialize segmentation agent
        segmentation = create_segmentation_agent(df)
        
        # Segment customers
        segmented_df = segmentation['segment_customers']()
        
        # Initialize data analyst and recommendation agents with segmented DataFrame
        data_analyst = create_data_analyst_agent(llm, segmented_df)
        recommender = create_recommendation_agent(llm, segmented_df)
        
        # Define query mapping for segment_agent's functions
        query_mapping = {
            r"characteristics.*high-value": segmentation['analyze_high_value_characteristics'],
            r"mid-value.*low-value.*spending": segmentation['compare_mid_low_spending'],
            r"satisfaction.*high-value": segmentation['analyze_high_value_satisfaction'],
            r"cities.*low-value": segmentation['top_cities_low_value'],
            r"average rating.*mid-value": segmentation['mid_value_avg_rating'],
            r"customers.*each segment": segmentation['segment_counts'],
        }
        
        def process_query(query, customer_id=None):
            try:
                # Normalize query for matching
                query_lower = query.lower().strip()
                
                # Route recommendation queries
                if "recommend" in query_lower and customer_id:
                    return recommender(customer_id)
                
                # Route specific segment queries to segment_agent using regex
                for pattern, func in query_mapping.items():
                    if re.search(pattern, query_lower):
                        return func()
                
                # Route all other queries to data_analyst (handles customer details, cities, segments, etc.)
                return data_analyst(query)
            
            except Exception as e:
                return f"Error processing query: {str(e)}"
        
        return process_query, segmented_df
    
    except Exception as e:
        return lambda query, customer_id=None: f"Error initializing system: {str(e)}", df






