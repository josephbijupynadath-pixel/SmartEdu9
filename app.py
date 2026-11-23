from modules.recommendation import recommend_resources
from modules.prediction import predict_marks, load_training_data, evaluate_model
import streamlit as st
import pandas as pd
# Page configuration
st.set_page_config(
    page_title="SmartEdu",
    page_icon="🎓",
    layout="wide"
)

def get_active_dataset():
    active_df = st.session_state.get("active_dataset_df")
    active_name = st.session_state.get("active_dataset_name")
    if active_df is not None and not active_df.empty:
        return active_df.copy(), active_name or "Uploaded Dataset"
    return load_training_data(), "Default Dataset (students.csv)"

# Custom styling
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.block-container {
    padding-top: 2rem;
}
h1 {
    color: #183153;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎓 SmartEdu")
st.sidebar.caption("Smart Education System")
st.sidebar.divider()

page = st.sidebar.radio(
    "MAIN MENU",
    [
        "Home",
        "Student Dashboard",
        "AI Prediction",
        "Learning Resources",
        "Blockchain Security",
        "Research Results",
        "Dataset Management"
    ]
)

st.sidebar.divider()
st.sidebar.info("AI-Based Personalized Learning & Secure Academic Records")

# HOME PAGE
if page == "Home":

    st.title("🎓 Welcome to SmartEdu")

    st.subheader(
        "AI-Based Personalized Learning and "
        "Blockchain-Secured Academic Records"
    )

    st.write(
        "SmartEdu is an intelligent educational platform "
        "designed to support personalized learning, "
        "student performance prediction and secure "
        "academic record verification."
    )

    st.divider()

    st.subheader("Application Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📊 Student Dashboard")
        st.write("Monitor student learning and academic performance.")

    with col2:
        st.info("🤖 AI Prediction")
        st.write("Predict student performance using Machine Learning.")

    with col3:
        st.info("📚 Personalized Learning")
        st.write("Provide suitable learning resources.")

    col4, col5, col6= st.columns(3)

    with col4:
        st.info("🔐 Blockchain Security")
        st.write("Verify the integrity of academic records.")

    with col5:
        st.info("📈 Research Results")
        st.write("Evaluate model performance and research findings.")
    with col6:
        st.info("📁 **Dataset Management**")
        st.write("Upload and manage multiple student datasets.")

    st.divider()

    st.success("Welcome! Select a page from the sidebar to continue.")

# STUDENT DASHBOARD
elif page == "Student Dashboard":

    import pandas as pd

    st.title("📊 Student Dashboard")
    st.write("Student academic performance overview.")

    # Load student dataset
    df, dataset_name = get_active_dataset()
    st.caption(f"Active Dataset: {dataset_name}")

    # Display student statistics
    st.subheader("Student Statistics")  

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", len(df))
    col2.metric("Average Marks", round(df["Marks"].mean(), 2))
    col3.metric("Average Attendance", round(df["Attendance"].mean(), 2))
    col4.metric("Departments", df["Department"].nunique())

    # Display student records
    st.subheader("Student Academic Records")
    st.dataframe(df,width="stretch")

    # Marks visualization
    st.subheader("Student Marks Analysis")
    st.bar_chart(df.set_index("Student_Name")["Marks"])

    # Attendance visualization
    st.subheader("Student Attendance Analysis")
    st.bar_chart(df.set_index("Student_Name")["Attendance"])


# AI PREDICTION
elif page == "AI Prediction":

    st.title("🤖 AI-Based Student Performance Prediction")

    st.write("Predict student academic performance using Machine Learning.")

    try:
        df = load_training_data()

        st.subheader("Enter Student Details")

        col1, col2 = st.columns(2)

        with col1:
            department = st.selectbox(
                "Select Department",
                sorted(df["Department"].unique())
            )

            semester = st.selectbox(
                "Select Semester",
                sorted(df["Semester"].unique())
            )

        with col2:
            subject = st.selectbox(
                "Select Subject",
                sorted(df["Subject"].unique())
            )

            attendance = st.slider(
                "Attendance Percentage",
                0, 100, 80
            )

        if st.button("Predict Student Performance"):

            marks = predict_marks(
                department,
                semester,
                subject,
                attendance
            )

            st.subheader("Prediction Results")

            st.metric("Predicted Marks", f"{marks}/100")

            if marks >= 85:
                category = "Excellent"
                st.success("Excellent Performance!")

            elif marks >= 70:
                category = "Good"
                st.success("Good Performance!")

            elif marks >= 50:
                category = "Average"
                st.warning("Average Performance")

            else:
                category = "At Risk"
                st.error("Student Needs Academic Support")

            st.write("Performance Category:", category)

            st.progress(int(marks))

            st.info(
                "Recommendation: Continue regular learning "
                "and maintain good attendance."
            )

        st.caption(
            f"Model trained using {len(df)} student records."
        )

    except Exception as e:
        st.error(f"Prediction error: {e}")

# LEARNING RESOURCES
elif page == "Learning Resources":

    st.title("📚 Personalized Learning Resources")

    st.write("Learning materials based on student academic needs.")

    df, dataset_name = get_active_dataset()
    st.caption(f"Active Dataset: {dataset_name}")

    subjects = sorted(df["Subject"].dropna().unique()) if "Subject" in df.columns else ["Database"]
    subject = st.selectbox("Select Subject", subjects)

    marks = st.slider("Enter Student Marks", 0, 100, 70)
    attendance = st.slider("Attendance Percentage", 0, 100, 82)


    if st.button("Get Learning Recommendations"):

        recommendations = recommend_resources(
            subject, marks, attendance
        )

        st.subheader("Recommended Learning Resources")

        for item in recommendations:
            st.write(f"📌 {item}")
            
            
# BLOCKCHAIN SECURITY

elif page == "Blockchain Security":

    st.title("🔒 Blockchain Academic Record Security")
    st.write("Secure academic records and verify their integrity.")

    df, dataset_name = get_active_dataset()
    st.caption(f"Active Dataset: {dataset_name}")

    default_id = "103"
    default_name = "Rahul"
    default_grade = "A+"

    if not df.empty and {"Student_ID", "Student_Name", "Marks"}.issubset(df.columns):
        use_selected = st.checkbox("Load student details from active dataset")
        if use_selected:
            labels = [
                f"{row['Student_ID']} - {row['Student_Name']} ({row['Marks']} marks)"
                for _, row in df.iterrows()
            ]
            chosen_idx = st.selectbox(
                "Pick a student record",
                range(len(labels)),
                format_func=lambda i: labels[i]
            )
            chosen_row = df.iloc[chosen_idx]
            default_id = str(chosen_row["Student_ID"])
            default_name = str(chosen_row["Student_Name"])
            score = float(chosen_row["Marks"])
            default_grade = (
                "A+" if score >= 90 else
                "A" if score >= 80 else
                "B+" if score >= 70 else
                "B" if score >= 60 else
                "C" if score >= 50 else "F"
            )

    st.subheader("Create Secure Academic Record")
    student_id = st.text_input("Student ID", value=default_id)
    student_name = st.text_input("Student Name", value=default_name)
    academic_grade = st.text_input("Academic Grade", value=default_grade)

    if st.button("Generate Blockchain Record"):

        if student_id and student_name and grade:

            record = {
                "student_id": student_id,
                "name": student_name,
                "grade": grade
            }

            blockchain = create_blockchain([record])

            st.session_state["blockchain"] = blockchain

            st.success("Academic record secured successfully!")

            st.write("Generated SHA-256 Hash:")

            st.code(blockchain[0]["hash"])

        else:
            st.warning("Please fill in all fields.")

    st.divider()

    st.subheader("Verify Academic Record")

    if "blockchain" in st.session_state:

        if st.button("Verify Blockchain"):

            if verify_blockchain(st.session_state["blockchain"]):
                st.success("Blockchain is valid. Record integrity verified!")
            else:
                st.error("Blockchain verification failed!")

    else:
        st.info("Generate an academic record first.")

# RESEARCH RESULTS
elif page == "Research Results":
    st.title("📊 Research Results")
    st.write("Machine Learning Model Evaluation and Research Analysis.")
    df, dataset_name = get_active_dataset()
    st.caption(f"Active Dataset: {dataset_name}")
    try:
        results = evaluate_model(df=df)

        col1, col2, col3 = st.columns(3)
        col1.metric("MAE", results["MAE"])
        col2.metric("RMSE", results["RMSE"])
        col3.metric("R² Score", results["R2 Score"])

        c1, c2 = st.columns(2)
        c1.metric("Training Records", results["Training Records"])
        c2.metric("Testing Records", results["Testing Records"])

        st.subheader("Actual vs. Predicted Marks")
        st.dataframe(results["Comparison"], width="stretch")
        st.bar_chart(results["Comparison"])
    except Exception as e:
        st.error(f"Evaluation error: {e}")
# DATASET MANAGEMENT
elif page == "Dataset Management":

    st.title("📂 Dataset Management")

    st.write(
        "Upload and manage multiple student academic datasets."
    )

    st.subheader("Upload Student Datasets")

    uploaded_files = st.file_uploader(
        "Choose CSV files",
        type=["csv"],
        accept_multiple_files=True
    )

    if "uploaded_datasets" not in st.session_state:
        st.session_state["uploaded_datasets"] = {}

    if uploaded_files:
        for uploaded_file in uploaded_files:
            dataset_name = uploaded_file.name

            try:
                df = pd.read_csv(uploaded_file)

                st.session_state["uploaded_datasets"][
                    dataset_name
                ] = df

                st.success(
                    f"{dataset_name} uploaded successfully!"
                )

            except Exception as e:
                st.error(
                    f"Error reading {dataset_name}: {e}"
                )

    st.divider()

    st.subheader("Available Datasets")

    datasets = st.session_state["uploaded_datasets"]

    if datasets:
        selected_dataset = st.selectbox(
            "Select a dataset",
            list(datasets.keys())
        )

        selected_df = datasets[selected_dataset]

        st.session_state["active_dataset_name"] = selected_dataset
        st.session_state["active_dataset_df"] = selected_df

        st.success(
            f"Selected Dataset: {selected_dataset}"
        )

        st.write("Total Students:", len(selected_df))
        st.write("Total Columns:", len(selected_df.columns))

        st.subheader("Dataset Preview")

        st.dataframe(
            selected_df,
            width="stretch"
        )

    else:
        st.info("Please upload a student CSV dataset.")




