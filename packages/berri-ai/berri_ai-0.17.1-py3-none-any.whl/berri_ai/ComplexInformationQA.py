from gpt_index import GPTSimpleVectorIndex 
from langchain import OpenAI, LLMChain
from langchain.schema import AgentAction, AgentFinish
import re
import os
from langchain.agents import initialize_agent, Tool, ZeroShotAgent, AgentExecutor
from typing import Any, List, Optional, Tuple, Union
from berri_ai.QAAgent import QAAgent

def querying_db(query: str):
  response = index2.query(query)
  response = (response.response, response.source_nodes[0].source_text)
  return response

tools = [
    Tool(
        name = "QueryingDB",
        func=querying_db,
        description="This function takes a query string as input and returns the most relevant answer from the documentation as output"
    )]

PREFIX = """Answer the following questions as best you can. You have access to the following tools:"""

SUFFIX = """Begin!

Question: {input}
Thought:{agent_scratchpad}"""

DEFAULT_PROMPT = ZeroShotAgent.create_prompt(
      tools, 
      prefix=PREFIX, 
      suffix=SUFFIX, 
      input_variables=["input", "agent_scratchpad"])

class ComplexInformationQA():
  """Base class for Complex Information QA Agent Class"""  
  def __init__(self, index, prompt=DEFAULT_PROMPT):
    self.index = index 
    self.tools = tools
    self.prompt = prompt
    self.llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=self.prompt)
  
  def querying_db(self, query: str):
    response = self.index.query(query)
    response = (response.response, response.source_nodes[0].source_text)
    return "hello"
  
  def run(self, query_string: str):
    tool_names = [tool.name for tool in self.tools]
    llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=self.prompt)
    # agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
    # agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=self.tools, verbose=True, )

    agent2 = QAAgent(llm_chain=self.llm_chain, tools=self.tools)
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent2, tools=self.tools, verbose=True, return_intermediate_steps=True)
    answer = agent_executor({"input":query_string})
    return answer