import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import google.generativeai as genai

# Access JIRA credentials from Streamlit Secrets
jira_email = st.secrets["jira"]["email"]
jira_api_token = st.secrets["jira"]["api_token"]
jira_url = st.secrets["jira"]["url"]
jira_project_key = st.secrets["jira"]["project_key"]

# Configure Gemini AI API key from Streamlit secrets
google_api_key = st.secrets["google"]["GOOGLE_API_KEY"]

# Function to create a JIRA ticket
def create_jira_ticket(feedback_data):
    url = f"{jira_url}/rest/api/2/issue/"
    
    # Log project key and other params for debugging
    st.write(f"JIRA Project Key: {jira_project_key}")
    
    # Prepare the data for the JIRA issue
    issue_data = {
        "fields": {
            "project": {
                "key": jira_project_key
            },
            "summary": f"Feedback - {feedback_data['user_id']}",
            "description": f"Feedback collected on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{feedback_data['feedback']}",
            "issuetype": {
                "name": "Task"  # Change this to the appropriate issue type in your JIRA instance
            }
        }
    }
    
    # Log issue data for debugging
    st.write(f"Issue Data: {issue_data}")

    # Authenticate using Basic Auth
    auth = (jira_email, jira_api_token)

    # Send the request to create a new ticket
    response = requests.post(url, json=issue_data, auth=auth)

    if response.status_code == 201:
        st.success("JIRA ticket created successfully!")
    else:
        st.error(f"Error creating JIRA ticket: {response.status_code} - {response.text}")
        # Display the full response for debugging
        st.write(response.text)

# Function to analyze feedback using Gemini AI
def analyze_feedback(feedback):
    try:
        # Load and configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate analysis or summary of the feedback
        prompt = f"Analyze the following product feedback and summarize key insights:\n\n{feedback}"
        response = model.generate_content(prompt)
        
        # Return the response text (analysis or summary)
        return response.text
    except Exception as e:
        st.error(f"Error analyzing feedback: {e}")
        return None

# Streamlit App UI
st.title("Product Feedback Collection System")
st.write("Please provide your feedback to help improve our product.")

# Feedback Form
with st.form(key="feedback_form"):
    st.subheader("Feedback Form")

    # Collecting key feedback metrics
    satisfaction = st.slider("How satisfied are you with the product?", min_value=1, max_value=5, step=1)
    usability = st.slider("How easy is the product to use?", min_value=1, max_value=5, step=1)
    feature_feedback = st.text_area("What features do you like the most?", height=100)
    improvement_suggestions = st.text_area("Any suggestions for improvement?", height=100)
    pricing_feedback = st.slider("How satisfied are you with the product's pricing?", min_value=1, max_value=5, step=1)
    overall_feedback = st.text_area("Any additional comments?", height=100)

    # Collecting demographic details
    user_role = st.selectbox("What is your role?", ["Developer", "Product Manager", "Designer", "Business User", "Other"])
    
    # User's frequency of usage
    usage_frequency = st.selectbox("How often do you use the product?", ["Daily", "Weekly", "Monthly", "Rarely"])

    # Submit button
    submit_button = st.form_submit_button(label="Submit Feedback")

if submit_button:
    st.write("Thank you for your feedback!")

    # Combine feedback into a single string to pass to JIRA
    feedback = (
        f"Satisfaction Rating: {satisfaction}\n"
        f"Usability Rating: {usability}\n"
        f"Features Liked: {feature_feedback}\n"
        f"Suggestions for Improvement: {improvement_suggestions}\n"
        f"Pricing Feedback: {pricing_feedback}\n"
        f"Overall Feedback: {overall_feedback}\n"
    )
    
    feedback_data = {
        'user_id': str(pd.to_datetime("today").strftime('%Y-%m-%d')),  # Using current date as a user ID for this example
        'feedback': feedback
    }
    
    # Analyze the feedback using Gemini AI
    feedback_analysis = analyze_feedback(feedback)
    
    if feedback_analysis:
        st.write("Feedback Analysis Summary:")
        st.write(feedback_analysis)

    # Create a JIRA ticket
    create_jira_ticket(feedback_data)
