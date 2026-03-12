# import pandas as pd
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# import joblib
# import re
# from nltk.tokenize import word_tokenize

# # Fallback stopwords
# FALLBACK_STOPWORDS = {
#     'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
#     'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
#     'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
#     'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
#     'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
#     'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
#     'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
#     'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
#     'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
#     'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
#     'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
#     'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
#     'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
#     'will', 'just', 'don', 'should', 'now'
# }

# def preprocess_text(text):
#     try:
#         text = text.lower()
#         text = re.sub(r'[^\w\s]', '', text)
#         tokens = word_tokenize(text)
#         stop_words = FALLBACK_STOPWORDS
#         tokens = [word for word in tokens if word not in stop_words]
#         return ' '.join(tokens)
#     except Exception as e:
#         print(f"Error in preprocess_text: {e}")
#         raise

# # Load data
# data = pd.read_csv('resume_screening.csv')

# # Combine text columns
# data['Combined_Text'] = data['Skills'].astype(str) + ' ' + data['Education'].astype(str) + ' ' + data['Certifications'].astype(str)
# data['Processed_Text'] = data['Combined_Text'].apply(preprocess_text)

# # TF-IDF Vectorization
# tfidf_vectorizer = TfidfVectorizer(max_features=15)
# tfidf_matrix = tfidf_vectorizer.fit_transform(data['Processed_Text'])

# # Prepare features for selection model
# X_selection = np.hstack([
#     tfidf_matrix.toarray(),
#     data[['Experience', 'Projects Count']].values
# ])
# y_selection = data['Recruiter Decision']

# # Train selection model
# X_train, X_test, y_train, y_test = train_test_split(X_selection, y_selection, test_size=0.2, random_state=42)
# selection_model = LogisticRegression(max_iter=1000)
# selection_model.fit(X_train, y_train)

# # Prepare features for salary model
# X_salary = data[['Experience', 'Projects Count']].values
# y_salary = data['Salary Expectation ($)']
# X_salary_train, X_salary_test, y_salary_train, y_salary_test = train_test_split(X_salary, y_salary, test_size=0.2, random_state=42)
# salary_model = RandomForestRegressor(n_estimators=100, random_state=42)
# salary_model.fit(X_salary_train, y_salary_train)

# # Save models and vectorizer
# joblib.dump(selection_model, 'selection_model.pkl')
# joblib.dump(salary_model, 'salary_model.pkl')
# joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')

# print(f"Selection model trained with {X_selection.shape[1]} features")
# print(f"Salary model trained with {X_salary.shape[1]} features")

#wobaffet 

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import re
from nltk.tokenize import word_tokenize

# Fallback stopwords (unchanged, matching app.py)
FALLBACK_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
    'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
    'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
    'will', 'just', 'don', 'should', 'now'
}

def preprocess_text(text):
    try:
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        tokens = word_tokenize(text)
        stop_words = FALLBACK_STOPWORDS
        tokens = [word for word in tokens if word not in stop_words]
        return ' '.join(tokens)
    except Exception as e:
        print(f"Error in preprocess_text: {e}")
        raise

# Load data
data = pd.read_csv('resume_screening.csv')

# Use full resume text (adjust column name based on your CSV)
# If you have a 'Resume_Text' column, use it; otherwise, combine relevant fields
if 'Resume_Text' in data.columns:
    data['Full_Resume'] = data['Resume_Text']
else:
    # Fallback to combining all text fields if Resume_Text isn't available
    data['Full_Resume'] = data['Skills'].astype(str) + ' ' + data['Education'].astype(str) + ' ' + \
                          data['Certifications'].astype(str) + ' ' + data.get('Experience', '').astype(str)

data['Processed_Resume'] = data['Full_Resume'].apply(preprocess_text)

# TF-IDF Vectorization using the full resume text
tfidf_vectorizer = TfidfVectorizer(max_features=15)  # Matches app.py
tfidf_matrix = tfidf_vectorizer.fit_transform(data['Processed_Resume'])

# Prepare features for selection model
# Convert Experience to numeric (assuming it's like "3 years" or a number)
data['Experience'] = data['Experience'].apply(lambda x: float(x.split()[0]) if isinstance(x, str) and x.split() else 0.0)
# Use 'Projects Count' as is (assuming it's numeric)
X_selection = np.hstack([
    tfidf_matrix.toarray(),
    data[['Experience', 'Projects Count']].values
])
y_selection = data['Recruiter Decision']

# Train selection model
X_train, X_test, y_train, y_test = train_test_split(X_selection, y_selection, test_size=0.2, random_state=42)
selection_model = LogisticRegression(max_iter=1000)
selection_model.fit(X_train, y_train)

# Evaluate the model
y_pred = selection_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Selection model accuracy: {accuracy:.2f} with {X_selection.shape[1]} features.")

# Prepare features for salary model
X_salary = data[['Experience', 'Projects Count']].values
y_salary = data['Salary Expectation ($)']
X_salary_train, X_salary_test, y_salary_train, y_salary_test = train_test_split(X_salary, y_salary, test_size=0.2, random_state=42)
salary_model = RandomForestRegressor(n_estimators=100, random_state=42)
salary_model.fit(X_salary_train, y_salary_train)

# Save models and vectorizer
joblib.dump(selection_model, 'selection_model.pkl')
joblib.dump(salary_model, 'salary_model.pkl')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')

print(f"Selection model trained with {X_selection.shape[1]} features")
print(f"Salary model trained with {X_salary.shape[1]} features")