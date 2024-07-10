import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI, OpenAI

# Assuming these modules are imported and installed

df = pd.read_csv("products.csv")
df1 = pd.read_csv("revi.csv")

def search_result(text):
    # Initialize the LangChain agent for ChatOpenAI
    agent = create_pandas_dataframe_agent(OpenAI(temperature=0), [df, df1], verbose=True, allow_dangerous_code=True)
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True
    )
    
    # Assuming you want to append "output as list" to the input text
    text1 = text + " output as list"
    
    try:
        # Invoke the agent with the modified text
        result = agent.invoke(text1)
        return result
    except Exception as e:
        # Handle any exceptions that might occur during invocation
        print(f"Error processing search query: {str(e)}")
        return None

