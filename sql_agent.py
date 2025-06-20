from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st


class SQLHandler(BaseCallbackHandler):
    '''Class to save the sql query through a callback handler'''
    def __init__(self):
        self.sql_result = []

    def on_agent_action(self, action, **kwargs):
        """Run on agent action. if the tool being used is sql_db_query,
         it means we're submitting the sql and we can 
         record it as the final sql query"""

        if action.tool in ["sql_db_query_checker","sql_db_query"]:
            self.sql_result.append(action.tool_input)

class SQLAgent:
    def __init__(self, db):
        self.db = db

        # Create the LLM model
        self.llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=st.secrets["OPENAI_API_KEY"])

        # Create the SQL handler
        self.handler = SQLHandler()

    def invoke(self, input):
        '''Create invoke function for the class to run the agent and return the result'''
        agent_executor = create_sql_agent(self.llm, db=self.db, agent_type="openai-tools", verbose=False)
        result = agent_executor.invoke({'input':input}, {'callbacks':[self.handler]})
        return result
    
    def get_sql(self):
        return self.handler.sql_result
    
    def get_output(self):
        return self.handler.output

if __name__ == '__main__':
    pass
