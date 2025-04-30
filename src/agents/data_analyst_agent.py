
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import pandas as pd

def create_data_analyst_agent(llm, df):
    # Generate a comprehensive data summary
    def generate_data_summary():
        summary = []
        
        # Overall dataset summary
        summary.append("Dataset Overview:")
        summary.append(df.describe(include='all').to_string())
        
        # Segment-specific summary (if Segment column exists)
        if 'Segment' in df.columns:
            summary.append("\nSegment-Specific Summary:")
            for segment in df['Segment'].unique():
                segment_data = df[df['Segment'] == segment]
                summary.append(f"\nSegment: {segment}")
                summary.append(segment_data[['Age', 'Total Spend', 'Items Purchased', 'Average Rating', 'Days Since Last Purchase']].describe().to_string())
                summary.append(f"Satisfaction Level Distribution:\n{segment_data['Satisfaction Level'].value_counts().to_string()}")
                if 'City' in df.columns:
                    summary.append(f"Top Cities:\n{segment_data['City'].value_counts().head(5).to_string()}")
        
        return "\n".join(summary)
    
    data_summary = generate_data_summary()
    
    # Define prompt template
    prompt = PromptTemplate(
        input_variables=["query", "data_summary"],
        template="""
        You are a data analyst for an e-commerce platform. Using the following dataset summary:
        {data_summary}
        
        Answer the query in a concise, accurate, and insightful manner. 
        Provide numerical results where applicable, rounded to 2 decimal places. 
        If the query involves segments (High-Value, Mid-Value, Low-Value), use segment-specific data. If the query cannot be answered due to missing data, explain why.
        
        Query: {query}
        """
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    def run(query):
        try:
            return chain.run(query=query, data_summary=data_summary)
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    return run





