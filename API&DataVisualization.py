import requests
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# === Parameters ===
QUERY = "Human Psychology"
MAX_RESULTS = 20
API_URL = "https://www.googleapis.com/books/v1/volumes"

# === Fetch Data ===
params = {
    'q': QUERY,
    'maxResults': MAX_RESULTS,
}
response = requests.get(API_URL, params=params)
books_data = response.json()

# === Parse Book Info ===
book_titles = []
book_ratings = []
ratings_count = []
all_categories = []

for book in books_data.get('items', []):
    info = book.get('volumeInfo', {})
    title = info.get('title')
    avg_rating = info.get('averageRating')
    rating_count = info.get('ratingsCount', 0)
    genres = info.get('categories', [])

    if title and avg_rating is not None:
        book_titles.append(title)
        book_ratings.append(avg_rating)
        ratings_count.append(rating_count)
        all_categories.extend(genres)

# === Visualization 1: Ratings Bar Chart ===
plt.figure(figsize=(10, 5))
sns.barplot(x=book_titles, y=book_ratings)
plt.title(f"Top Rated Books for '{QUERY}'")
plt.xlabel("Book Title")
plt.ylabel("Average Rating")
plt.tight_layout()
plt.show()

# === Visualization 2: Ratings Count Distribution ===
plt.figure(figsize=(10, 5))
sns.histplot(ratings_count, bins=10, kde=True, color='blue')
plt.title("Distribution of Ratings Count")
plt.xlabel("Number of Books")
plt.ylabel("Rating Count")
plt.tight_layout()
plt.show()

# === Visualization 3: Category Pie Chart ===
category_counts = Counter(all_categories)
labels = list(category_counts.keys())
sizes = list(category_counts.values())

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title("Genre Distribution Among Results")
plt.tight_layout()
plt.show()
