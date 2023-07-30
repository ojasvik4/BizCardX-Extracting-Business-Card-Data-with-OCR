Business-Card-Data
Project Title : Extracting Business Card Data with OCR

Technologies : OCR,streamlit GUI, SQL,Data Extraction

Domain : Business

Problem Statement: Develop a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR. The extracted information should include the company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code. The extracted information should then be displayed in the application's graphical user interface (GUI)

Steps involved in the project:

Dashboard creation: Created an intuitive user interface using Streamlit that guides users through the process of uploading the business card image and extracting its information. Used the widgets like file uploader, buttons, and text boxes to make the interface more interactive

Data Extraction: Used easyOCR to extract the relevant information from the uploaded business card image

Display the extracted information: After extracting the information, it is displayed in a clean and organized manner in the Streamlit GUI using tables widget

Implement database integration: Used PostgreSQL database to store the extracted information. SQL queries can be made to insert, update, delete and retrieve data from the database from the GUI

Test the application: Tested the application thoroughly to ensure that it works as expected. Used try except block to handle exceptions

The code is written in python , database used is PostgreSQL and UI is developed using streamlit

Packages used in the project: Pandas, Streamlit, Psycopg, Sqlalchemy, EasyOCR
