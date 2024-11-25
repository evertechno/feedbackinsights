import streamlit as st
import google.generativeai as genai
import requests
from datetime import datetime

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Access JIRA credentials from Streamlit Secrets
jira_email = st.secrets["jira"]["email"]
jira_api_token = st.secrets["jira"]["api_token"]
jira_url = st.secrets["jira"]["url"]
jira_project_key = st.secrets["jira"]["project_key"]

# Function to create a JIRA ticket
def create_jira_ticket(feedback_summary):
    url = f"{jira_url}/rest/api/2/issue/"
    
    # Log project key and other params for debugging
    st.write(f"JIRA Project Key: {jira_project_key}")
    
    # Prepare the data for the JIRA issue
    issue_data = {
        "fields": {
            "project": {
                "key": jira_project_key
            },
            "summary": "Product Feedback Summary",
            "description": f"Feedback Summary: {feedback_summary}",
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

# Streamlit App UI
st.title("Product Feedback Collection with Gemini AI")
st.write("Provide your feedback to help improve our product. We'll summarize it for you!")

# Feedback Form - Asking limited relevant questions
with st.form(key="feedback_form"):
    st.subheader("Feedback Form")

    satisfaction = st.slider("How satisfied are you with the product?", min_value=1, max_value=5, step=1)
    usability = st.slider("How easy is the product to use?", min_value=1, max_value=5, step=1)
    improvement_suggestions = st.text_area("Any suggestions for improvement?", height=100)
    feature_requests = st.text_area("What additional features would you like to see?", height=100)

    # Submit button
    submit_button = st.form_submit_button(label="Submit Feedback")

# When the user submits feedback
if submit_button:
    st.write("Thank you for your feedback!")

    # Combine feedback into a string
    feedback = (
        f"Satisfaction Rating: {satisfaction}\n"
        f"Usability Rating: {usability}\n"
        f"Suggestions for Improvement: {improvement_suggestions}\n"
        f"Feature Requests: {feature_requests}\n"
    )

    # Generate a summary using Gemini AI
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Summarize the following product feedback in a concise and clear way:\n{feedback}"
        response = model.generate_content(prompt)
        
        feedback_summary = response.text.strip()
        st.write("Generated Summary:")
        st.write(feedback_summary)
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        feedback_summary = "Could not generate a summary."

    # Create the JIRA ticket
    feedback_data = {
        'user_id': str(datetime.now().strftime('%Y-%m-%d')),  # Use current date as user ID
        'feedback': feedback_summary
    }
    
    create_jira_ticket(feedback_summary)
