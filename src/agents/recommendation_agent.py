
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# import pandas as pd

# def create_recommendation_agent(llm, df):
#     # Define prompt template
#     prompt = PromptTemplate(
#         input_variables=["customer_data", "segment"],
#         template="""
#         You are a recommendation system for an e-commerce platform. Based on the customer data:
#         {customer_data}
#         Segment: {segment}
        
#         Provide 2-3 personalized recommendations to improve customer satisfaction and engagement.
#           Tailor recommendations based on the customer's segment (High-Value, Mid-Value, Low-Value), s
#           pending behavior, satisfaction level, and recent activity. Examples include targeted promotions, loyalty rewards, or re-engagement campaigns. 
#           Be concise and actionable.
#         """
#     )
    
#     chain = LLMChain(llm=llm, prompt=prompt)
    
#     def run(customer_id):
#         try:
#             # Check if customer ID exists
#             customer_data = df[df['Customer ID'] == customer_id].to_dict('records')
#             if not customer_data:
#                 return "Customer ID not found."
            
#             # Check if Segment column exists
#             if 'Segment' not in df.columns:
#                 return "Error: Segment column not found. Please run segmentation first."
            
#             # Get segment
#             segment = df[df['Customer ID'] == customer_id]['Segment'].iloc[0]
            
#             # Run recommendation
#             return chain.run(customer_data=str(customer_data), segment=segment)
#         except Exception as e:
#             return f"Error generating recommendation: {str(e)}"
    
#     return run





from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import pandas as pd

def create_recommendation_agent(llm, df):
    # Define the prompt template
    prompt = PromptTemplate(
        input_variables=["customer_id", "segment", "total_spend"],
        template="""
        You are a smart assistant for an e-commerce business. 
        Generate 2–3 concise and actionable personalized recommendations to improve customer satisfaction and engagement.

        Customer ID: {customer_id}  
        Segment: {segment}  
        Total Spend: ${total_spend}

        Tailor suggestions based on the customer's value segment (High-Value, Mid-Value, Low-Value) and their spending behavior. 
        Examples include loyalty rewards, targeted promotions, or re-engagement campaigns.
        """
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    def run(customer_id):
        try:
            # Check if customer ID exists
            customer_row = df[df['Customer ID'] == customer_id]
            if customer_row.empty:
                return "Customer ID not found."

            # Check for required columns
            required_cols = {'Segment', 'Total Spend'}
            if not required_cols.issubset(df.columns):
                return f"Error: Missing required columns {required_cols - set(df.columns)}"

            # Extract values
            segment = customer_row['Segment'].iloc[0]
            total_spend = customer_row['Total Spend'].iloc[0]

            # Run LLM chain
            return chain.run(customer_id=str(customer_id), segment=segment, total_spend=total_spend)
        except Exception as e:
            return f"Error generating recommendation: {str(e)}"
    
    return run
