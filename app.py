import streamlit as st
from utils.parser import parse_document
from utils.summarizer import generate_summary
from utils.qa import answer_question
from utils.challenge import generate_questions, evaluate_answer

st.set_page_config(page_title="GenAI Research Assistant", layout="wide")

st.title("📄 GenAI Smart Assistant for Research Summarization")

uploaded_file = st.file_uploader("📂 Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("🔍 Reading and parsing document..."):
        text, paragraphs = parse_document(uploaded_file)

    st.subheader("📌 Document Summary")
    summary = generate_summary(text)
    st.info(summary)

    st.markdown("---")
    mode = st.radio("🔧 Choose a mode:", ["Ask Anything", "Challenge Me"])

    if "memory" not in st.session_state:
        st.session_state.memory = {"last_question": "", "last_answer": ""}

    if mode == "Ask Anything":
        query = st.text_input("💬 Ask a question based on the document (follow-ups allowed):")

        if query:
            # Handle vague follow-up questions
            combined_query = query
            if len(query.split()) < 4 and st.session_state.memory["last_question"]:
                combined_query = st.session_state.memory["last_question"] + " " + query

            answer, ref = answer_question(combined_query, paragraphs)
            st.markdown(answer)
            st.caption(f"📚 Justified by: {ref}")

            # Update memory
            st.session_state.memory["last_question"] = query
            st.session_state.memory["last_answer"] = answer

    elif mode == "Challenge Me":
        st.subheader("🧠 Answer the following logic-based questions:")
        questions = generate_questions(paragraphs)
        user_answers = []

        for i, q in enumerate(questions):
            user_input = st.text_input(f"Q{i+1}: {q['question']}", key=f"q_{i}")
            user_answers.append((q, user_input))

        if st.button("✅ Submit Answers"):
            for i, (qdata, user_input) in enumerate(user_answers):
                is_correct, feedback = evaluate_answer(user_input, qdata["answer"])
                st.markdown(f"**Q{i+1}: {qdata['question']}**")
                st.caption(f"📍 Source: {qdata['source']}")
                if is_correct:
                    st.success(f"✅ Correct! {feedback}")
                else:
                    st.error(f"❌ Incorrect. {feedback}")
