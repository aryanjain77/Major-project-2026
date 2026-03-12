import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
import joblib
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Load dataset
df = pd.read_csv('resume_screening.csv')

# Handle missing values and combine text features
for col in ['Skills', 'Education', 'Certifications', 'Job Role']:
    df[col] = df[col].fillna('')  # Replace NaN with empty string
df['Text'] = df['Skills'] + ' ' + df['Education'] + ' ' + df['Certifications'] + ' ' + df['Job Role']
df['Text'] = df['Text'].str.lower().str.replace(r'[^\w\s]', '', regex=True)
stop = stopwords.words('english')
df['Text'] = df['Text'].apply(lambda x: ' '.join(word for word in str(x).split() if word not in stop))

# Features and target
X = df[['Text', 'Experience (Years)', 'Projects Count', 'Salary Expectation ($)']]
y = df['Recruiter Decision']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline: TF-IDF for text, StandardScaler for numeric
preprocessor = ColumnTransformer([
    ('text', TfidfVectorizer(max_features=5000), 'Text'),
    ('numeric', StandardScaler(), ['Experience (Years)', 'Projects Count', 'Salary Expectation ($)'])
])
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train
pipeline.fit(X_train, y_train)

# Evaluate
preds = pipeline.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, preds)}")

# Save model
joblib.dump(pipeline, 'resume_model.pkl')