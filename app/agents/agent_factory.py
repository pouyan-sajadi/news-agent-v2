from swarm import Agent
from .prompts import search_prompt, profiler_prompt, diversity_prompt, synthesizer_prompt
from app.core.utils import search_news  
from app.config import MODEL

search_agent = Agent(
    name="News Searcher",
    instructions=search_prompt,
    functions=[search_news],
    model=MODEL
)

source_profiler_agent = Agent(
    name="Source Profiler",
    instructions=profiler_prompt,
    model=MODEL
)

diversity_selector_agent = Agent(
    name="Diversity Selector",
    instructions=diversity_prompt,
    model=MODEL
)

debate_synthesizer_agent = Agent(
    name="Debate Synthesizer",
    instructions=synthesizer_prompt,
    model=MODEL
)
