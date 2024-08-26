from collections import defaultdict
import string

from nltk.corpus import stopwords
import frontmatter
import os

titles = []
categories = []
title_index = defaultdict(list)

stopwords = set(stopwords.words("english"))

for root, _, files in os.walk("../pages/posts"):
    for file in files:
        with open(os.path.join(root, file)) as f:
            post = frontmatter.load(f)
            titles.append(post["title"])
            categories.append(post.get("categories", ["Post"])[0])

def get_title_words(titles):
    titles = [title.lower().translate(str.maketrans("", "", string.punctuation)) for title in titles]
    titles = [title.split(" ") for title in titles]
    titles = [[word for word in title if word not in stopwords] for title in titles]
    titles = [set(title) for title in titles]

    return titles

def build_title_index(titles):
    title_index = defaultdict(list)

    for i, title in enumerate(titles):
        for word in title:
            title_index[word].append(i)

    return title_index

def calculate_categories_from_title_words(query, title_index):
    title_word_candidates = [title_index[word] for word in query]
    title_word_candidates = [word for sublist in title_word_candidates for word in sublist]
    title_word_candidates = list(set(title_word_candidates))

    category_counts = defaultdict(int)

    for title_index in title_word_candidates:
        category = categories[title_index]
        category_counts[category] += 1

    title_word_candidates = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    category_names = [category for category, count in title_word_candidates if count > 1]

    return category_names

query = "taylor swift"

query_words = get_title_words([query])[0]

title_words = get_title_words(titles)
title_index = build_title_index(title_words)
results = calculate_categories_from_title_words(query_words, title_index)

if len(results) == 0:
    print("No results found")
else:
    print("Top result:", results[0])
