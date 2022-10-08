'''
import streamlit as st
import pandas as pd

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False






def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""Simple Login App"""

	st.title("Simple Login App")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
				if task == "Add Post":
					st.subheader("Add Your Post")

				elif task == "Analytics":
					st.subheader("Analytics")
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")








if __name__ == '__main__':
	main()
'''
import streamlit as st
import streamlit.components.v1 as stc

# File Processing Pkgs
import pandas as pd
import docx2txt
from PIL import Image 
from PyPDF2 import PdfFileReader
import pdfplumber


def read_pdf(file):
	pdfReader = PdfFileReader(file)
	count = pdfReader.numPages
	all_page_text = ""
	for i in range(count):
		page = pdfReader.getPage(i)
		all_page_text += page.extractText()

	return all_page_text

def read_pdf2(file):
	with pdfplumber.open(file) as pdf:
	    page = pdf.pages[0]
	    return page.extract_text()

# import fitz  # this is pymupdf

# def read_pdf_fitz(file):
# 	with fitz.open(file) as doc:
# 		text = ""
# 		for page in doc:
# 			text += page.getText()
# 		return text 

# Fxn
@st.cache
def load_image(image_file):
	img = Image.open(image_file)
	return img 



def main():
	st.title("File Upload Tutorial")

	menu = ["Home","Dataset","DocumentFiles","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")
		image_file = st.file_uploader("Upload Image",type=['png','jpeg','jpg'])
		if image_file is not None:
		
			# To See Details
			# st.write(type(image_file))
			# st.write(dir(image_file))
			file_details = {"Filename":image_file.name,"FileType":image_file.type,"FileSize":image_file.size}
			st.write(file_details)

			img = load_image(image_file)
			st.image(img,width=250,height=250)


	elif choice == "Dataset":
		st.subheader("Dataset")
		data_file = st.file_uploader("Upload CSV",type=['csv'])
		if st.button("Process"):
			if data_file is not None:
				file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
				st.write(file_details)

				df = pd.read_csv(data_file)
				st.dataframe(df)

	elif choice == "DocumentFiles":
		st.subheader("DocumentFiles")
		docx_file = st.file_uploader("Upload File",type=['txt','docx','pdf'])
		if st.button("Process"):
			if docx_file is not None:
				file_details = {"Filename":docx_file.name,"FileType":docx_file.type,"FileSize":docx_file.size}
				st.write(file_details)
				# Check File Type
				if docx_file.type == "text/plain":
					# raw_text = docx_file.read() # read as bytes
					# st.write(raw_text)
					# st.text(raw_text) # fails
					st.text(str(docx_file.read(),"utf-8")) # empty
					raw_text = str(docx_file.read(),"utf-8") # works with st.text and st.write,used for further processing
					# st.text(raw_text) # Works
					st.write(raw_text) # works
				elif docx_file.type == "application/pdf":
					# raw_text = read_pdf(docx_file)
					# st.write(raw_text)
					try:
						with pdfplumber.open(docx_file) as pdf:
						    page = pdf.pages[0]
						    st.write(page.extract_text())
					except:
						st.write("None")
					    
					
				elif docx_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
				# Use the right file processor ( Docx,Docx2Text,etc)
					raw_text = docx2txt.process(docx_file) # Parse in the uploadFile Class 
					st.write(raw_text)

	else:
		st.subheader("About")
		st.info("Built with Streamlit")
		st.info("Jesus Saves @JCharisTech")
		st.text("Jesse E.Agbe(JCharis)")



if __name__ == '__main__':
	main()
