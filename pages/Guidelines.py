import streamlit as st

def display_guidelines():
    """
    Function to display guidelines and regulations links.
    """
    st.subheader("Guidelines and Regulations")
    st.markdown("[NIH Guide for the Care and Use of Laboratory Animals](https://olaw.nih.gov/guide-for-the-care-and-use-of-laboratory-animals)")
    st.markdown("[IACUC Guidelines and Policies](https://www.iacuc.org/guidelines/index.html)")
    st.markdown("[NC3Rs Guidelines and Resources](https://www.nc3rs.org.uk/resources)")

# Define the Experiment Design Assistance function
def experiment_design_assistance():
    """
    Function to assist with experiment design.
    """
    st.subheader("Experiment Design Assistance")

    # Dropdown menu to select template
    template_option = st.selectbox("Select Template Design:", ("Template Design 1",))

    # Display selected template form fields
    if template_option == "Template Design 1":
        display_template_design_1()

# Define the form fields for Template Design 1
def display_template_design_1():
    """
    Function to display form fields for Template Design 1.
    """
    st.markdown("### Template Design 1")
    objective = st.text_area("Objective")
    hypothesis = st.text_area("Hypothesis")
    experimental_design = st.text_area("Experimental Design")
    subjects = st.text_area("Subjects")
    experimental_procedures = st.text_area("Experimental Procedures")
    data_analysis = st.text_area("Data Analysis")
    ethical_considerations = st.text_area("Ethical Considerations")
    references = st.text_area("References")

# Define the main function
def main():
    """
    Main function to run the Experiment Design Assistance App.
    """
    st.title("Experiment Design Assistance App")

    display_guidelines()

    # Display experiment design assistance section
    experiment_design_assistance()

if __name__ == "__main__":
    main()
