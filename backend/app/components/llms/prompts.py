# ===== QUERY REFINEMENT =====
QUERY_REWRITE = """Provide a concise and specific search query for an event retrieval engine to find relevant events based on the following prompt. Remember to keep the language and intention of the original prompt.

Prompt: {prompt}

Refine Query: 

"""

HYPOTHETICAL_REWRITE = """Act as a prompt engineer skilled at refining prompts for an event retrieval engine. Your task is to refine the following prompt to optimize results.  Follow these steps:

1. **Keyword Extraction:** Identify the semantically relevant keywords within the input prompt.  Prioritize keywords that directly relate to events, locations, dates, or key figures.

2. **Contextual Analysis:** Analyze the keywords in relation to the overall topic of the prompt.  Infer the implicit meanings and potential relationships between the keywords.  Consider what specific information the retrieval engine might need to find relevant events.

3. **Refined Prompt Generation:**  Rewrite the input prompt based on your keyword analysis and contextual understanding.  The refined prompt should be a concise and accurate query that explicitly targets the desired information.

Remember to keep the language and intention of the original prompt.

Prompt: {prompt}

Refined Query:
"""

# ===== EXTRACTING KEYWORDS =====
EXTRACT_KEYWORDS = """You are a prompt engineer tasked with creating a list of keywords for news search optimization. Your goal is to identify semantically relevant keywords for a news article that will improve search engine rankings and user satisfaction.

You can use the provided examples as reference, where each query and result represent a news article with extracted keywords:

Query: 'The government announces a new policy to tackle climate change. The policy includes a carbon tax and incentives for Prenewable energy.'
Result: ['government', 'policy', 'climate change', 'carbon tax', 'renewable energy']"

Query: 'Apple Inc. announces a breakthrough in battery technology, promising longer-lasting charges for its devices.'
Result: ['Apple', 'battery technology', 'longer-lasting charges']"

Query: 'NASA reveals stunning new images of Jupiter's moon, Europa, suggesting the presence of water and potential life.'
Result: ['NASA', 'Jupiter', 'Europa', 'water', 'potential life']"

Query: 'The World Health Organization declares a global health emergency due to the rapid spread of a new virus.'
Result: ['World Health Organization', 'global health emergency', 'new virus']"

If there is any question in the provided Query, do not try to answer it. Just focus on extracing keywords
"""
