import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Personal Study Assistant",
    page_icon="📚",
    layout="wide"
)


st.title("📚 AI Personal Study Assistant")

st.write(
    "Your AI-powered study companion for learning, "
    "quizzes, revision and study planning."
)


st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a feature",
    [
        "💬 Ask Your Notes",
        "👨‍🏫 AI Tutor",
        "📝 Quiz",
        "📅 Study Planner",
        "🔄 Revision",
        "📊 Progress"
    ]
)


if page == "💬 Ask Your Notes":

    st.header("Ask Your Notes")

    question = st.text_input(
        "Ask a question about your uploaded notes"
    )

    if st.button("Ask"):

        if not question:
            st.warning("Please enter a question.")
        else:

            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "message": question
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.success("Answer")

                st.write(data["response"])

                if data["sources"]:
                    st.subheader("Sources")

                    for source in data["sources"]:
                        st.write(
                            f"📄 {source['filename']} "
                            f"(Chunk {source['chunk_index']})"
                        )

            else:
                st.error(
                    f"Error: {response.text}"
                )


elif page == "👨‍🏫 AI Tutor":

    st.header("AI Tutor")

    question = st.text_input(
        "What do you want me to explain?"
    )

    if st.button("Explain"):

        if not question:
            st.warning("Please enter a topic.")
        else:

            response = requests.post(
                f"{API_URL}/tutor",
                json={
                    "question": question
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.success("Tutor Explanation")

                st.write(data["answer"])

            else:
                st.error(
                    f"Error: {response.text}"
                )


elif page == "📝 Quiz":

    st.header("Quiz Generator")

    topic = st.text_input(
        "Enter topic"
    )

    num_questions = st.number_input(
        "Number of questions",
        min_value=1,
        max_value=10,
        value=5
    )

    if st.button("Generate Quiz"):

        if not topic:
            st.warning("Please enter a topic.")
        else:

            response = requests.post(
                f"{API_URL}/quiz",
                json={
                    "topic": topic,
                    "num_questions": num_questions
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.session_state["quiz"] = data["questions"]

                st.success("Quiz generated!")

            else:
                st.error(
                    f"Error: {response.text}"
                )


    if "quiz" in st.session_state:

        st.subheader("Your Quiz")

        answers = {}

        for index, question in enumerate(
            st.session_state["quiz"]
        ):

            st.write(
                f"**Q{index + 1}. "
                f"{question['question']}**"
            )

            answer = st.radio(
                "Choose an answer:",
                list(question["options"].keys()),
                format_func=lambda x: (
                    f"{x}. {question['options'][x]}"
                ),
                key=f"question_{index}"
            )

            answers[str(index)] = answer

        if st.button("Submit Quiz"):

            correct = 0

            for index, question in enumerate(
                st.session_state["quiz"]
            ):

                if answers[str(index)] == question[
                    "correct_answer"
                ]:
                    correct += 1

            total = len(
                st.session_state["quiz"]
            )

            score = (correct / total) * 100

            st.success(
                f"Score: {correct}/{total} "
                f"({score:.2f}%)"
            )


elif page == "📅 Study Planner":

    st.header("Study Planner")

    subjects = st.text_input(
        "Subjects (comma separated)"
    )

    days = st.number_input(
        "Number of days",
        min_value=1,
        max_value=30,
        value=7
    )

    hours = st.number_input(
        "Study hours per day",
        min_value=0.5,
        max_value=12.0,
        value=3.0
    )

    if st.button("Create Study Plan"):

        if not subjects:
            st.warning("Please enter subjects.")
        else:

            subject_list = [
                subject.strip()
                for subject in subjects.split(",")
            ]

            response = requests.post(
                f"{API_URL}/planner",
                json={
                    "subjects": subject_list,
                    "days": days,
                    "hours_per_day": hours
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.success("Study plan generated!")

                st.json(data)

            else:
                st.error(
                    f"Error: {response.text}"
                )


elif page == "🔄 Revision":

    st.header("Revision Assistant")

    topic = st.text_input(
        "Enter topic to revise"
    )

    if st.button("Create Revision"):

        if not topic:
            st.warning("Please enter a topic.")
        else:

            response = requests.post(
                f"{API_URL}/revision",
                json={
                    "topic": topic
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.subheader("Summary")

                st.write(data["summary"])

                st.subheader("Key Points")

                for point in data["key_points"]:
                    st.write(f"• {point}")

                st.subheader("Revision Questions")

                for question in data[
                    "revision_questions"
                ]:
                    st.write(f"❓ {question}")

            else:
                st.error(
                    f"Error: {response.text}"
                )


elif page == "📊 Progress":

    st.header("Progress Dashboard")

    response = requests.get(
        f"{API_URL}/progress/summary"
    )

    if response.status_code == 200:

        data = response.json()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Study Hours",
            data["total_study_hours"]
        )

        col2.metric(
            "Average Quiz Score",
            f"{data['average_quiz_score']}%"
        )

        col3.metric(
            "Completed Topics",
            data["completed_topics"]
        )

        col4.metric(
            "Total Topics",
            data["total_topics"]
        )

    else:
        st.error(
            f"Error: {response.text}"
        )