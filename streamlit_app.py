import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

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

    # Combine feedback into a single string to pass to Gemini
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
        f"Third Party Integration: {third_party_integration}\n"
        f"Data Privacy: {data_privacy}\n"
        f"Customer Support Timeliness: {customer_support_timeliness}\n"
        f"Live Chat Experience: {live_chat_experience}\n"
        f"Billing Satisfaction: {billing_satisfaction}\n"
        f"User Community: {user_community}\n"
        f"Updates Frequency: {updates_frequency}\n"
        f"Feature Flexibility: {feature_flexibility}\n"
        f"Demo Experience: {demo_experience}\n"
        f"User Role: {user_role}\n"
        f"Company Size: {company_size}\n"
        f"Industry: {industry}\n"
        f"Platform: {platform}\n"
        f"Device Type: {device_type}\n"
        f"Usage Frequency: {usage_frequency}\n"
    )

    # Add timestamp and user ID (for tracking if needed)
    user_id = st.text_input("Please enter your User ID (optional)")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_with_meta = f"Timestamp: {timestamp}\nUser ID: {user_id}\n\n{feedback}"

    # Log feedback to a CSV file (can be extended to a database)
    feedback_data = {
        "timestamp": [timestamp],
        "user_id": [user_id],
        "satisfaction": [satisfaction],
        "usability": [usability],
        "design_quality": [design_quality],
        "ease_of_use": [ease_of_use],
        "feature_feedback": [feature_feedback],
        "improvement_suggestions": [improvement_suggestions],
        "support_feedback": [support_feedback],
        "feature_requests": [feature_requests],
        "pricing_feedback": [pricing_feedback],
        "overall_feedback": [overall_feedback],
        "ease_of_integration": [ease_of_integration],
        "product_stability": [product_stability],
        "performance": [performance],
        "security_features": [security_features],
        "product_updates": [product_updates],
        "onboarding_process": [onboarding_process],
        "training_materials": [training_materials],
        "user_interface": [user_interface],
        "documentation": [documentation],
        "language_support": [language_support],
        "mobile_experience": [mobile_experience],
        "feature_relevance": [feature_relevance],
        "data_analysis": [data_analysis],
        "collaboration_tools": [collaboration_tools],
        "customization_options": [customization_options],
        "scalability": [scalability],
        "product_value": [product_value],
        "third_party_integration": [third_party_integration],
        "data_privacy": [data_privacy],
        "customer_support_timeliness": [customer_support_timeliness],
        "live_chat_experience": [live_chat_experience],
        "billing_satisfaction": [billing_satisfaction],
        "user_community": [user_community],
        "updates_frequency": [updates_frequency],
        "feature_flexibility": [feature_flexibility],
        "demo_experience": [demo_experience],
        "user_role": [user_role],
        "company_size": [company_size],
        "industry": [industry],
        "platform": [platform],
        "device_type": [device_type],
        "usage_frequency": [usage_frequency]
    }

    feedback_df = pd.DataFrame(feedback_data)
    feedback_df.to_csv("feedback.csv", mode='a', header=False, index=False)

    # Use Gemini API to generate actionable insights based on feedback
    try:
        # Load and configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate insights from the feedback
        prompt = f"Given the following user feedback, generate actionable insights for the product team:\n\n{feedback_with_meta}"
        response = model.generate_content(prompt)
        
        # Display actionable insights
        st.subheader("Actionable Insights for the Product Team:")
        st.write(response.text)
    
    except Exception as e:
        st.error(f"Error: {e}")

# Display previously collected feedback if needed
if st.button("View Collected Feedback"):
    try:
        feedback_df = pd.read_csv("feedback.csv")
        st.write(feedback_df.tail(10))  # Show last 10 feedbacks
    except Exception as e:
        st.error(f"Error loading feedback data: {e}")
