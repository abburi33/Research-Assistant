import streamlit as st
import speech_recognition as sr
import pyttsx3 

# Initialize the recognizer 
r = sr.Recognizer() 

# Function to convert text to speech
def speak_text(command):
    """
    Function to convert text to speech and speak it aloud.

    Args:
    - command (str): The text to be converted to speech.
    """
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def app():
    """
    Main function to run the Speech to Text and Text to Speech Converter app.
    """
    st.title("SPEECH TO TEXT AND TEXT TO SPEECH CONVERTER")

    # Sidebar for selecting the conversion option
    option = st.sidebar.selectbox("Select conversion option:", ("Speech to Text", "Text to Speech"))

    if option == "Speech to Text":
        st.header("Speech to Text Conversion")
        st.info("""
            This feature allows you to convert speech to text. Click the "Start Recording" button to begin recording your speech. 
            Once you're done speaking, click the "Stop Recording" button to stop recording and see the converted text.
        """)

        recording = False
        text = ""

        # Create a row layout to place buttons side by side
        col1, col2 = st.columns([1, 1])

        # Button to start recording
        if not recording:
            if col1.button("Start Recording"):
                recording = True

        # Button to stop recording
        if recording:
            if col2.button("Stop Recording"):
                recording = False
                st.write("Recording stopped.")

            st.write("Recording...")

            try:
                # use the microphone as source for input
                with sr.Microphone() as source:
                    # wait for a second to let the recognizer
                    # adjust the energy threshold based on
                    # the surrounding noise level 
                    r.adjust_for_ambient_noise(source, duration=0.2)

                    # Continuous loop for recording until "Stop Recording" button is clicked
                    while recording:
                        # listens for the user's input 
                        audio = r.listen(source)

                        # Using Google to recognize audio
                        text = r.recognize_google(audio)
                        text = text.lower()

                        st.write("You said:", text)
                        speak_text(text)

            except sr.RequestError as e:
                st.error(f"Could not request results: {e}")

            except sr.UnknownValueError:
                st.error("Unknown error occurred")

        if not recording and text:
            st.subheader("Converted Text")
            st.info(text)
    
    elif option == "Text to Speech":
        st.header("Text to Speech Conversion")
        st.info("""
            This feature allows you to convert text to speech. 
            Enter the desired text in the input box below and click the "Convert to Speech" button to hear the text spoken aloud.
        """)
        
        # Input box for user to enter text
        text_input = st.text_area("Enter text here:")

        # Button to convert text to speech
        if st.button("Convert to Speech"):
            speak_text(text_input)

if __name__ == "__main__":
    app()
