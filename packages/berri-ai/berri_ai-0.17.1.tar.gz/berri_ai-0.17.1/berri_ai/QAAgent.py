from langchain import OpenAI, LLMChain
from langchain.schema import AgentAction, AgentFinish
import re
import os
from langchain.agents import initialize_agent, Tool, ZeroShotAgent, AgentExecutor
from typing import Any, List, Optional, Tuple, Union
os.environ["OPENAI_API_KEY"] = "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"

class QAAgent(ZeroShotAgent):
  """Agent for the MRKL chain."""
  lastDocsViewed: List = None
  FINAL_ANSWER_ACTION = "Final Answer: "
  def _extract_tool_and_input(self, llm_output: str) -> Optional[Tuple[str, str]]:
      if self.FINAL_ANSWER_ACTION in llm_output:
          return "Final Answer", llm_output.split(self.FINAL_ANSWER_ACTION)[-1]
      regex = r"Action: (.*?)\nAction Input: (.*)"
      match = re.search(regex, llm_output)
      if not match:
          raise ValueError(f"Could not parse LLM output: `{llm_output}`")
      action = match.group(1)
      action_input = match.group(2)
      return action, action_input.strip(" ").strip('"')

  def doc_extractor(self, observation):
    # assume it's a tuple that can take in 2 inputs -> (the doc results,the doc links)
    print("observation doc extractor: ", observation)
    self.lastDocsViewed = observation[1]
    return observation[0]
    

  def plan(self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any) -> Union[AgentAction, AgentFinish]:
      """Given input, decided what to do.

      Args:
          intermediate_steps: Steps the LLM has taken to date,
              along with observations
          **kwargs: User inputs.

      Returns:
          Action specifying what tool to use.
      """
      thoughts = ""
      for action, observation in intermediate_steps:
          if type(observation) == tuple:
            observation = self.doc_extractor(observation)
          thoughts += action.log
          thoughts += f"\n{self.observation_prefix}{observation}\n{self.llm_prefix}"
      new_inputs = {"agent_scratchpad": thoughts, "stop": self._stop}
      full_inputs = {**kwargs, **new_inputs}
      full_output = self.llm_chain.predict(**full_inputs)
      parsed_output = self._extract_tool_and_input(full_output)
      predict_output = None
      while parsed_output is None:
          full_output = self._fix_text(full_output)
          full_inputs["agent_scratchpad"] += full_output
          output = self.llm_chain.predict(**full_inputs)
          predict_output = output
          full_output += output
          parsed_output = self._extract_tool_and_input(full_output)
      tool, tool_input = parsed_output
      if tool == self.finish_tool_name:
          print("last docs viewed: ", self.lastDocsViewed)
          tool_input = {"response": tool_input, "references": "\n Here is a list of documents that I viewed: " + str(self.lastDocsViewed)}
          return AgentFinish({"output": tool_input}, full_output)
      output = AgentAction(tool, tool_input, full_output)
      return output