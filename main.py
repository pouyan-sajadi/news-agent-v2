import streamlit as st
from app.core.process import process_news
from app.core.logger import logger

st.set_page_config(
    page_title="News Agent Swarm", 
    page_icon="🤖",
    layout="wide"
)

st.title("🗞️ News Agent Swarm v2")

# Sidebar configuration
with st.sidebar:
    st.header("🎛️ Customize Your News Experience")
    
    # Focus Dial
    st.subheader("🎯 Focus Dial")
    focus = st.radio(
        "What matters most to you?",
        options=[
            "Just the facts",
            "Human Impact", 
            "The Clash",
            "Hidden Angles",
            "The Money Trail"
        ],
        index=0
    )
    st.session_state.focus = focus
    st.divider()
    
    # Depth Level
    st.subheader("🔍 Reading Depth")
    depth = st.select_slider(
        "How much time do you have?",
        options=[1, 2, 3],
        value=2,
        format_func=lambda x: {
            1: "Quick Hit (30 sec)",
            2: "Espresso Shot (2 min)",
            3: "Coffee Break (5+ min)"
        }[x]
    )
    st.session_state.depth = depth
    
    st.divider()
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

**What it does:**
- 🕷️ **Search Agent**: Crawls Google News for fresh articles
- 🧠 **Profiler Agent**: Tags sources by tone, region, and bias  
- 🎯 **Diversity Selector**: Picks articles that actually disagree with each other
- 🗣️ **Debate Synthesizer**: Crafts a structured report with multiple viewpoints

**Pro tip**: Try controversial topics like "AI regulation", "crypto crash", or "remote work debate" for spicy results 
""")

# Input Section  
st.markdown("---")
col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input(
        "**🎯 Drop your topic here:**", 
        value="artificial intelligence",
        placeholder="e.g., 'ChatGPT impact on jobs', 'Tesla stock volatility', 'climate change solutions'"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  
    generate_btn = st.button("**Deploy Agents**", type="primary", use_container_width=True)

if generate_btn:
    if topic.strip():
        logger.info(f"🧠 User requested topic: {topic}")
        try:
            logger.info("🚀 Starting agentic pipeline for topic: %s", topic)
            
            # Progress Section
            st.markdown("---")
            st.markdown("### 🤖 Agent Swarm Status")
            st.markdown("*Grab a coffee - this might take **2-3 minutes** while the agents do their magic...*")
            
            with st.status("🚀 Initializing agent swarm...", expanded=True) as status:
                def update(msg):
                    status.update(label=f"{msg}")
  
                raw_news_list, selected_articles, profiling_output, final_report, error = process_news(topic, user_preferences={'focus': focus, 'depth' : depth}, status_callback=update)    

            if error:
                st.error(f"💥 **Agent swarm crashed:** {error}")
                st.markdown("*Try a different topic or wait a moment for the APIs to recover...*")
                logger.exception(f"❌ Unhandled error during processing: {str(error)}")
                
            elif selected_articles and final_report:
                status.update(label="✅ Mission accomplished! All agents reporting success 🎉", state="complete")
                
                # Success Message
                st.balloons()
                st.success("🎉 **BOOM!** Your multi-perspective news analysis is ready to consume.")
                logger.info("✅ Report generation completed successfully")
                
                # Main Report
                st.markdown("---")
                st.header("📰 The Debate Breakdown")
                st.markdown("*Here's what the agents found when they went digging...*")
                st.markdown(final_report)

                # Debug/Technical Details
                st.markdown("---")
                with st.expander("🔍 **Nerd Stats** - See how the report was generated under the hood"):
                    st.markdown("""
                    **For the curious minds who want to peek under the hood...**
                    
                    This shows the complete agent workflow: from raw search results → 
                    AI-powered source profiling → diversity filtering → final synthesis.
                    """)

                    profiling_lookup = {item["id"]: item for item in profiling_output}

                    with st.expander("🕷️ **Raw Intel** - What Search Agent found"):
                        st.markdown(f"**{len(raw_news_list)} articles** scraped from Google News (before filtering):") 
                        for i, article in enumerate(raw_news_list, 1):
                            st.markdown(f"{i}. [{article.get('title', 'Untitled')}]({article.get('url', '#')}) - *{article.get('source', 'Unknown')}*")

                    with st.expander("🏷️ **AI Profiling** - How each source was tagged"):
                        st.markdown("Our **Profiler Agent** analyzed each article's vibe, geography, and bias:")
                        for article in raw_news_list:
                            profile = profiling_lookup.get(article["id"], {})
                            tags = []
                            for tag_field in ['region', 'tone', 'type', 'perspective']:
                                if tag_field in profile:
                                    tags.append(f"**{tag_field.title()}**: `{profile[tag_field]}`")
                            
                            st.markdown(f"**📄 {article.get('title', 'Untitled')}**")
                            if tags:
                                st.markdown(" • ".join(tags))
                            else:
                                st.markdown("*Agent couldn't analyze this one* 🤷")
                            st.markdown("---")

                    with st.expander("🎯 **Final Selection** - The chosen ones"):
                        st.markdown(f"**Diversity Selector Agent** picked these **{len(selected_articles)} articles** for maximum perspective clash:")
                        for i, article in enumerate(selected_articles, 1):
                            st.markdown(f"{i}. [{article.get('title', 'Untitled')}]({article.get('url', '#')}) - *{article.get('source', 'Unknown')}*")

            else:
                st.error("🤔 **Hmm, that's weird...** The agents returned empty-handed.")
                st.markdown("*Try a different topic, or maybe the agents are on a union break 🛠️*")
                logger.exception(f"❌ Empty results returned")

        except Exception as e:
            st.error(f"💥 **Something broke:** {str(e)}")
            st.markdown("*Our agents might be overwhelmed. Try again in a moment, or ping the developer 🐛*")
            logger.error(f"❌ Unhandled error during processing: {str(e)}")

    else:   
        st.warning("🎯 **Hey!** You forgot to enter a topic. The agents need something to work with!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
💡 <strong>How it works:</strong> OpenAI Swarm orchestrates multiple LLM agents • SerpAPI for news search • Real-time article scraping<br>
🛠️ Built with Python, Streamlit, and a lot of caffeine ☕
</div>
""", unsafe_allow_html=True)