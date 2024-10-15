from components.llms import AgentFactory
from components.llms.prompts import QUERY_REWRITE, HYPOTHETICAL_REWRITE
from schema.llm_response import RefineQuery

import os 
import json

from dotenv import load_dotenv

load_dotenv()


def refine_query(query): 

    llm_config = {'api_key': os.getenv("GOOGLE_API_KEY"), 
              'response_setting': {
                  "response_mime_type":'application/json', 
                  "response_schema": RefineQuery
              }}
    refine_agent = AgentFactory.produce(provider='gemini', 
                                    **llm_config)
    result = refine_agent.run(HYPOTHETICAL_REWRITE.format(prompt=query))
    result = json.loads(result)
    return result