import string
import joblib
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import time

def remove_punc(text):
    exclude = string.punctuation
    if not isinstance(text, str):
        text = str(text)
    return text.translate(str.maketrans('','',exclude))

ps = PorterStemmer()              
def stemming(text):
    if not isinstance(text, str):
        text = str(text)
    return " ".join(ps.stem(word) for word in text.split())

def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = remove_punc(text)
    text = stemming(text)
    return text.strip()


def predict_genre(new_texts):
    model = joblib.load("best_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")

    if isinstance(new_texts, str):
        new_texts = [new_texts]

    cleaned = [clean_text(text) for text in new_texts]
    features = vectorizer.transform(cleaned)
    predictions = model.predict(features)

    return predictions

file_messages = '/home/aditya-aman/All Repository/University-Complaint-Helper/messages01.log'
file_messages2= '/home/aditya-aman/All Repository/University-Complaint-Helper/messages2.log'

# If this get used for large scale, the time recored will be used to connect the user account. this "[] Processing Message : " will be used send the line to the previous defined user by time Z.
# NOTE : Use \n[] Processing Message :  insted of \n to coonect correctly 
complaint_resolution = {
    "['CIVIL']": "We are sorry that you are facing such issue, please follow the following steps to resolve your problem at the earliest.\n[] Processing message: Step-1 :- Follow the following link to the official complaint page of VIT: https://snm.vitbhopal.dev/client/login\n[] Processing message: Step-2 :- Login through your VIT Mail ID.\n[] Processing message: Step-3 :- Navigate to the \"Submit a Ticket\" column via the Sidebar or Top-bar.\n[] Processing message: Step-4 :- Select options like your block, category (As mentioned above), subcategory and describe your problem in the Description.\n[] Processing message: Step-5 :- Submit the created Ticket to initiate the procedure for a Solution\n[] Processing message: You can also Contact the following if your problem is still not resolved :-\n[] Processing message: 1. Chief Warden Boys <cw@vitbhopal.ac.in>\n[] Processing message: 2. Chief Warden Ladies <cw.lh@vitbhopal.ac.in>",

    "['Electrical']": "We are sorry that you are facing such issue, please follow the following steps to resolve your problem at the earliest.\n[] Processing message: Step-1 :- Follow the following link to the official complaint page of VIT: https://snm.vitbhopal.dev/client/login\n[] Processing message: Step-2 :- Login through your VIT Mail ID.\n[] Processing message: Step-3 :- Navigate to the \"Submit a Ticket\" column via the Sidebar or Top-bar.\n[] Processing message: Step-4 :- Select options like your block, category (As mentioned above), subcategory and describe your problem in the Description.\n[] Processing message: Step-5 :- Submit the created Ticket to initiate the procedure for a Solution\n[] Processing message: You can also Contact the following if your problem is still not resolved :-\n[] Processing message: 1. Chief Warden Boys <cw@vitbhopal.ac.in>\n[] Processing message: 2. Chief Warden Ladies <cw.lh@vitbhopal.ac.in>",

    "['Lift']": "We are sorry that you are facing such issue, please follow the following steps to resolve your problem at the earliest.\n[] Processing message: Step-1 :- Follow the following link to the official complaint page of VIT: https://snm.vitbhopal.dev/client/login\n[] Processing message: Step-2 :- Login through your VIT Mail ID.\n[] Processing message: Step-3 :- Navigate to the \"Submit a Ticket\" column via the Sidebar or Top-bar.\n[] Processing message: Step-4 :- Select options like your block, category (As mentioned above), subcategory and describe your problem in the Description.\n[] Processing message: Step-5 :- Submit the created Ticket to initiate the procedure for a Solution\n[] Processing message: You can also Contact the following if your problem is still not resolved :-\n[] Processing message: 1. Chief Warden Boys <cw@vitbhopal.ac.in>\n[] Processing message: 2. Chief Warden Ladies <cw.lh@vitbhopal.ac.in>",

    "['Airconditioning']": "We are sorry that you are facing such issue, please follow the following steps to resolve your problem at the earliest.\n[] Processing message: Step-1 :- Follow the following link to the official complaint page of VIT: https://snm.vitbhopal.dev/client/login\n[] Processing message: Step-2 :- Login through your VIT Mail ID.\n[] Processing message: Step-3 :- Navigate to the \"Submit a Ticket\" column via the Sidebar or Top-bar.\n[] Processing message: Step-4 :- Select options like your block, category (As mentioned above), subcategory and describe your problem in the Description.\n[] Processing message: Step-5 :- Submit the created Ticket to initiate the procedure for a Solution\n[] Processing message: You can also Contact the following if your problem is still not resolved :-\n[] Processing message: 1. Chief Warden Boys <cw@vitbhopal.ac.in>\n[] Processing message: 2. Chief Warden Ladies <cw.lh@vitbhopal.ac.in>",

    "['Plumbing']": "We are sorry that you are facing such issue, please follow the following steps to resolve your problem at the earliest.\n[] Processing message: Step-1 :- Follow the following link to the official complaint page of VIT: https://snm.vitbhopal.dev/client/login\n[] Processing message: Step-2 :- Login through your VIT Mail ID.\n[] Processing message: Step-3 :- Navigate to the \"Submit a Ticket\" column via the Sidebar or Top-bar.\n[] Processing message: Step-4 :- Select options like your block, category (As mentioned above), subcategory and describe your problem in the Description.\n[] Processing message: Step-5 :- Submit the created Ticket to initiate the procedure for a Solution\n[] Processing message: You can also Contact the following if your problem is still not resolved :-\n[] Processing message: 1. Chief Warden Boys <cw@vitbhopal.ac.in>\n[] Processing message: 2. Chief Warden Ladies <cw.lh@vitbhopal.ac.in>",

    "['Water Geyser ']": "We are sorry that you are facing such issue, please follow the following steps to resolve your problem at the earliest.\n[] Processing message: Step-1 :- Follow the following link to the official complaint page of VIT: https://snm.vitbhopal.dev/client/login\n[] Processing message: Step-2 :- Login through your VIT Mail ID.\n[] Processing message: Step-3 :- Navigate to the \"Submit a Ticket\" column via the Sidebar or Top-bar.\n[] Processing message: Step-4 :- Select options like your block, category (As mentioned above), subcategory and describe your problem in the Description.\n[] Processing message: Step-5 :- Submit the created Ticket to initiate the procedure for a Solution\n[] Processing message: You can also Contact the following if your problem is still not resolved :-\n[] Processing message: 1. Chief Warden Boys <cw@vitbhopal.ac.in>\n[] Processing message: 2. Chief Warden Ladies <cw.lh@vitbhopal.ac.in>",

    "['Water Cooler ']": "We are sorry that you are facing such issue, please follow the following steps to resolve your problem at the earliest.\n[] Processing message: Step-1 :- Follow the following link to the official complaint page of VIT: https://snm.vitbhopal.dev/client/login\n[] Processing message: Step-2 :- Login through your VIT Mail ID.\n[] Processing message: Step-3 :- Navigate to the \"Submit a Ticket\" column via the Sidebar or Top-bar.\n[] Processing message: Step-4 :- Select options like your block, category (As mentioned above), subcategory and describe your problem in the Description.\n[] Processing message: Step-5 :- Submit the created Ticket to initiate the procedure for a Solution\n[] Processing message: You can also Contact the following if your problem is still not resolved :-\n[] Processing message: 1. Chief Warden Boys <cw@vitbhopal.ac.in>\n[] Processing message: 2. Chief Warden Ladies <cw.lh@vitbhopal.ac.in>",

    "['Carpentry']": "We are sorry that you are facing such issue, please follow the following steps to resolve your problem at the earliest.\n[] Processing message: Step-1 :- Follow the following link to the official complaint page of VIT: https://snm.vitbhopal.dev/client/login\n[] Processing message: Step-2 :- Login through your VIT Mail ID.\n[] Processing message: Step-3 :- Navigate to the \"Submit a Ticket\" column via the Sidebar or Top-bar.\n[] Processing message: Step-4 :- Select options like your block, category (As mentioned above), subcategory and describe your problem in the Description.\n[] Processing message: Step-5 :- Submit the created Ticket to initiate the procedure for a Solution\n[] Processing message: You can also Contact the following if your problem is still not resolved :-\n[] Processing message: 1. Chief Warden Boys <cw@vitbhopal.ac.in>\n[] Processing message: 2. Chief Warden Ladies <cw.lh@vitbhopal.ac.in>",

    "['House Keeping']": "We are sorry that you are facing such issue, please follow the following steps to resolve your problem at the earliest.\n[] Processing message: Step-1 :- Follow the following link to the official complaint page of VIT: https://snm.vitbhopal.dev/client/login\n[] Processing message: Step-2 :- Login through your VIT Mail ID.\n[] Processing message: Step-3 :- Navigate to the \"Submit a Ticket\" column via the Sidebar or Top-bar.\n[] Processing message: Step-4 :- Select options like your block, category (As mentioned above), subcategory and describe your problem in the Description.\n[] Processing message: Step-5 :- Submit the created Ticket to initiate the procedure for a Solution\n[] Processing message: You can also Contact the following if your problem is still not resolved :-\n[] Processing message: 1. Chief Warden Boys <cw@vitbhopal.ac.in>\n[] Processing message: 2. Chief Warden Ladies <cw.lh@vitbhopal.ac.in>",

    "['Mess']": "We are sorry that you are facing such issue, please follow the following steps to resolve your problem at the earliest.\n[] Processing message: Step-1 :- Follow the following link to the official complaint page of VIT: https://snm.vitbhopal.dev/client/login\n[] Processing message: Step-2 :- Login through your VIT Mail ID.\n[] Processing message: Step-3 :- Navigate to the \"Submit a Ticket\" column via the Sidebar or Top-bar.\n[] Processing message: Step-4 :- Select options like your block, category (As mentioned above), subcategory and describe your problem in the Description.\n[] Processing message: Step-5 :- Submit the created Ticket to initiate the procedure for a Solution\n[] Processing message: You can also Contact the following if your problem is still not resolved :-\n[] Processing message: 1. Chief Warden Boys <cw@vitbhopal.ac.in>\n[] Processing message: 2. Chief Warden Ladies <cw.lh@vitbhopal.ac.in>",

    "['CTS']": "We are Sorry to know about this technical issue, if this issue does not get resolved soon, please try the following:-\n[] Processing message: 1. Please register your complain-ticket on the VIT-complaint site at the earliest: https://snm.vitbhopal.dev/client/login\n[] Processing message: 2. Try conveying your issue to CTS office via Mail <ad.cts@vitbhopal.ac.in>\n[] Processing message: 3. Reach out to the CTS office located in AB-01 in Room No. 212",

    "['COE']": "We are sorry to hear about your issue, please find the contact details of the concerned department below:-\n[] Processing message: 1. COE office <coe@vitbhopal.ac.in>\n[] Processing message: 2. Exam Cell coordinators <ecc2@vitbhopal.ac.in>, <ecc3@vitbhopal.ac.in>\n[] Processing message: 3. Deputy COE <dycoe@vitbhopal.ac.in>\n[] Processing message: 4. Dr G Prabukanna <prabukanna.g@vitbhopal.ac.in>\nIf your issue is still unresolved, reach out to the COE office located in AB-01 in Room No. 124",

    "['DSW']": "We are sorry to see your issue, be assured that no in-disciplinary act will go unchecked. You are requested to reach out to the authorities as soon as possible. Below, you can find the contact details of the same:-\n[] Processing message: 1. Director Student Welfare <dsw@vitbhopal.ac.in>\n[] Processing message: 2. Chief Warden Boys <cw@vitbhopal.ac.in>\n[] Processing message: 3. Chief Warden Ladies <cw.lh@vitbhopal.ac.in>\n[] Processing message: 4. Pro Vice Chancellor <provc@vitbhopal.ac.in>\nIf your issue is still unresolved, reach out to the DSW office located in AB-01",

    "['Academics']": "We are sorry to hear about your issue, please find the contact details of the concerned department below:-\n[] Processing message: 1. Dean Faculty Affairs <dfa@vitbhopal.ac.in>\n[] Processing message: 2. Academic Coordinator <ac@vitbhopal.ac.in>\n[] Processing message: 3. Assis. Dean 1st year <ad.fy@vitbhopal.ac.in>\n[] Processing message: 4. Assis. Director Proctor <ad.proctor@vitbhopal.ac.in>\n[] Processing message: 5. Assis. Dean Academics <asstdean.acad@vitbhopal.ac.in>\n[] Processing message: 6. Dean Research <dean.research@vitbhopal.ac.in>\nIf your issue is still unresolved, reach out to your Proctor or Program Chair.",

    "['FFCS']": "We are sorry to hear about your issue, please find the contact details of the concerned department below:-\n[] Processing message: 1. FFCS coordinator <ffcs.timetable@vitbhopal.ac.in>\n[] Processing message: 2. Academic coordinator <ac@vitbhopal.ac.in>\n[] Processing message: 3. PC <allpc@vitbhopal.ac.in>\nIf your issue isn’t resolved please reach out to your Course Coordinator/Dean or Program-Chair as soon as possible."
}

while True:
    with open(file_messages, 'r') as input_file:
        pre_content = input_file.read()
        user_time = pre_content[0:26]
        content = pre_content[55:]
    
    if pre_content:

        post_content= str(predict_genre(content))

        final_content = complaint_resolution[post_content]

        with open(file_messages2, 'w') as output_file:
            output_file.write(user_time + " Processing message: "+ final_content) #Client side : It will give the solution
        with open(file_messages, 'w') as input_file:
            input_file.write('')
        print(user_time + " Processing message: "+ post_content) #Server side : it will show the category 
        
    time.sleep(1)