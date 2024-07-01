# MAF Assistant
MAF Assistant is a Python application designed to automate PubMed searches. 

## Overview
The application enables users to perform searches against the PubMed database and automatically select the most relevant articles based on user-defined criteria. Additionally, searches can be stored in a database for future reference.

## Features
The application is built with Streamlit and includes the following interfaces:

### Presentation Page
User Authentication: Users are prompted to enter a unique username, which is used to manage individual user information.  
  
![image](https://github.com/JoseCouceiro/MAF_Assistant/assets/118387556/e87dd300-9b49-4990-a269-dd7ab27c40ab)
  
### Main Page
The main page consists of four tabs:

#### Search Tab:

**Functionality**: Perform searches on PubMed.  
**Options**: Specify the start and end dates for the search. Optionally, save the search by checking a checkbox.  
  
![image](https://github.com/JoseCouceiro/MAF_Assistant/assets/118387556/c4e1fdae-c092-47db-8b59-8046b0e3b695)
  
#### Search Terms Tab:

**Functionality**: Add or remove search terms to be used in the searches.  

![image](https://github.com/JoseCouceiro/MAF_Assistant/assets/118387556/8a9f1108-b02f-4aec-9028-745658673256)
  
#### Classification Parameters Tab:

**Functionality**: Set the weight of various classification parameters used to select the most relevant articles. The weights can have either a positive or negative value.  

![image](https://github.com/JoseCouceiro/MAF_Assistant/assets/118387556/23325f04-beb8-4c6e-a649-960112b78b0b)

#### Results Archive Tab:

**Functionality**: View saved searches. Clicking on a specific search displays the articles selected for that search.  
**Options**: Searches can be deleted by using the 'Delete' checkbox.  

![image](https://github.com/JoseCouceiro/MAF_Assistant/assets/118387556/63e6ffb9-22f6-41c0-a74c-ca8f9cce12e4)

## How to Run
### Mount the Environment
A requirements file for a conda environment can be found at "\journalrater\requirements.txt".

Create a new conda environment with the command:

```bash
conda create --name <YOUR_ENV> python==<YOUR_VERSION>
```

Run the following command from inside the project's main folder:

```bash
~\anaconda3\envs\<YOUR_ENV>\python.exe -m pip install -r src/requirements.txt
```

### Run the App
To run the application, use the command:

```bash
streamlit run drug_predictor.py
```






