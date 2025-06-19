import json
import os
from app.agents.agent_factory import (
    search_agent,
    source_profiler_agent,
    diversity_selector_agent,
    debate_synthesizer_agent
)
from swarm import Swarm

client = Swarm()

def process_news(topic, status_callback=None):
    """Run the news processing workflow"""

    def notify(msg):
        if status_callback:
            status_callback(msg)

    # 🔍 Search
    notify("🔍 Searching for news...")
    search_response = client.run(
        agent=search_agent,
        messages=[{"role": "user", "content": f"Find recent news about {topic}"}]
    )

    try:
        raw_news_list = json.loads(search_response.messages[-1]["content"])
    except json.JSONDecodeError as e:
        return None, None, None, f"Search JSON decode error: {e}"

    # 💾 Save raw articles
    os.makedirs("news_output", exist_ok=True)
    raw_file = f"news_output/{topic.replace(' ', '_')}_articles.json"
    with open(raw_file, "w", encoding="utf-8") as f:
        json.dump(raw_news_list, f, indent=2)

    # 🧠 Profile Sources
    notify("🧠 Profiling sources...")
    profile_response = client.run(
        agent=source_profiler_agent,
        messages=[{"role": "user", "content": f"Profile these articles:\n{json.dumps(raw_news_list, indent=2)}"}]
    )

    try:
        profiling_output = json.loads(profile_response.messages[-1]["content"])
    except json.JSONDecodeError as e:
        return None, None, None, f"Profiler JSON decode error: {e}"

    profiling_file = f"news_output/{topic.replace(' ', '_')}_profiling.json"
    with open(profiling_file, "w", encoding="utf-8") as f:
        json.dump(profiling_output, f, indent=2)

    # 🎯 Select Diverse Subset
    notify("🧮 Selecting diverse subset...")
    diversity_response = client.run(
        agent=diversity_selector_agent,
        messages=[{"role": "user", "content": f"Select a diverse subset:\n{json.dumps(profiling_output, indent=2)}"}]
    )

    try:
        selected_ids = json.loads(diversity_response.messages[-1]["content"])
    except json.JSONDecodeError as e:
        return None, None, None, f"Diversity selector JSON decode error: {e}"

    selected_articles = [a for a in raw_news_list if a["id"] in selected_ids]

    selected_file = f"news_output/{topic.replace(' ', '_')}_selected.json"
    with open(selected_file, "w", encoding="utf-8") as f:
        json.dump(selected_articles, f, indent=2)

    # 🗣️ Synthesize Debate
    notify("🗣️ Synthesizing report...")
    debate_response = client.run(
        agent=debate_synthesizer_agent,
        messages=[{"role": "user", "content": f"Create a debate report:\n{json.dumps(selected_articles, indent=2)}"}]
    )
    final_report = debate_response.messages[-1]["content"]

    report_file = f"news_output/{topic.replace(' ', '_')}_debate_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(final_report)

    return selected_articles, profiling_output, final_report, None
