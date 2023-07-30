import streamlit as st
import re
import pandas as pd
import numpy as np
import psycopg2
import easyocr
import cv2
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu
from PIL import Image
import warnings
warnings.filterwarnings("ignore")

def extract(uploaded_file):
    reader=easyocr.Reader(lang_list=['en'],gpu=False)
    if uploaded_file is not None:
        img = cv2.imdecode(np.fromstring(uploaded_file.read(),np.uint8),1)
        result_1 = reader.readtext(img,detail=0,paragraph=True)
        result_2 = reader.readtext(img,detail=0,paragraph=False)
        name = result_2[0]
        des = result_2[1]
        mob = []
        for i in result_2:
            if re.findall(r'\d+-\d+-\d+',i):
                mob.append(i)
        for i in result_2:
            if re.findall(r'[a-zA-Z]+@[a-zA-Z0-9]+.[a-zA-Z]+',i):
                mail = i
                break
            else:
                mail = 'Not found'
        for i in result_2:
            if re.findall(r'[wW]+.[a-zA-Z0-9]+.[a-zA-Z]+',i): 
                web = i
                break
            else:
                web = 'Not found' 
        for i in result_1:
            if len(i) > 30:
                add = i
        org = result_1[-1]
        if len(mob) == 1:
            mob1=mob[0]
            mob2 = 'Not Available'
        elif len(mob) == 2:
            mob1 = mob[0]
            mob2 = mob[1]
    
       
        info = {'name':name, 'designation':des,'primary_contact':mob1,'secondary_contact':mob2,'webpage':web,'email_id':mail,
                'address':add,'organization':org}
        res= pd.DataFrame(info,index=['Details'])
        res['name'] = res['name'].str.title()
        res['designation'] = res['designation'].str.title()
        res['organization'] = res['organization'].str.title()
        return res

def push_data(df):
    engine = create_engine('postgresql://postgres:Postgres123$@localhost:5432/business_card')
    df.to_sql('b_card', engine, if_exists='append', index=False)
    st.success('Business card information successfully pushed to PostgreSQL Database', icon="✅")

def modify():
    st.subheader(':orange[ ⏪ Use this section to update an already existing detail in PostgreSQL database ⏩]')
    st.write('')
    engine = create_engine('postgresql://postgres:Postgres123$@localhost:5432/business_card')
    st.write('')
    st.write('')
    st.markdown(':orange[Please select the name of the individual from the dropdown whose details you want to edit]')
    st.write('')
    st.write('')
    names = pd.read_sql_query('SELECT name from b_card', engine)
    names.sort_values(by='name', ascending = True, inplace = True)
    list1 = list(names['name'])
    option = st.selectbox('Make your choice.....',(list1))
    st.write('')
    st.write('')
    if st.button('Fetch the details....',key=2):
        st.write('')
        st.write('')
        df = pd.read_sql_query(f'SELECT * from b_card where name=\'{option}\'', engine)
        st.table(data=df)
    st.markdown(':red[Please select the field you wish to edit]')
    st.write('')
    st.write('')
    df = pd.read_sql_query(f'SELECT * from b_card where name=\'{option}\'', engine)
    list2 = list(df.columns)
    col6, col7 = st.columns([5,10])
    with col6:
        option2 = st.selectbox('Make your choice.....',(list2))  
    with col7:    
        new_value = st.text_input('Current value is displayed here 👇', df[f'{option2}'][0])
        st.write("")
        st.write("")
        st.write("")
    if st.button('🟢 Update the field value in PostgreSQL database 🟢',key=3):
        conn = psycopg2.connect(
        host="localhost",
        database="business_card",
        user="postgres",
        password="Postgres123$")
        cursor = conn.cursor()
        query = f'UPDATE b_card set {option2} = \'{new_value}\' where name=\'{option}\''
        cursor.execute(query)
        conn.commit()
        st.markdown(':orange[ Displaying the data after the changes....]')
        df = pd.read_sql_query(f'SELECT * from b_card where name=\'{option}\'', engine)
        st.table(data=df)
    st.write('')
    st.subheader(':red[⏪ Use this section to delete an already existing detail in PostgreSQL database ⏩]')
    st.write('')
    names = pd.read_sql_query('SELECT name from b_card', engine)
    names.sort_values(by='name', ascending = True, inplace = True)
    list1 = list(names['name'])
    option3 = st.selectbox('Make your choice.....',(list1),key=5)
    st.write('')
    st.write('')
    if st.button('🚨 Delete the details of the individual from PostgreSQL database 🚨',key=4):
        conn = psycopg2.connect(
        host="localhost",
        database="business_card",
        user="postgres",
        password="Postgres123$")
        cursor = conn.cursor()
        query = f'DELETE from b_card  where name=\'{option3}\''
        cursor.execute(query)
        conn.commit()
        st.markdown(':orange[ Displaying the data after deletion....]')
        df = pd.read_sql_query(f'SELECT * from b_card', engine)
        df.sort_values(by='name', ascending = True, inplace = True)
        df.reset_index(drop=True)
        st.table(data=df)    

def download():
    col9,col10,col11 = st.columns([5,30,5])
    with col10:
        st.subheader(':green[ ⏬ Use this section to download data from PostgreSQL database ⏬]')
        st.write('')
        engine = create_engine('postgresql://postgres:Postgres123$@localhost:5432/business_card')
        df = pd.read_sql_query(f'SELECT * from b_card', engine)
        df.sort_values(by='name', ascending = True, inplace = True)
        df.reset_index(drop=True)
        return df  

if __name__ =='__main__':
    st.set_page_config(layout="wide")
    col1, col2, col3 = st.columns([1,8,1])
    with col2:
        st.title(':blue[Extracting Business Card Data with OCR]')
    st.write('')
    st.write('')
    selected = option_menu(None, ["Home","Extract & upload",  "Modify", "Download"], 
    icons=['house', "database-fill-add", "gear", 'database-fill-down'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    if selected == 'Home':
        st.subheader(":orange[🔖 **About the project** ]")
        st.write('')
        st.write('')
        st.markdown('<div style="text-align: justify"> A business card is a small printed card that typically contains an individual\'s or a company\'s contact information, such as name, job title, address, phone number, email address, and website. It serves as a tangible representation of professional identity and acts as a convenient networking tool. </div>', unsafe_allow_html=True)
        st.write('')
        st.markdown('<div style="text-align: justify"> The significance of a business card lies in its ability to make a lasting impression and facilitate effective communication in the business world. It provides a concise summary of vital information, enabling individuals to easily share their details with others. When exchanging business cards, it creates a personal connection and serves as a physical reminder of a meeting or interaction. Business cards are versatile marketing tools. They can be distributed at networking events, conferences, or during chance encounters, allowing individuals to expand their professional network and generate potential business opportunities. Furthermore, a unique and visually appealing design can make a business card stand out, increasing the chances of being remembered and contacted in the future. </div>', unsafe_allow_html=True)
        st.write('')
        st.markdown('<div style="text-align: justify"> OCR stands for Optical Character Recognition. It is a technology that enables the conversion of printed or handwritten text into digital form by scanning and analyzing images or documents. The significance of OCR lies in its ability to automate and streamline various processes that involve the extraction and interpretation of textual information. </div>', unsafe_allow_html=True)
        st.write('')
        st.markdown('<div style="text-align: justify"> EasyOCR is an open-source Python library that provides a simple yet powerful Optical Character Recognition (OCR) solution. It allows developers to extract text from images or scanned documents effortlessly. EasyOCR supports more than 80 languages, making it a versatile tool for various applications and industries. One of the key advantages of EasyOCR is its ease of use. It offers a straightforward API, enabling developers to integrate OCR functionality into their applications with minimal coding effort. The library handles the complexities of text recognition, including text localization, character segmentation, and recognition, simplifying the overall development process. </div>', unsafe_allow_html=True)
        st.write('')
        st.markdown('<div style="text-align: justify"> Objective of this project is to leverage the abilities of EasyOCR to extract the information from business card, store it in a database for future retreival and usage. Hence, avoiding manual data entry.   </div>', unsafe_allow_html=True)
        st.write('')
        st.divider()    
        st.subheader(':orange[📝 About the developer ]')
        st.write('')
        st.markdown('<div style="text-align: justify">Gururaj H C is passionate about Machine Learning and fascinated by its myriad real world applications. Possesses work experience with both IT industry and academia. Currently pursuing “IIT-Madras Certified Advanced Programmer with Data Science Mastery Program” course as a part of his learning journey.  </div>', unsafe_allow_html=True)
        st.divider()
        col1001, col1002, col1003 = st.columns([10,10,10])
        with col1002:
            st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Agdasima');
                    .custom-text { font-family: 'Agdasima', sans-serif; font-size: 28px;color:red }
                    </style>
                    <p class="custom-text">An Effort by : MAVERICK_GR</p>
                    """, unsafe_allow_html=True)
            st.markdown(':green[**DEVELOPER CONTACT DETAILS**]')
        col2001, col2002 = st.columns([10,10])
        with col2001:
            st.markdown(":orange[email id:] gururaj008@gmail.com")
            st.markdown(":orange[Personal webpage hosting other Datascience projects: ]") 
            st.markdown(':green[https://gururaj008-personal-webpage.streamlit.app/]')
            st.markdown(':green[http://gururaj008.pythonanywhere.com/]') 
        with col2002:
            st.markdown(":orange[LinkedIn profile :] https://www.linkedin.com/in/gururaj-hc-machine-learning-enthusiast/")
            st.markdown(":orange[Github link:] https://github.com/Gururaj008 ")

    if selected == 'Extract & upload':
        st.subheader(':green[ ⏫ Use this section to extract data from the business card and push it to PostgreSQL ⏫]')
        st.write('')
        uploaded_file = st.file_uploader("Upload the business card here...\n", type=['png', 'jpeg', 'jpg'])
        col4, col5 = st.columns([10,10])
        with col4:
            if st.button('⏳ Read the card and push the data to PostgreSQL database ⏳',key=1):
                try:
                    st.warning('Extracting the information.....', icon="⏫")
                    df = extract(uploaded_file)
                    st.table(data=df.T)
                    push_data(df)
                    with col5:
                        st.write('')
                        st.write('')
                        st.write('')
                        st.write('')
                        st.write('')
                        st.write('')
                        st.write('')
                        image = Image.open(uploaded_file)
                        st.image(image,use_column_width='always')
                except:
                    st.error('Upload an image first...', icon="🚨")
        st.divider()
        col1001, col1002, col1003,col1004, col1005 = st.columns([10,10,10,10,15])
        with col1005:
            st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Agdasima');
                    .custom-text { font-family: 'Agdasima', sans-serif; font-size: 28px;color:cyan }
                    </style>
                    <p class="custom-text">An Effort by : MAVERICK_GR</p>
                    """, unsafe_allow_html=True)
            
        
    if selected == 'Modify':
        modify()
        st.divider()
        col1001, col1002, col1003,col1004, col1005 = st.columns([10,10,10,10,15])
        with col1005:
            st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Agdasima');
                    .custom-text { font-family: 'Agdasima', sans-serif; font-size: 28px;color:lime }
                    </style>
                    <p class="custom-text">An Effort by : MAVERICK_GR</p>
                    """, unsafe_allow_html=True)

    if selected == 'Download':
        down1 = download()
        down1.reset_index(drop=True,inplace=True)
        st.table(down1)
        csv_2 = down1.to_csv()
        col6, col7, col8 = st.columns([10,6,10])
        with col7:
            st.write('')
            st.download_button(label="🔻 Download data as CSV 🔻",data=csv_2,
                            file_name='business_card_info.csv',mime='text/csv')
        st.divider()
        col1001, col1002, col1003,col1004, col1005 = st.columns([10,10,10,10,15])
        with col1005:
            st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Agdasima');
                    .custom-text { font-family: 'Agdasima', sans-serif; font-size: 28px;color:gold }
                    </style>
                    <p class="custom-text">An Effort by : MAVERICK_GR</p>
                    """, unsafe_allow_html=True)


