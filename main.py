import streamlit as st
from app.core.process import process_news
from app.core.logger import logger

st.set_page_config(
    page_title="Signal - Cut Through Noise", 
    page_icon="📡",
    layout="wide"
)

st.title("Pick your topic, pick your style – see every side of the story")

# Initialize session state variables if they don't exist
if 'current_report' not in st.session_state:
    st.session_state.current_report = None
if 'report_history' not in st.session_state:
    st.session_state.report_history = []

# --- MAIN APPLICATION UI ---

st.markdown("#### Turn any news topic into a multi-perspective analysis with your choice of focus, depth, and tone")

# Topic Input
topic_input = st.text_input(
    "*What's happening that you want the full story on?*",
    value="",
    placeholder="Try: tech layoffs, Middle East tensions, AI advancements, Meta's new AI team...",
    key="topic_input"
)

# Analysis Settings
st.markdown("#### Analysis Settings")

col_spacer1, col1, col_spacer2, col2, col_spacer3, col3, col_spacer4 = st.columns([0.1, 2, 0.5, 2, 0.5, 2, 0.5])

with col1:
    st.markdown("**🎯 What to Emphasize**")
    st.caption("Choose which aspects of the story matter most to you")
    
    focus = st.radio(
        "",
        options=[
            "Just the facts",
            "Human Impact", 
            "The Clash",
            "Hidden Angles",
            "The Money Trail"
        ],
        index=0,
        key="focus_setting",
        help="""
        **Just the facts**: Core information, data, and verified claims only
        
        **Human Impact**: Personal stories and how real people are affected
        
        **The Clash**: Conflicting viewpoints and who's arguing what
        
        **Hidden Angles**: Overlooked details and underreported perspectives
        
        **The Money Trail**: Financial implications and who profits/pays
        """
    )

with col2:
    st.markdown("**📏 How Much Detail**")
    st.caption("Control the length and depth of your report")
    
    depth = st.select_slider(
        "",
        options=[1, 2, 3],
        value=2,
        format_func=lambda x: {
            1: "Quick Scan",
            2: "Standard Read",
            3: "Deep Dive"
        }[x],
        key="depth_setting",
        help="""
        **Quick Scan (30 sec)**: Key points only, perfect for a quick update
        
        **Standard Read (2 min)**: Balanced coverage with context
        
        **Deep Dive (5+ min)**: Comprehensive analysis with full details
        """
    )

with col3:
    st.markdown("**✍️ Writing Style**")
    st.caption("How should we present the information?")
    
    tone_option = st.radio(
        "",
        options=[
            "Grandma Mode",
            "Gen Z Mode",
            "Express Mode", 
            "Commentary Mode"
        ],
        index=0,
        key="tone_setting",
        help="""
        **Grandma Mode**: Clear, patient explanations with context
        
        **Gen Z Mode**: Quick, energetic, with current references
        
        **Express Mode**: Crisp, efficient, straight to the point
        
        **Commentary Mode**: Includes analysis and connects the dots
        """
    )

# Map tone_option to the tone expected by the agent
tone_mapping = {
            "Express Mode": "Sharp & Snappy",
            "Grandma Mode": "Grandma Mode",
            "Gen Z Mode": "Gen Z Mode",
            "Commentary Mode": "News with attitude" 
        }
tone = tone_mapping.get(tone_option, "Quick Hit Mode") 

st.markdown("""
<style>
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) {
        padding-top: 0rem;
    }
</style>
""", unsafe_allow_html=True)

# Deploy Button
generate_btn = st.button("**Deploy Analysis Agents**", type="primary", use_container_width=True)

# --- PROCESSING LOGIC ---

# This block executes when the user clicks the button
if generate_btn:
    if topic_input.strip():
        logger.info(f"🧠 User requested topic: {topic_input}")

        # Archive the previous report if it exists
        if st.session_state.current_report:
            st.session_state.report_history.append(st.session_state.current_report)
        
        # Clear current report for new analysis
        st.session_state.current_report = {
            "topic": topic_input,
            "creative_report": None,
            "agent_details": {}
        }

        # --- UI Placeholders for Live Updates ---
        st.markdown("### Agent Processing Details")
        final_report_container = st.container()

        expanders = {
            "search": st.expander("**1. Search Agent** - Finding articles...", expanded=True),
            "profiling": st.expander("**2. Profiler Agent** - Analyzing sources...", expanded=False),
            "selection": st.expander("**3. Diversity Selector** - Choosing articles...", expanded=False),
            "synthesis": st.expander("**4. Debate Synthesizer** - Structuring report...", expanded=False),
            "editing": st.expander("**5. Creative Editor** - Polishing output...", expanded=False),
        }
        
        # Create placeholders inside each expander for dynamic content
        placeholders = {step: expander.empty() for step, expander in expanders.items()}

        # --- Callback Function to Update UI ---
        def update_ui_callback(output):
            step = output.get("step")
            status = output.get("status")
            data = output.get("data")
            message = output.get("message")

            placeholder = placeholders.get(step)
            if not placeholder:
                return

            if status == "running":
                placeholder.info(f"⏳ {message}")

            elif status == "completed":
                st.session_state.current_report["agent_details"][step] = data
                placeholder.empty()
                with placeholder.container():
                    if step == "search":
                        st.success(f"Found {len(data)} articles.")
                        for i, article in enumerate(data, 1):
                            st.markdown(f"{i}. [{article.get('title', 'Untitled')}]({article.get('url', '#')}) - *{article.get('source', 'Unknown')}* - `Published: {article.get('date', 'N/A')}`")
                        expanders["profiling"].expanded = True
                    
                    elif step == "profiling":
                        st.success("Profiling complete.")
                        profiling_lookup = {item["id"]: item for item in data}
                        raw_news_list = st.session_state.current_report["agent_details"].get('search', [])
                        for article in raw_news_list:
                            profile = profiling_lookup.get(article["id"], {})
                            tags = [f"**{k.title()}**: `{v}`" for k, v in profile.items() if k != 'id']
                            st.markdown(f"**📄 {article.get('title', 'Untitled')}**")
                            if tags:
                                st.markdown(" • ".join(tags))
                            else:
                                st.markdown("*Agent couldn't analyze this one* 🤷")
                            st.markdown("---")
                        expanders["selection"].expanded = True

                    elif step == "selection":
                        st.success(f"Selected {len(data)} articles for the final report.")
                        for i, article in enumerate(data, 1):
                            st.markdown(f"{i}. [{article.get('title', 'Untitled')}]({article.get('url', '#')}) - *{article.get('source', 'Unknown')}* - `Published: {article.get('date', 'N/A')}`")
                        expanders["synthesis"].expanded = True

                    elif step == "synthesis":
                        st.success("✅ Initial report structured and passed to the Creative Editor.")
                        expanders["editing"].expanded = True

                    elif step == "editing":
                        st.success("Report polished and ready!")
                        st.markdown(data)
                        st.session_state.current_report["creative_report"] = data

            elif step == "error":
                placeholder.error(f"💥 **Agent crashed:** {message}")

        # --- Agent Pipeline Execution ---
        user_preferences = {'focus': focus, 'depth': depth, 'tone': tone}
        process_news(topic_input, user_preferences, status_callback=update_ui_callback)

        # --- Final Output Display (Current Report) ---
        if st.session_state.current_report and st.session_state.current_report["creative_report"]:
            final_report_container.markdown("---")
            final_report_container.header("📰 The Debate Breakdown")
            final_report_container.markdown(st.session_state.current_report["creative_report"])
            st.toast("Your report is ready!", icon="🎉")
            st.balloons()
        else:
            final_report_container.error("The agent swarm failed to produce a final report.")

    else:
        st.warning("🎯 **Hey!** You forgot to enter a topic. The agents need something to work with!")

# --- Display Current Report (if not just generated) ---
# This block ensures the current report persists across reruns (e.g., sidebar changes)
if not generate_btn and st.session_state.current_report and st.session_state.current_report["creative_report"]:
    st.markdown("### Agent Processing Details")
    # Re-render expanders with content from session state
    expanders = {
        "search": st.expander("**1. Search Agent** - Finding articles...", expanded=True),
        "profiling": st.expander("**2. Profiler Agent** - Analyzing sources...", expanded=False),
        "selection": st.expander("**3. Diversity Selector** - Choosing articles...", expanded=False),
        "synthesis": st.expander("**4. Debate Synthesizer** - Structuring report...", expanded=False),
        "editing": st.expander("**5. Creative Editor** - Polishing output...", expanded=False),
    }
    
    # Populate expanders with archived data
    for step, data in st.session_state.current_report["agent_details"].items():
        with expanders[step]:
            if step == "search":
                st.success(f"Found {len(data)} articles.")
                for i, article in enumerate(data, 1):
                    st.markdown(f"{i}. [{article.get('title', 'Untitled')}]({article.get('url', '#')}) - *{article.get('source', 'Unknown')}* - `Published: {article.get('date', 'N/A')}`")
            elif step == "profiling":
                st.success("Profiling complete.")
                profiling_lookup = {item["id"]: item for item in data}
                raw_news_list = st.session_state.current_report["agent_details"].get('search', [])
                for article in raw_news_list:
                    profile = profiling_lookup.get(article["id"], {})
                    tags = [f"**{k.title()}**: `{v}`" for k, v in profile.items() if k != 'id']
                    st.markdown(f"**📄 {article.get('title', 'Untitled')}**")
                    if tags:
                        st.markdown(" • ".join(tags))
                    else:
                        st.markdown("*Agent couldn't analyze this one* 🤷")
                    st.markdown("---")
            elif step == "selection":
                st.success(f"Selected {len(data)} articles for the final report.")
                for i, article in enumerate(data, 1):
                    st.markdown(f"{i}. [{article.get('title', 'Untitled')}]({article.get('url', '#')}) - *{article.get('source', 'Unknown')}* - `Published: {article.get('date', 'N/A')}`")
            elif step == "synthesis":
                st.success("✅ Initial report structured and passed to the Creative Editor.")
            elif step == "editing":
                st.success("Report polished and ready!")
                st.markdown(data)

    st.markdown("---")
    st.header("📰 The Debate Breakdown")
    st.markdown(st.session_state.current_report["creative_report"])

# --- Display Archived Reports ---
if st.session_state.report_history:
    st.markdown("---")
    st.header("🗂️ Previous Analyses")
    for i, report_data in enumerate(st.session_state.report_history):
        with st.expander(f"Report for '{report_data.get('topic', 'N/A')}'", expanded=False):
            st.markdown(report_data.get('creative_report', 'No report available.'))

# --- ABOUT SECTION (COLLAPSED) ---
st.markdown("---")
with st.expander("About This Application"):
    st.markdown("""
    ### Break free from your news bubble. Get the FULL story.

    **The Problem:** Every news source has bias. CNN leans left, Fox leans right. TechCrunch loves startups, Reuters stays diplomatic. 
    Your location, their politics, the author's expertise—it all shapes what you read. Relying on 1-2 sources? You're missing half the story.

    **The Solution:** This smart news analyzer automatically:
    - **Finds stories you'd miss** (sources from different countries, politics, industries)
    - **Identifies each source's angle** (who's pro/anti, regional vs global perspective)
    - **Shows you the full debate** (what supporters say vs what critics argue)  
    - **Delivers one balanced summary** (all viewpoints in 2 minutes of reading)

    **Bottom line:** Get the nuanced, multi-angle story in 2 minutes instead of spending an hour tab-hopping between biased sources.

    ---

    **How it works:**
    - 🕷️ **Search Agent**: Crawls Google News for fresh articles
    - 🧠 **Profiler Agent**: Tags sources by tone, region, and bias  
    - 🎯 **Diversity Selector**: Picks articles that actually disagree with each other
    - 🗣️ **Debate Synthesizer**: Crafts a structured report with multiple viewpoints
    - 🎨 **Creative Editor**: Polishes the final output based on selected tone and depth.

    **Pro tip**: Try controversial topics like "AI regulation", "crypto crash", or "remote work debate" for insightful results.
    """)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
Built with Python, Streamlit, and a lot of caffeine :D | <a href="https://github.com/spouyans/news_debate_app" target="_blank">GitHub Project</a>
</div>
""", unsafe_allow_html=True)

