import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


def api_request(method, endpoint, **kwargs):
    try:
        return requests.request(
            method,
            f"{API_URL}{endpoint}",
            timeout=(5, 120),
            **kwargs
        )
    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to the study assistant API. "
            "Start the backend in a separate terminal with "
            "`python -m uvicorn app.main:app --reload`, then try again."
        )
    except requests.exceptions.Timeout:
        st.error("The API request timed out. Please try again.")
    except requests.exceptions.RequestException as exc:
        st.error(f"API request failed: {exc}")
    return None


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

    st.subheader("Upload a PDF")
    uploaded_pdf = st.file_uploader(
        "Choose a PDF to add to your notes",
        type=["pdf"],
        key="notes_pdf_upload",
    )

    if st.button("Upload PDF", disabled=uploaded_pdf is None):
        if uploaded_pdf is not None:
            response = api_request(
                "POST",
                "/documents/upload",
                files={
                    "file": (
                        uploaded_pdf.name,
                        uploaded_pdf.getvalue(),
                        "application/pdf",
                    )
                },
            )

            if response is not None and response.status_code == 200:
                data = response.json()
                st.success(
                    f"Uploaded and indexed {data['filename']} "
                    f"({data['stored_chunks']} chunks)."
                )
            elif response is not None:
                st.error(f"Upload failed: {response.text}")

    st.divider()

    question = st.text_input(
        "Ask a question about your uploaded notes"
    )

    if st.button("Ask"):

        if not question:
            st.warning("Please enter a question.")
        else:

            response = api_request(
                "POST",
                "/chat",
                json={
                    "message": question
                }
            )

            if response is not None and response.status_code == 200:

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
                    st.warning(
                        "No matching content was retrieved from your notes. "
                        "Check that the PDF upload completed successfully "
                        "and try a more specific question."
                    )

            elif response is not None:
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

            response = api_request(
                "POST",
                "/tutor",
                json={
                    "question": question
                }
            )

            if response is not None and response.status_code == 200:

                data = response.json()

                st.success("Tutor Explanation")

                st.write(data["answer"])

            elif response is not None:
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

            response = api_request(
                "POST",
                "/quiz",
                json={
                    "topic": topic,
                    "num_questions": num_questions
                }
            )

            if response is not None and response.status_code == 200:

                data = response.json()

                st.session_state["quiz"] = data["questions"]

                st.success("Quiz generated!")

            elif response is not None:
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

            response = api_request(
                "POST",
                "/planner",
                json={
                    "subjects": subject_list,
                    "days": days,
                    "hours_per_day": hours
                }
            )

            if response is not None and response.status_code == 200:

                data = response.json()

                st.success("Study plan generated!")

                st.json(data)

            elif response is not None:
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

            response = api_request(
                "POST",
                "/revision",
                json={
                    "topic": topic
                }
            )

            if response is not None and response.status_code == 200:

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

            elif response is not None:
                st.error(
                    f"Error: {response.text}"
                )


elif page == "📊 Progress":

    st.header("Progress Dashboard")

    response = api_request(
        "GET",
        "/progress/summary"
    )

    if response is not None and response.status_code == 200:

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

    elif response is not None:
        st.error(
            f"Error: {response.text}"
        )