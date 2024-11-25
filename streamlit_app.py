import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Access JIRA credentials from Streamlit Secrets
jira_email = st.secrets["jira"]["email"]
jira_api_token = st.secrets["jira"]["api_token"]
jira_url = st.secrets["jira"]["url"]
jira_project_key = st.secrets["jira"]["project_key"]

# Function to create a JIRA ticket
def create_jira_ticket(feedback_data):
    url = f"{jira_url}/rest/api/2/issue/"

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

    # Authenticate using Basic Auth
    auth = (jira_email, jira_api_token)

    # Send the request to create a new ticket
    response = requests.post(url, json=issue_data, auth=auth)

    if response.status_code == 201:
        st.success("JIRA ticket created successfully!")
    else:
        st.error(f"Error creating JIRA ticket: {response.status_code} - {response.text}")

# Streamlit App UI
st.title("Product Feedback Collection System")
st.write("Please provide your feedback to help improve our product.")

# Feedback Form
with st.form(key="feedback_form"):
    st.subheader("Product Feedback Form")

    # Collecting advanced feedback metrics
    satisfaction = st.slider("How satisfied are you with the product?", min_value=1, max_value=5, step=1)
    usability = st.slider("How easy is the product to use?", min_value=1, max_value=5, step=1)
    design_quality = st.slider("How would you rate the design quality?", min_value=1, max_value=5, step=1)
    ease_of_use = st.slider("How easy is the product to set up and start using?", min_value=1, max_value=5, step=1)
    support_feedback = st.text_area("How would you rate our customer support?", height=100)
    feature_requests = st.text_area("What additional features would you like to see?", height=100)
    pricing_feedback = st.slider("How satisfied are you with the product's pricing?", min_value=1, max_value=5, step=1)
    overall_feedback = st.text_area("Any additional comments?", height=100)

    # Collecting additional product-related feedback
    ease_of_integration = st.slider("How easy was it to integrate the product into your workflow?", min_value=1, max_value=5, step=1)
    product_stability = st.slider("How stable is the product? (No crashes, errors, etc.)", min_value=1, max_value=5, step=1)
    performance = st.slider("How would you rate the performance of the product?", min_value=1, max_value=5, step=1)
    security_features = st.slider("How satisfied are you with the security features?", min_value=1, max_value=5, step=1)
    product_updates = st.slider("How would you rate the frequency and quality of product updates?", min_value=1, max_value=5, step=1)
    onboarding_process = st.slider("How would you rate the onboarding process for new users?", min_value=1, max_value=5, step=1)
    training_materials = st.slider("How useful are the training materials provided for the product?", min_value=1, max_value=5, step=1)
    user_interface = st.slider("How would you rate the user interface of the product?", min_value=1, max_value=5, step=1)
    documentation = st.slider("How would you rate the product documentation?", min_value=1, max_value=5, step=1)
    mobile_experience = st.slider("How would you rate the product's mobile experience?", min_value=1, max_value=5, step=1)
    feature_relevance = st.slider("How relevant do you find the features for your needs?", min_value=1, max_value=5, step=1)
    data_analysis = st.slider("How useful is the data analysis/reporting feature?", min_value=1, max_value=5, step=1)
    collaboration_tools = st.slider("How well do the collaboration tools in the product work?", min_value=1, max_value=5, step=1)
    customization_options = st.slider("How satisfied are you with the customization options?", min_value=1, max_value=5, step=1)
    product_value = st.slider("Do you feel the product offers good value for the price?", min_value=1, max_value=5, step=1)

    # Submit button
    submit_button = st.form_submit_button(label="Submit Feedback")

if submit_button:
    st.write("Thank you for your feedback!")

    # Combine feedback into a single string to pass to JIRA
    feedback = (
        f"Satisfaction Rating: {satisfaction}\n"
        f"Usability Rating: {usability}\n"
        f"Design Quality Rating: {design_quality}\n"
        f"Ease of Use: {ease_of_use}\n"
        f"Customer Support Rating: {support_feedback}\n"
        f"Feature Requests: {feature_requests}\n"
        f"Pricing Feedback: {pricing_feedback}\n"
        f"Overall Feedback: {overall_feedback}\n"
        f"Ease of Integration: {ease_of_integration}\n"
        f"Product Stability: {product_stability}\n"
        f"Performance: {performance}\n"
        f"Security Features: {security_features}\n"
        f"Product Updates: {product_updates}\n"
        f"Onboarding Process: {onboarding_process}\n"
        f"Training Materials: {training_materials}\n"
        f"User Interface: {user_interface}\n"
        f"Documentation: {documentation}\n"
        f"Mobile Experience: {mobile_experience}\n"
        f"Feature Relevance: {feature_relevance}\n"
        f"Data Analysis: {data_analysis}\n"
        f"Collaboration Tools: {collaboration_tools}\n"
        f"Customization Options: {customization_options}\n"
        f"Product Value: {product_value}\n"
    )
    
    feedback_data = {
        'user_id': str(pd.to_datetime("today").strftime('%Y-%m-%d')),  # Using current date as a user ID for this example
        'feedback': feedback
    }
    
    # Create a JIRA ticket
    create_jira_ticket(feedback_data)
