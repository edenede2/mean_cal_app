
import pandas as pd
import streamlit as st

def calculate_weighted_mean(group):
    valid_rows = group.dropna(subset=['finish', 'weight'], how='all')
    total_weight = valid_rows['weight'].sum()
    weighted_scores_sum = (valid_rows['finish'] * valid_rows['weight']).sum()
    if total_weight == 0:
        return None
    return weighted_scores_sum / total_weight

def calculate_overall_weighted_mean(data):
    valid_rows = data.dropna(subset=['finish', 'weight'], how='all')
    total_weight = valid_rows['weight'].sum()
    weighted_scores_sum = (valid_rows['finish'] * valid_rows['weight']).sum()
    if total_weight == 0:
        return None
    return weighted_scores_sum / total_weight

# Sidebar with Help and Downloadable CSV Template
st.sidebar.title("Help and Template")
st.sidebar.write("Download the CSV template to see how to fill in your course data.")
template_csv = "finish,work,exam,weight,semester,type,year,course_name"
st.sidebar.download_button("Download CSV Template", template_csv, "course_template.csv")

# File Upload
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.rename(columns={'simester': 'semester', 'name': 'course_name'}, inplace=True)
    
    # Select multiple courses to retake
    st.write("### Want to retake some courses?")
    course_list = df['course_name'].unique().tolist()
    selected_courses = st.multiselect("Select the courses you'd like to retake:", course_list)
    
    # Create a dictionary to store new scores
    new_scores = {}
    for course in selected_courses:
        new_scores[course] = st.slider(f"New score for {course}:", min_value=0, max_value=100, step=1)
    
    # Take a snapshot of the original data for comparison
    original_ba_data = df[df['type'] == 'ba'].copy()
    original_bsc_data = df[df['type'] == 'bsc'].copy()
    
    # Update the data with the new scores for the selected courses
    for course, score in new_scores.items():
        df.loc[df['course_name'] == course, 'finish'] = score
    
    # Group data and calculate weighted mean
    ba_data = df[df['type'] == 'ba'].copy()
    bsc_data = df[df['type'] == 'bsc'].copy()
    
    # Calculate the overall and yearly weighted means before and after retaking courses
    overall_ba_mean_before = calculate_overall_weighted_mean(original_ba_data)
    overall_bsc_mean_before = calculate_overall_weighted_mean(original_bsc_data)
    overall_ba_mean_after = calculate_overall_weighted_mean(ba_data)
    overall_bsc_mean_after = calculate_overall_weighted_mean(bsc_data)
    
    # Display the before and after overall weighted means
    st.write(f"### Overall Weighted Mean for B.A. Courses: Before {overall_ba_mean_before:.2f}, After {overall_ba_mean_after:.2f}")
    st.write(f"### Overall Weighted Mean for B.Sc. Courses: Before {overall_bsc_mean_before:.2f}, After {overall_bsc_mean_after:.2f}")
else:
    st.warning("You need to upload a CSV or Excel file.")