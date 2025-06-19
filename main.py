import streamlit as st
from app.core.process import process_news

st.set_page_config(page_title="🧠 AI News Debate Synthesizer")
st.title("🧠 AI News Debate Synthesizer")
st.markdown("Enter a topic to generate a multi-perspective, source-aware news report.")

topic = st.text_input("🔍 Topic:", value="artificial intelligence")

if st.button("📝 Generate Report"):
    if topic.strip():
        try:
            with st.status("🧠 Launching agent swarm...", expanded=True) as status:
                def update(msg):
                    status.update(label=msg)
  
                selected_articles, profiling_output, final_report, error = process_news(topic, status_callback=update)    

            if error:
                st.error(f"❌ Something went wrong: {error}")
                
            elif selected_articles and final_report:
                status.update(label="✅ All agents finished. Debate ready!", state="complete")
                st.success("✅ Boom! Your debate report is ready to roll.")

                st.header("📄 The Ultimate News Showdown")
                st.markdown(final_report)

                with st.expander("🧠 Behind-the-Scenes: Sourcing Overview"):
                    st.markdown("Here’s how the agents went from search to synthesis — complete with tags and final picks.")

                    # Build a lookup dict from profiling_output using ID
                    profiling_lookup = {item["id"]: item for item in profiling_output}

                    st.subheader("🔍 All Retrieved Sources")
                    st.markdown("These are the articles originally gathered by the news search agent. They come from reputable sources and form the raw pool of information.") 
                    for article in selected_articles:
                        st.markdown(f"- [{article.get('title', 'Untitled')}]({article.get('url', '#')}) — *{article.get('source', 'Unknown')}*")

                    st.subheader("🏷️ Tags by Agent")
                    st.markdown("The profiler agent analyzed each article for tone, region, type, and perspective — giving us insight into the diversity of the content.")
                    for article in selected_articles:
                        profile = profiling_lookup.get(article["id"], {})
                        tags = []
                        for tag_field in ['region', 'tone', 'type', 'perspective']:
                            if tag_field in profile:
                                tags.append(f"**{tag_field.capitalize()}**: {profile[tag_field]}")
                        st.markdown(f"**{article.get('title', 'Untitled')}**")
                        if tags:
                            st.markdown(", ".join(tags))
                        else:
                            st.markdown("_No tags available_")
                        st.markdown("---")

                    st.subheader("✅ Final Shortlisted Articles")
                    st.markdown("Based on diversity of viewpoints and source characteristics, these articles were selected to build the final debate report.")
                    for article in selected_articles:
                        st.markdown(f"- [{article.get('title', 'Untitled')}]({article.get('url', '#')}) — *{article.get('source', 'Unknown')}*")

            else:
                st.error("⚠️ Something weird happened. Try another topic or give the agents a coffee break.")

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please enter a topic to begin.")
