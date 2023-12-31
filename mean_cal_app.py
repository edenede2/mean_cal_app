
import pandas as pd
import streamlit as st

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
    
def calculate_weighted_mean(group):
    valid_rows = group.dropna(subset=['finish', 'weight'], how='all')
    total_weight = valid_rows['weight'].sum()
    weighted_scores_sum = (valid_rows['finish'] * valid_rows['weight']).sum()
    if total_weight == 0:
        return None
    return weighted_scores_sum / total_weight


def edit_existing_course():
    df = st.session_state.df
    st.write("### Edit Existing Course")
    course_list = df['course_name'].unique().tolist()
    selected_course = st.selectbox("Select a course to edit:", course_list)
    
    # Get the current values for the selected course
    selected_row = df[df['course_name'] == selected_course].iloc[0]
    current_weight = selected_row['weight']
    current_finish_score = selected_row['finish']
    
    # Input new values
    new_weight = st.number_input(f"Edit Weight for {selected_course} (Current: {current_weight}):", min_value=0.0, max_value=10.0, step=0.1)
    new_finish_score = st.number_input(f"Edit Finish Score for {selected_course} (Current: {current_finish_score}):", min_value=0, max_value=100, step=1)
    
    if st.button(f"Update {selected_course}"):
        df.loc[df['course_name'] == selected_course, 'weight'] = new_weight
        df.loc[df['course_name'] == selected_course, 'finish'] = new_finish_score
        st.write(f"{selected_course} has been updated successfully!")
        return df
    return None

def calculate_overall_weighted_mean(data):
    valid_rows = data.dropna(subset=['finish', 'weight'], how='all')
    total_weight = valid_rows['weight'].sum()
    weighted_scores_sum = (valid_rows['finish'] * valid_rows['weight']).sum()
    if total_weight == 0:
        return None
    return weighted_scores_sum / total_weight

# New Functions
# Function to Add New Courses
def add_new_course_updated(session_state_df):
    if st.session_state.df.empty:
        st.warning("No data available to add a new course.")
        return
    
    #st.write("### Add a New Course")
    #course_name = st.text_input("Course Name:")
    #semester = st.radio("Semester:", ('a', 'b'))
    #course_type = st.radio("Type:", ('ba', 'bsc'))
    #year = st.radio("Year:", (1, 2, 3, 4))
    #weight = st.number_input("Weight:", min_value=0.0, max_value=10.0, step=0.1)
    #finish_score = st.number_input("Finish Score:", min_value=0, max_value=100, step=1)

    if st.button("Add Course"):
        new_row = pd.Series({
            'finish': 95,
            'work': None,
            'exam': None,
            'weight': 3,
            'semester': 'a',
            'type': 'ba',
            'year': 1,
            'course_name': 'Intro to Python',
            'difficulty': None
        })

        st.write("Debug Info:")
        st.write("Type of st.session_state.df:", type(st.session_state.df))
        st.write("st.session_state.df head:", st.session_state.df.head())
        st.write("New course added!")

    next_index = len(session_state_df)
    session_state_df.loc[next_index] = new_row
    return session_state_df
    st.write("New course added!")


    
# Function to Rate Course Difficulty
def rate_course_difficulty():
    if st.session_state.df.empty:
        st.warning("No data available to rate a course.")
        return

    st.write("### Rate Course Difficulty")
    course_list = st.session_state.df['course_name'].unique().tolist()
    selected_course = st.selectbox("Select a course to rate:", course_list)
    difficulty = st.slider("Rate the difficulty of the course:", min_value=1, max_value=9, step=1)

    if st.button("Rate Difficulty"):
        st.session_state.df.loc[st.session_state.df['course_name'] == selected_course, 'difficulty'] = difficulty
        st.write(f"Difficulty for course {selected_course} has been rated as {difficulty}!")

# Function to Suggest Courses to Improve Final Score
def suggest_courses_to_improve_score():
    if st.session_state.df.empty:
        st.warning("No data available to rate a course.")
        return
    st.write("### Suggest Courses to Improve Final Score")
    target_score = st.number_input("Target Final Score:", min_value=0, max_value=100, step=1)
    
    for course_type in ['ba', 'bsc']:
        st.write(f"Suggestions for {course_type.upper()} courses:")
        
        # Filter the DataFrame to include only the relevant course_type
        filtered_df = st.session_state.df[st.session_state.df['type'] == course_type]        
        if filtered_df.empty:
            st.write(f"No courses found for type {course_type.upper()}.")
            continue

        # Compute the overall weighted mean for the filtered DataFrame
        overall_weighted_mean = calculate_overall_weighted_mean(filtered_df)
        st.write(f"Current weighted mean for {course_type.upper()}: {overall_weighted_mean if overall_weighted_mean is not None else 'N/A'}")
        
        if overall_weighted_mean is None:
            st.write("Could not compute overall weighted mean.")
            continue

        # Filter out courses that are already highly scored
        potential_courses = filtered_df[filtered_df['finish'] < target_score].copy()
        
        if potential_courses.empty:
            st.write(f"No potential courses to improve for type {course_type.upper()}.")
            continue
        
        # Create 'difficulty' column if it doesn't exist
        if 'difficulty' not in potential_courses.columns:
            potential_courses['difficulty'] = float('nan')
        
        # Fill NaNs with maximum difficulty
        potential_courses['difficulty'].fillna(9, inplace=True)
        
        # Calculate the impact of each course on the final score
        potential_courses['impact'] = potential_courses['weight'] / filtered_df['weight'].sum()
        
        # Calculate impact per unit difficulty
        potential_courses['impact_per_difficulty'] = potential_courses['impact'] / potential_courses['difficulty']
        
        # Sort courses by their impact per unit difficulty
        suggested_courses = potential_courses.sort_values('impact_per_difficulty', ascending=False)
        
        # Show the top 5 suggested courses
        st.write("#### Top 5 Suggested Courses to Help Improve Your Final Score:")
        st.table(suggested_courses.head(5)[['course_name', 'impact', 'difficulty', 'impact_per_difficulty']])

st.title("University Course Manager :brain: :smile: \n by Eden Eldar")

# Sidebar with Help and Downloadable CSV Template
with st.sidebar:
    st.title("Help and Template")
    st.write("Download the CSV template to see how to fill in your course data.")
    template_csv = "finish,work,exam,weight,semester,type,year,course_name"
    st.download_button("Download CSV Template", template_csv, "course_template.csv")

# Download Updated CSV Button
# with st.expander("Download Updated CSV"):
#    def download_link(object_to_download, download_filename, download_link_text):
#        import base64
#        if isinstance(object_to_download, pd.DataFrame):
#            object_to_download = object_to_download.to_csv(index=False)
#        b64 = base64.b64encode(object_to_download.encode()).decode()
#        return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

#    if st.button('Download Updated CSV File'):
#        tmp_download_link = download_link(df, 'updated_courses.csv', 'Click here to download your updated CSV file')
#        st.markdown(tmp_download_link, unsafe_allow_html=True)
#    if df is not None:
#        if st.button('Download Updated CSV File'):
#            tmp_download_link = download_link(df, 'updated_courses.csv', 'Click here to download your updated CSV file')
#            st.markdown(tmp_download_link, unsafe_allow_html=True)
# File Upload
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    uploaded_df = pd.read_csv(uploaded_file)
    uploaded_df.rename(columns={'simester': 'semester', 'name': 'course_name'}, inplace=True)
    if 'difficulty' not in uploaded_df.columns:
        uploaded_df['difficulty'] = float('nan')

    st.session_state.df = uploaded_df

    edit_existing_course()
    st.session_state.df = add_new_course_updated(st.session_state.df)
    if st.session_state.df is not None:
        st.write("New course added!")
    rate_course_difficulty()
    suggest_courses_to_improve_score()

else:
    st.warning("You need to upload a CSV or Excel file.")

with st.expander("Download Updated CSV"):
    def download_link(object_to_download, download_filename, download_link_text):
        import base64
        if isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)
        b64 = base64.b64encode(object_to_download.encode()).decode()
        return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
        
    if st.session_state.df is not None:  # Changed from if df is not None:
        if st.button('Download Updated CSV File', key='download_csv1'):
            tmp_download_link = download_link(st.session_state.df, 'updated_courses.csv', 'Click here to download your updated CSV file')  # Changed from download_link(df, ...)
            st.markdown(tmp_download_link, unsafe_allow_html=True)
st.write("Updated DataFrame:")
st.write(st.session_state.df)
