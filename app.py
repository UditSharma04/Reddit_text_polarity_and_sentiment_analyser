import asyncio
import os
import streamlit as st

from config.config import REDDIT_CONFIG
from src.reddit_client import RedditClient
from src.text_analysis import TextAnalyzer
from src.sentiment_analysis import calculate_sentiment_distribution
from src.entity_analysis import EntityAnalyzer
from src.visualization import Visualizer
from src.content_generator import ContentGenerator


st.set_page_config(page_title="Reddit Analyzer", page_icon="🔎", layout="centered")
st.title("Reddit Analyzer (Simple Demo)")
st.caption("Analyze Reddit topics and get help drafting a post or answering questions.")


@st.cache_resource
def get_cached_components():
    return (
        RedditClient(**REDDIT_CONFIG),
        TextAnalyzer(),
        EntityAnalyzer(),
        Visualizer(),
    )


reddit_client, text_analyzer, entity_analyzer, visualizer = get_cached_components()
content_generator = ContentGenerator()

query = st.text_input("What topic do you want to analyze?", placeholder="e.g., AI in education")
limit = st.slider("Number of results", min_value=5, max_value=100, value=20, step=5)

analyze_clicked = st.button("Analyze")


async def analyze(query_text: str, limit_num: int):
    keywords = text_analyzer.extract_keywords(query_text)
    search_query = " ".join(keywords) or query_text
    results = await reddit_client.search_reddit(search_query, limit=limit_num)
    return keywords, results


if analyze_clicked and query:
    with st.spinner("Searching Reddit and analyzing..."):
        try:
            keywords, results = asyncio.run(analyze(query, limit))
        except RuntimeError:
            # In case of running inside an existing event loop (rare in Streamlit)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            keywords, results = loop.run_until_complete(analyze(query, limit))

    if results:
        sentiments = calculate_sentiment_distribution(results)
        st.subheader("Sentiment Distribution")
        fig = visualizer.figure_sentiment_distribution(sentiments)
        st.pyplot(fig)

        st.subheader("Top Keywords")
        texts = [r['text'] for r in results if r.get('text')]
        combined = " ".join(texts)
        top_keywords = text_analyzer.extract_top_keywords(combined)
        if top_keywords:
            shown = ", ".join([w for _, w in top_keywords[:20]])
            st.write(shown)
        else:
            st.write("No keywords found.")

        st.subheader("Named Entities")
        entities = entity_analyzer.extract_entities(combined)
        if entities:
            for etype, elist in entities.items():
                if elist:
                    st.markdown(f"**{etype}**: " + ", ".join(sorted(set(elist))[:30]))
        else:
            st.write("No entities detected.")

        # Provide analysis context to the chatbot so follow-ups stay on topic
        content_generator.set_context(topic=query, keywords=top_keywords, sentiment_data=sentiments, entities=entities)

        st.subheader("Suggested Summary Post")
        post = content_generator.generate_content(query=query, keywords=top_keywords, sentiment_data=sentiments)
        if post and post[0]:
            st.success(post[0])
        else:
            st.info("Could not generate content right now. Try again or adjust the topic.")

st.subheader("Chat: Ask for help or refine your post")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_analyzed_query" not in st.session_state:
    st.session_state.last_analyzed_query = None

# Reset chat history if the analyzed query changed
if st.session_state.last_analyzed_query != query and query:
    st.session_state.chat_history = []
    st.session_state.last_analyzed_query = query

# Render chat messages in order using Streamlit's chat UI
for role, msg in st.session_state.chat_history:
    with st.chat_message("user" if role == "you" else "assistant"):
        st.markdown(msg)

# Chat input at the bottom; show loader while generating
user_msg = st.chat_input("Ask a question or request a rewrite…")
if user_msg:
    st.session_state.chat_history.append(("you", user_msg))
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            reply = content_generator.chat_reply(user_msg)
            reply = reply or "I'm having trouble responding right now. Please try again."
            st.markdown(reply)
    st.session_state.chat_history.append(("assistant", reply))



