import streamlit as st
from review.agent.open_agent import get_response

title = st.text_input("Type in your question:", "Where is Kuta?")

def main():
    st.write(get_response(title))

main()
