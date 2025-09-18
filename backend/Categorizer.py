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
while True:
    with open(file_messages, 'r') as input_file:
        pre_content = input_file.read()
        user_time = pre_content[0:26]
        content = pre_content[55:]
    
    if pre_content:

        post_content= str(predict_genre(content))


    




    with open(file_messages2, 'w') as output_file:
        output_file.write(user_time + " Processing message: "+ post_content) #Client side : It will give the solution
    with open(file_messages, 'w') as input_file:
        input_file.write('')
    print(user_time + " Processing message: "+ post_content) #Server side : it will show the category 
    
    time.sleep(1)