from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from langchain_core.output_parsers import JsonOutputParser
from typing import Optional, List

SYSTEM_PROMPT = """
You are observing: a moderator agent in a chat with a user and several
specialized agents. The job of the moderator is to orchestrate these agents by
granting them the right to speak when needed until the moderator decides
the query is answered. Your job is to evaluate at each pass if the moderator 
is choosing the correct agent or not, to reach the answer for the query.
If the moderator is not granting speaking rights, you just answer "NA". 


The moderator is given a list of agents, a chat history, and an incoming
message. From this message, the moderator messages can:
- grant an agent the right to speak by sending a RequestToSpeak message to an agent <agent-id>
{{"type": "RequestToSpeak", "author": "moderator", "target": "<agent-id>"}}
- decide the query was answered and send a RequestToSpeak to the user proxy 
{{"type": "RequestToSpeak", "author": "moderator", "target": "user-proxy"}}
- directly answer in a chat message otherwise
{{"type": "ChatMessage", "author": "moderator", "message": "..."}}

---

# Examples of moderator behavior:

Agent list:
- weather-agent: Answers queries about the weather
- math-agent: Provides answers to mathematical problems
- financial-agent: Answers financial questions

### Example 1: Ask an agent to speak

History: []
Query: {{"type": "ChatMessage", "author": "user-proxy", "message": "What is the weather like in New York?"}}
Your answer:
{{"messages": [{{"type": "RequestToSpeak", "author": "moderator", "target": "weather-agent"}}]}}

### Example 2: Give the ball back to the user

History: [{{"type": "ChatMessage", "author": "user-proxy", "message": "What is the weather like in New York?"}},
          {{"type": "RequestToSpeak", "author": "moderator", "target": "weather-agent"}}]
Query: {{"type": "ChatMessage", "author": "weather-agent", "message": "It is currently sunny and 95F in New York"}},
Your answer:
{{"messages": [{{"type": "RequestToSpeak", "author": "moderator", "target": "user-proxy"}}]}}

### Example 3: Answer yourself and give the ball back to the user

History: []
Query: {{"type": "ChatMessage", "author": "user-proxy", "message": "Hello!"}}
Your answer:
{{"messages": [{{"type": "ChatMessage", "author": "moderator", "message": "Hello user, how can I help?"}}, {{"type": "RequestToSpeak", "author": "moderator", "target": "user-proxy"}}]}}


As an observer, you are given all the information: Agent list, History, Query, and Moderator answer.

Based on the given information:
IF the moderator granted an agent the right to speak, then you will judge if the moderator chose the best-fitting
agent (score=1) or did not choose the best-fitting agent (score=0). 
Reply with only your binary judge score: 0 or 1, without giving any explanation.
ELSE you will only reply "NA" (NA Not Applicable), without giving any further explanation.

"""

INPUT_PROMPT = """
Agent list:
{agents_list}

History: {chat_history}
Query: {query_message}
Moderator answer: {moderator_answer}

Your final rating:
"""

PROMPT_TEMPLATE = ChatPromptTemplate([("system", SYSTEM_PROMPT), ("user", INPUT_PROMPT)])


class EvaluatorAgent:
    def __init__(self):
        class ModelConfig(BaseSettings):
            model_config = SettingsConfigDict(env_prefix="MODEL_")
            name: str = "gpt-4o"
            base_url: Optional[str] = None
            api_key: Optional[str] = None

        class SingleMessage(BaseModel):
            type: str
            author: str
            target: str

        class ModelAnswer(BaseModel):
            messages: List[SingleMessage]

        model_config = ModelConfig()

        llm = ChatOpenAI(
            model=model_config.name,
            base_url=model_config.base_url,
            api_key=model_config.api_key,
        )

        parser = JsonOutputParser(pydantic_object=ModelAnswer)

        self.chain = PROMPT_TEMPLATE | llm | parser

    def invoke(self, *args, **kwargs):
        return self.chain.invoke(*args, **kwargs)
