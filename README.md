# A Web Government Application - All your documents and services in one place

## Intro
  Welcome to the Web Government Application, an application, where you can access all documents and services in one place.
  This repository serves as a central hub for the collaborative efforts of our team in designing and implementing this application.

## Repository Contents
  This repository contains various resources and code related to our Web Government Application. 
  Here's a brief overview of what you can find here:
  - Project Source Code: The heart of our project. The source code for the logic and user interfaces of our application.
  - Testing and Validation: Test scripts, testing data, and all the validation procedures we used to ensure the reliability and performance of our application.
  - Issues: The record of all the issues we raised and encountered while working on this project, our discussions and comments. Feel free to open an issue if you have any questions or suggestions.
  - Wikis and ReadMes: The place to go for an elaborate description of our application, its' modules and all the details. This ReadMe is one of the files you may want to read through to get a feel of what we are trying to accomplish here.

## Team Members
  - Abdelrahman Hashad
  - Ali Noureddine
  - Artem Maksymov
  - Mostafa Elbasiouny

## Objective and System Requirements
  Our primary goal is to develop a web application, which would allow you to comfortably access your documents and governmental services at any given time, from any device with access to Internet. In this context, we aim to:
  - Provide a solution with a secure log on and registration features, to allow users use their username and password, as well as banking application to connect to their account.
  - Pull personal user data either from user registration prompts or from the banking registration data.
  - Provide users with the list of their private documents and allow them to add custom documents and safely store them.
  - Allow users access various governmental services including, but not limited to: paying fines, paying off tickets, filing taxes, requesting criminal or background records, etc.

## Getting Started
  To get a feel of our application, please feel free to download the latest release by navigating to the releases tab and selecting the freshest version.
  Once you have the freshest release installed you will need to containerize it and run exposing a port.

  Please remember, that when running the application as a containerized one on your machine, you will only get access to the data in the local database, not to real-life data.

  Please follow the following steps to install and setup our module on your workstation.
  - [ ] Step 1. Cloning the repository on your workstation.
  ```
  git clone https://github.com/armaksymov/web_government.git
  ```

  - [ ] Step 2. Make sure you have up-to-date python installed on your workstation (Should be > 3.10).
  ```
  python --version
  ```

  - [ ] Step 3. Install all the required packages for our project.
  ```
  pip install -r requirements.txt
  ```

  - [ ] Step 4. Running the application.
  ```
  python run.py
  ```

## Contact Us
  Should you have any questions, suggestions, or encounter any issues while working with our application, please don't hesitate to raise an issue stating your question or feel free to reach out to any of our team members listed above.
  We are committed to develop as the best version of itself and value your input.

## Thank you for your interest in our project and for reading this file!
