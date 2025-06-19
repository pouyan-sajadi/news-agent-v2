import streamlit as st
from app.core.process import process_news

st.set_page_config(page_title="🧠 AI News Debate Synthesizer")
st.title("🧠 AI News Debate Synthesizer")
st.markdown("Enter a topic to generate a multi-perspective, source-aware news report.")

topic = st.text_input("🔍 Topic:", value="artificial intelligence")

if st.button("📝 Generate Report"):
    if topic.strip():
        try:
            with st.spinner("🕵️ Scanning the web for fresh news and crafting a smart, source-rich report — this may take up to 2 minutes..."):
                selected_articles, profiling_output, final_report, error = process_news(topic)

            if error:
                st.error(f"❌ An error occurred: {error}")
            elif selected_articles and final_report:
                st.success("✅ Boom! Your debate report is ready to roll.")

                st.header("📄 The Ultimate News Showdown")
                st.markdown(final_report)

                with st.expander("🧠 Behind-the-Scenes: Source Profiling"):
                    st.markdown("Ever wondered how your news sources vibe? Here’s how the AI sized them up.")
                    st.json(profiling_output)

                with st.expander("📰 The Chosen Ones (a.k.a. Selected Articles)"):
                    st.markdown("These are the MVPs that made it into the final debate — handpicked by our AI crew.")
                    for a in selected_articles:
                        st.markdown(f"**{a['title']}** — {a['source']} ({a['date']})  \n[Read full article]({a['url']})")
            else:
                st.error("⚠️ Something weird happened. Try another topic or give the agents a coffee break.")

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please enter a topic to begin.")
