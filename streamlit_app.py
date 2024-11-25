import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import google.generativeai as genai

# Configure the Gemini AI API key from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Access JIRA credentials from Streamlit Secrets
jira_email = st.secrets["jira"]["email"]
jira_api_token = st.secrets["jira"]["api_token"]
jira_url = st.secrets["jira"]["url"]
jira_project_key = st.secrets["jira"]["project_key"]

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

# Function to summarize feedback using Gemini AI
def summarize_feedback(feedback):
    try:
        # Load and configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate the summarized feedback
        prompt = f"Summarize the following feedback: {feedback}"
        response = model.generate_content(prompt)
        
        # Return the summarized content
        return response.text
    except Exception as e:
        st.error(f"Error with Gemini AI: {e}")
        return feedback  # If AI fails, return the original feedback

# Streamlit App UI
st.title("Advanced Product Feedback Collection System")
st.write("Please provide your feedback to help improve our product.")

# Feedback Form
with st.form(key="feedback_form"):
    st.subheader("Feedback Form")

    # Collecting advanced feedback metrics
    satisfaction = st.slider("How satisfied are you with the product?", min_value=1, max_value=5, step=1)
    usability = st.slider("How easy is the product to use?", min_value=1, max_value=5, step=1)
    design_quality = st.slider("How would you rate the design quality?", min_value=1, max_value=5, step=1)
    feature_feedback = st.text_area("What features do you like the most?", height=100)
    improvement_suggestions = st.text_area("Any suggestions for improvement?", height=100)
    ease_of_use = st.slider("How easy is the product to set up and start using?", min_value=1, max_value=5, step=1)
    support_feedback = st.text_area("How would you rate our customer support?", height=100)
    feature_requests = st.text_area("What additional features would you like to see?", height=100)
    pricing_feedback = st.slider("How satisfied are you with the product's pricing?", min_value=1, max_value=5, step=1)
    overall_feedback = st.text_area("Any additional comments?", height=100)

    # Collecting demographic details
    user_role = st.selectbox("What is your role?", ["Developer", "Product Manager", "Designer", "Business User", "Other"])
    company_size = st.selectbox("What is your company's size?", ["1-10", "11-50", "51-200", "201-1000", "1000+"])
    industry = st.selectbox("Which industry does your company belong to?", ["Tech", "Finance", "Healthcare", "Retail", "Other"])
    
    # Collecting feedback on the platform used
    platform = st.selectbox("Which platform are you using?", ["Web", "iOS", "Android", "Desktop App"])
    device_type = st.selectbox("Which device are you using?", ["Smartphone", "Laptop", "Tablet", "Desktop"])

    # User's frequency of usage
    usage_frequency = st.selectbox("How often do you use the product?", ["Daily", "Weekly", "Monthly", "Rarely"])

    # Additional Features (25 new features)
    ease_of_integration = st.slider("How easy was it to integrate the product into your workflow?", min_value=1, max_value=5, step=1)
    product_stability = st.slider("How stable is the product? (No crashes, errors, etc.)", min_value=1, max_value=5, step=1)
    performance = st.slider("How would you rate the performance of the product?", min_value=1, max_value=5, step=1)
    security_features = st.slider("How satisfied are you with the security features?", min_value=1, max_value=5, step=1)
    product_updates = st.slider("How would you rate the frequency and quality of product updates?", min_value=1, max_value=5, step=1)
    onboarding_process = st.slider("How would you rate the onboarding process for new users?", min_value=1, max_value=5, step=1)
    training_materials = st.slider("How useful are the training materials provided for the product?", min_value=1, max_value=5, step=1)
    user_interface = st.slider("How would you rate the user interface of the product?", min_value=1, max_value=5, step=1)
    documentation = st.slider("How would you rate the product documentation?", min_value=1, max_value=5, step=1)
    language_support = st.selectbox("How satisfied are you with the language support?", ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"])
    mobile_experience = st.slider("How would you rate the product's mobile experience?", min_value=1, max_value=5, step=1)
    feature_relevance = st.slider("How relevant do you find the features for your needs?", min_value=1, max_value=5, step=1)
    data_analysis = st.slider("How useful is the data analysis/reporting feature?", min_value=1, max_value=5, step=1)
    collaboration_tools = st.slider("How well do the collaboration tools in the product work?", min_value=1, max_value=5, step=1)
    customization_options = st.slider("How satisfied are you with the customization options?", min_value=1, max_value=5, step=1)
    scalability = st.slider("How would you rate the scalability of the product for larger teams?", min_value=1, max_value=5, step=1)
    product_value = st.slider("Do you feel the product offers good value for the price?", min_value=1, max_value=5, step=1)
    third_party_integration = st.slider("How well does the product integrate with third-party tools?", min_value=1, max_value=5, step=1)
    data_privacy = st.slider("How would you rate the product's data privacy features?", min_value=1, max_value=5, step=1)
    customer_support_timeliness = st.slider("How timely is the customer support?", min_value=1, max_value=5, step=1)
    live_chat_experience = st.slider("How would you rate the live chat experience with support?", min_value=1, max_value=5, step=1)
    billing_satisfaction = st.slider("How satisfied are you with the billing process?", min_value=1, max_value=5, step=1)
    user_community = st.slider("How helpful do you find the product's user community?", min_value=1, max_value=5, step=1)
    updates_frequency = st.slider("How often do you think the product should be updated?", min_value=1, max_value=5, step=1)
    feature_flexibility = st.slider("How flexible are the product's features to cater to different business needs?", min_value=1, max_value=5, step=1)
    demo_experience = st.slider("How would you rate the demo experience of the product?", min_value=1, max_value=5, step=1)
    
    # Submit button
    submit_button = st.form_submit_button(label="Submit Feedback")

if submit_button:
    st.write("Thank you for your feedback!")

    # Combine feedback into a single string to pass to Gemini AI for summarization
    feedback = (
        f"Satisfaction Rating: {satisfaction}\n"
        f"Usability Rating: {usability}\n"
        f"Design Quality Rating: {design_quality}\n"
        f"Ease of Use: {ease_of_use}\n"
        f"Features Liked: {feature_feedback}\n"
        f"Suggestions for Improvement: {improvement_suggestions}\n"
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
        f"Language Support: {language_support}\n"
        f"Mobile Experience: {mobile_experience}\n"
        f"Feature Relevance: {feature_relevance}\n"
        f"Data Analysis: {data_analysis}\n"
        f"Collaboration Tools: {collaboration_tools}\n"
        f"Customization Options: {customization_options}\n"
        f"Scalability: {scalability}\n"
        f"Product Value: {product_value}\n"
        f"Third-party Integration: {third_party_integration}\n"
        f"Data Privacy: {data_privacy}\n"
        f"Customer Support Timeliness: {customer_support_timeliness}\n"
        f"Live Chat Experience: {live_chat_experience}\n"
        f"Billing Satisfaction: {billing_satisfaction}\n"
        f"User Community: {user_community}\n"
        f"Updates Frequency: {updates_frequency}\n"
        f"Feature Flexibility: {feature_flexibility}\n"
        f"Demo Experience: {demo_experience}\n"
    )
    
    # Summarize feedback using Gemini AI
    summarized_feedback = summarize_feedback(feedback)

    # Prepare feedback data
    feedback_data = {
        'user_id': str(pd.to_datetime("today").strftime('%Y-%m-%d')),  # Using current date as a user ID for this example
        'feedback': summarized_feedback
    }
    
    # Create a JIRA ticket with the summarized feedback
    create_jira_ticket(feedback_data)
