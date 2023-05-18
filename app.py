import streamlit as st
import pandas as pd
import time
from tempfile import NamedTemporaryFile
import os
from autogpt_accessories import autogpt_process

# Set the temporary directory path
tmp_dir = os.path.join(os.getcwd(), "tmp")

# Check if the directory already exists
if not os.path.exists(tmp_dir):
    # Create the temporary directory
    os.mkdir(tmp_dir)

# Set page configuration
st.set_page_config(
    page_title="Automate your Stuff",
    page_icon="🌟",
    layout="wide"
)

# Define a function to process the CSV file
def process_csv(dataset):
    return f"Dataset processed length: {len(dataset)}"

# Define the main function
def main():
    # Set the title and logo
    st.title("Automate your Stuff")
    st.markdown("<center><h1 style='color: #ffac33;'>🌟</h1></center>", unsafe_allow_html=True)


    def delete_files(directory):
        file_list = os.listdir(directory)
        for file_name in file_list:
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)


    # Display settings
    st.sidebar.subheader("Settings")
    api_key = st.sidebar.text_input("OpenAI API Key", type='password')
    os.environ['OPENAI_API_KEY'] = api_key

    # Assuming 'directory_path' is the path to the directory containing the files

    # Upload CSV file
    st.subheader("Upload CSV File")
    if st.button('Clear history'):
        delete_files(tmp_dir)
        st.success("History cleared successfully!")
    file = st.file_uploader("Choose a CSV file", type=["csv"])

    if file is not None:
        # Display the uploaded file
        with NamedTemporaryFile(dir=tmp_dir, suffix='.csv', delete=False) as temp_file:
            temp_file.write(file.getvalue())
            temp_file_input_path = temp_file.name

        st.subheader("Uploaded CSV file")
        st.write(pd.read_csv(temp_file_input_path))

        # Process the file
        if st.button("Process"):
            df2 = pd.read_csv(temp_file_input_path)
            if not api_key:
                st.warning("Please enter your OpenAI API Key in the settings.")
            else:
                with NamedTemporaryFile(dir=tmp_dir, suffix='.csv', delete=False) as temp_file:
                    temp_file_output_path = temp_file.name

                with st.spinner("Processing..."):
                    result = autogpt_process(temp_file_input_path, temp_file_output_path)

                st.success("Task completed!")
                
                # Create a CSV file from the data
                df = pd.read_csv(temp_file_output_path)
                csv = df.to_csv(index=False)
                # Provide the file name and data to the user for download
                st.download_button("Download Processed File", csv, file_name='processed_file.csv', mime='text/csv')

                # Share on multiple platforms
                st.subheader("Share Processed File")
                # Create columns for better layout
                col1, col2 = st.columns(2)

                with col1:
                    # Email sharing option
                    with st.expander("Email"):
                        email = st.text_input("Recipient's Email")
                        message = st.text_area("Email Message", key="email_message")

                        if st.button("Send Email"):
                            # Implement email sharing functionality
                            if not email:
                                st.warning("Please enter the recipient's email address.")
                            else:
                                # Implement email sending code
                                st.success(f"Email sent to {email} successfully!")

                with col2:
                    # Slack sharing option
                    with st.expander("Slack"):
                        slack_channel = st.text_input("Slack Channel")
                        message = st.text_area("Slack Message", key="slack_message")

                        if st.button("Send to Slack"):
                            # Implement Slack sharing functionality
                            if not slack_channel:
                                st.warning("Please enter the Slack channel.")
                            else:
                                # Implement Slack message sending code
                                st.success(f"Sent to Slack channel {slack_channel} successfully!")

                # Additional sharing options...
                # Add more beta_expanders or columns for additional

# Run the app
if __name__ == "__main__":
    main()
