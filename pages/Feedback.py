import streamlit as st
from send_mail import send_email

def contact_us():
    st.header("Contact Us")

    with st.form(key="company_form"):
        user_email = st.text_input("Your Email Address", 'yourmail@gmail.com')
        topic = st.selectbox(
            "What topic do you want to discuss?",
            ("Meeting Feature Feedback", "Bugs in the Application", "Suggestions", "Other Queries")
        )
        text = st.text_area("Text")
        submit_button = st.form_submit_button("Submit")
        message = f"""\
    From: {user_email}
    topic: {topic}
    message: {text}
    """

    if submit_button:
        subject = "Message from Research Assistant Contact Form"
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        smtp_user = "hermoinegrangerjean79@gmail.com"  # Replace with your Gmail email
        smtp_password = "onxt ubyi sbaa kbyt"  # Replace with your App Password

        send_email(subject, message, user_email, smtp_server, smtp_port, smtp_user, smtp_password)
        st.success('Message sent successfully!')

# To run the contact_us function
if __name__ == "__main__":
    contact_us()
