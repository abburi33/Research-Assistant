import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
import config
from send_mail import send_email

def schedule_meeting():
    """
    Function to schedule a meeting.
    """
    st.subheader("Schedule a Meeting")

    with st.form("meeting_form"):
        # Meeting type selection
        meeting_type = st.selectbox("Meeting Type:", ["Internal", "Client", "Team"])
        
        # Customizing radio button style
        st.markdown("<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
        
        # Meeting description input
        description = st.text_input("Description:")
        
        # Date and time selection
        date = st.date_input("Date:", value=datetime.now())
        time = st.time_input("Time:", value=datetime.now().time())

        # Attendee information input
        attendee_email = st.text_input("Attendee Email:", key="email_input")
        attendee_name = st.text_input("Attendee Name:", key="name_input")

        # Submit button
        submitted = st.form_submit_button("Schedule")

        if submitted:
            # Combine date and time
            date_time = datetime.combine(date, time)
            smtp_server = "smtp.gmail.com"
            smtp_port = 465
            smtp_user = "hermoinegrangerjean79@gmail.com" # Replace with your Gmail email
            smtp_password = "onxt ubyi sbaa kbyt"  # Replace with your App Password
            
            # Send email
            subject = f"Meeting Scheduled: {meeting_type} - {description}"
            message = f"A {meeting_type} meeting is scheduled on {date_time.strftime('%Y-%m-%d %H:%M')} with {attendee_name}."
            send_email(subject, message, attendee_email, smtp_server, smtp_port, smtp_user, smtp_password)
            st.success("Meeting scheduled successfully!")

def main():
    """
    Main function to run the Research Assistant app.
    """
    # Streamlit webpage layout
    st.set_page_config(layout="wide")

    # Header and content
    st.header("Your Research Assistant!")
    
    schedule_meeting()

if __name__ == "__main__":
    main()
