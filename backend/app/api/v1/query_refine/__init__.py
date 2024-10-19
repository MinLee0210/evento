import json
import os

from components.llms import AgentFactory
from components.llms.prompts import HYPOTHETICAL_REWRITE, QUERY_REWRITE
from dotenv import load_dotenv
from schema.llm_response import RefineQuery

load_dotenv()


def refine_query(query):

    llm_config = {
        "api_key": os.getenv("GOOGLE_API_KEY"),
        "response_setting": {
            "response_mime_type": "application/json",
            "response_schema": RefineQuery,
        },
    }
    refine_agent = AgentFactory.produce(provider="gemini", **llm_config)
    result = refine_agent.run(HYPOTHETICAL_REWRITE.format(prompt=query))
    result = json.loads(result)
    return result
