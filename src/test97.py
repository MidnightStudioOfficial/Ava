import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Prepare the dataset
book_titles = [
    "The Great Gatsby",
    "To Kill a Mockingbird",
    "Pride and Prejudice",
    "1984",
    "The Catcher in the Rye",
    "Brave New World",
    "Animal Farm",
    "The Hobbit",
    "The Lord of the Rings",
    "Harry Potter and the Sorcerer's Stone",
]

book_descriptions = [
    "A story about the fabulously wealthy Jay Gatsby.",
    "A classic novel set in the 1930s America.",
    "A romantic novel by Jane Austen.",
    "A dystopian novel by George Orwell.",
    "A coming-of-age novel by J.D. Salinger.",
    "A dystopian novel by Aldous Huxley.",
    "A political allegory by George Orwell.",
    "A fantasy novel by J.R.R. Tolkien.",
    "A high fantasy novel by J.R.R. Tolkien.",
    "The first book in the Harry Potter series.",
]

# Step 2: Preprocess the data
nltk.download("punkt")  # Download the necessary NLTK data

# Tokenize and normalize the book descriptions
tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
preprocessed_book_descriptions = [
    tokenizer.tokenize(desc.lower()) for desc in book_descriptions
]

# Step 3: Train the model
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(
    [" ".join(desc) for desc in preprocessed_book_descriptions]
)
cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Step 4: Get personalized recommendations
user_input = input("Enter your interests: ")

# Preprocess the user input
preprocessed_user_input = tokenizer.tokenize(user_input.lower())

# Transform the preprocessed user input using the trained vectorizer
user_tfidf = vectorizer.transform([" ".join(preprocessed_user_input)])

# Calculate the cosine similarities between the user input and book descriptions
similarities = cosine_similarity(user_tfidf, tfidf_matrix).flatten()

# Sort the similarities in descending order
similarities_indices = similarities.argsort()[::-1]

# Display the top 3 recommendations
print("Top 3 Book Recommendations:")
for index in similarities_indices[:3]:
    print(f"Book: {book_titles[index]}")
    print(f"Description: {book_descriptions[index]}")
    print()
