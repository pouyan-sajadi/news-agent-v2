import json
import os
import time
from app.agents.agent_factory import (
    create_search_agent,
    create_source_profiler_agent,
    create_diversity_selector_agent,
    create_debate_synthesizer_agent,
    create_creative_editor_agent
)
from swarm import Swarm
from app.core.logger import logger

client = Swarm()

def process_news(topic, user_preferences, status_callback=None):
    """Run the news processing workflow"""

    def notify(msg):
        if status_callback:
            status_callback(msg)

    focus = user_preferences.get("focus", "Just the Facts")
    depth = user_preferences.get("depth", 2)
    tone = user_preferences.get("tone", "News with attitude")

    # Search
    logger.info("🔍 Running Search Agent...")
    notify("🔍 Searching for news:")
    notify("🔍 Scouting the web for the latest headlines...")
    start_time = time.time()
    search_agent_instance = create_search_agent()
    search_response = client.run(
        agent=search_agent_instance,
        messages=[{"role": "user", "content": f"Find recent news about {topic}"}]
    )
    end_time = time.time()
    logger.info(f"Search Agent finished in {end_time - start_time:.2f} seconds.")

    try:
        raw_news_list = json.loads(search_response.messages[-1]["content"])
        logger.info(f"Successfully decoded JSON from Search Agent. Found {len(raw_news_list)} articles.")
    except json.JSONDecodeError as e:
        logger.exception("Failed to decode JSON from Search Agent")
        return None, None, None, None, f"Search JSON decode error: {e}"

    # Save raw articles
    os.makedirs("news_output", exist_ok=True)
    raw_file = f"news_output/{topic.replace(' ', '_')}_articles.json"
    with open(raw_file, "w", encoding="utf-8") as f:
        json.dump(raw_news_list, f, indent=2)

    # Profile Sources
    logger.info("Running Source Profiler Agent...")
    notify("🧠 Profiling sources:")
    notify("🧠 Analyzing sources and their perspectives...")
    source_profiler_agent_instance = create_source_profiler_agent(focus)
    profiler_message = f"Profile these articles:\n{json.dumps(raw_news_list, indent=2)}"
    profile_response = client.run(
        agent=source_profiler_agent_instance,
        messages=[{"role": "user", "content": profiler_message}]
    )

    try:
        profiling_output = json.loads(profile_response.messages[-1]["content"])
        logger.info("Successfully decoded JSON from Profiler Agent.")
    except json.JSONDecodeError as e:
        logger.exception("Failed to decode JSON from Profiler Agent")
        return None, None, None, None, f"Profiler JSON decode error: {e}"

    profiling_file = f"news_output/{topic.replace(' ', '_')}_profiling.json"
    with open(profiling_file, "w", encoding="utf-8") as f:
        json.dump(profiling_output, f, indent=2)

    # Select Diverse Subset
    logger.info("Running Diversity Selector Agent...")
    logger.debug("Passing this data to Diversity Selector: %s", json.dumps(profiling_output, indent=2))
    notify("🧮 Selecting diverse subset:")
    notify("🧮 Curating a well-rounded, diverse set of articles...")
    logger.debug("depth parameter: %s", depth)
    diversity_selector_agent_instance = create_diversity_selector_agent(focus, depth)
    diversity_message = f"Select a diverse subset from these profiles: {json.dumps(profiling_output, indent=2)}"
    try:
        diversity_response = client.run(
            agent=diversity_selector_agent_instance,
            messages=[{"role": "user", "content": diversity_message}]
        )
    except Exception as e:
        logger.error(f"❌ Unhandled error during processing: {e}")
        return None, None, None, None, f"Diversity selector failed: {e}"

    try:
        logger.debug("Raw response from Diversity Selector: %s", diversity_response.messages[-1]["content"])
        selected_ids = json.loads(diversity_response.messages[-1]["content"])
        logger.debug(f"Diversity Selector returned: {selected_ids}")
    except json.JSONDecodeError as e:
        logger.exception("Failed to decode JSON from Diversity Selector Agent")
        return None, None, None, None, f"Diversity selector JSON decode error: {e}"

    selected_articles = [a for a in raw_news_list if a["id"] in selected_ids]
    logger.info(f"Selected {len(selected_articles)} articles based on IDs.")

    selected_file = f"news_output/{topic.replace(' ', '_')}_selected.json"
    with open(selected_file, "w", encoding="utf-8") as f:
        json.dump(selected_articles, f, indent=2)

    # Synthesize Debate
    logger.info("Running Debate Synthesizer Agent...")
    notify("🗣️ Synthesizing report:")
    notify("🗣️ Weaving it all into a compelling debate-style report...")
    debate_synthesizer_agent_instance = create_debate_synthesizer_agent(focus, depth)
    debate_response = client.run(
        agent=debate_synthesizer_agent_instance,
        messages=[{"role": "user", "content": f"Create a debate report:\n{json.dumps(selected_articles, indent=2)}"}]
    )
    final_report = debate_response.messages[-1]["content"]

    report_file = f"news_output/{topic.replace(' ', '_')}_debate_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(final_report)

    # Creative Editor
    logger.info("Running Creative Editor Agent...")
    notify("🎨 Applying creative touch:")
    notify("🎨 Formatting the final report for maximum engagement...")
    creative_editor_agent_instance = create_creative_editor_agent(focus, depth, tone)
    creative_response = client.run(
        agent=creative_editor_agent_instance,
        messages=[{"role": "user", "content": f"Rewrite this report:\n{final_report}"}]
    )
    creative_report = creative_response.messages[-1]["content"]

    creative_report_file = f"news_output/{topic.replace(' ', '_')}_creative_report.md"
    with open(creative_report_file, "w", encoding="utf-8") as f:
        f.write(creative_report)

    return raw_news_list, selected_articles, profiling_output, creative_report, None