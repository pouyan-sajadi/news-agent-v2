## 🧠 News Debate Synthesizer · v2

This is version 2 of my AI-powered news app — a smarter, more structured take on news summarization.

Instead of just summarizing headlines, this app **collects diverse news articles**, **analyzes their tone and perspective**, and **builds a structured report** that highlights how different sources frame the same story. Think of it as a multi-viewpoint synthesis tool — part summarizer, part analyst.

### What’s New in v2:
- Switched to **OpenAI's Swarm framework** to orchestrate multiple LLM agents
- Uses **real-time search with SerpAPI** to fetch the latest articles
- Reads the **full text** of articles, not just previews or headlines
- Runs **source profiling**, **diversity filtering**, and **debate-style synthesis**
- **New Creative Agent** for more engaging and readable output.
- **Customizable Output** to tailor the analysis to your needs.
- Fully modularized and production-ready structure

---

## 🚀 What It Does

Give it a topic (like *artificial intelligence*, *climate policy*, or *NVIDIA earnings*), and this app will:

1.  **Search** the web for recent and reputable news using SerpAPI.
2.  **Extract & Clean** full article content via `newspaper3k`.
3.  **Profile Sources** for tone, region, viewpoint, and type using a custom OpenAI-powered agent.
4.  **Select a Diverse Subset** using a diversity-aware filtering agent.
5.  **Synthesize** a report that highlights key themes and presents contrasting viewpoints with precise citations.
6.  **Edit and Refine** the report with a creative agent for a more engaging and readable format.
7.  **Deliver** a markdown-based, source-rich debate report — like a smart summary written by your well-informed friend.

---

## 🛠️ Tech Stack

- **🧠 LLM Agents**: Built with [OpenAI Swarm](https://github.com/openai/swarm)
- **🌐 Search**: [SerpAPI](https://serpapi.com/) for Google News results
- **📰 Scraping**: `newspaper3k` for full article content
- **🧩 Multi-Agent Workflow**:
  - `search_agent`: finds and cleans relevant news
  - `source_profiler_agent`: tags each article by tone, region, perspective
  - `diversity_selector_agent`: selects a well-rounded subset
  - `debate_synthesizer_agent`: crafts the final structured report
  - `creative_editor_agent`: refines the report for readability and engagement
- **💬 Frontend**: [Streamlit](https://streamlit.io/) for interactive UI
- **📁 Modular Design**: Clean structure with `core`, `agents`, `utils`, `config`, and `tests`

---

## 🎨 Customizable Output

You can tailor the output of the analysis to your specific needs with the following options:

### Focus

-   **Just the Facts**: A neutral, data-driven summary.
-   **Human Impact**: Focus on the personal stories and societal effects.
-   **The Clash**: Highlight the conflict and disagreement between sources.
-   **Hidden Angles**: Uncover the surprising or underreported details.
-   **The Money Trail**: Follow the financial implications of the story.

### Depth

-   **Quick Scan**: A brief, high-level overview.
-   **Balanced View**: A more detailed and nuanced analysis.
-   **Deep Dive**: A comprehensive and in-depth exploration of the topic.

---

## 📦 Installation

```bash
git clone https://github.com/pouyan-sajadi/news-agent-v2.git
cd news_debate_app
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

Create a .env file in the root directory with the following content:
```env
OPENAI_API_KEY=your-openai-key
SERPAPI_KEY=your-serpapi-key
```
Running Locally:
```bash
streamlit run main.py
```