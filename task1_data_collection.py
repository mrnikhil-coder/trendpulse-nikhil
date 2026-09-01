import requests
url = "https://hacker-news.firebaseio.com/v0/topstories.json"

headers = {
    "User-Agent": "TrendPulse/1.0"
}

response = requests.get(url, headers=headers)

print(response.status_code)
story_ids = response.json()[:500]

print(len(story_ids))
def get_category(title):
    title = title.lower()

    technology = ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"]
    worldnews = ["war", "government", "country", "president", "election", "climate", "attack", "global"]
    sports = ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"]
    science = ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"]
    entertainment = ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]

    for word in technology:
        if word in title:
            return "technology"

    for word in worldnews:
        if word in title:
            return "worldnews"

    for word in sports:
        if word in title:
            return "sports"

    for word in science:
        if word in title:
            return "science"

    for word in entertainment:
        if word in title:
            return "entertainment"

    return None
stories = []

for story_id in story_ids:
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

    try:
        story_response = requests.get(story_url, headers=headers)

        if story_response.status_code == 200:
            story = story_response.json()
            stories.append(story)
        else:
            print(f"Failed to fetch story {story_id}")

    except requests.RequestException as error:
        print(f"Error fetching story {story_id}: {error}")

print("Stories fetched:", len(stories))
from datetime import datetime
import time

categories = {
    "technology": [],
    "worldnews": [],
    "sports": [],
    "science": [],
    "entertainment": []
}

category_keywords = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

for category, keywords in category_keywords.items():

    for story in stories:
        if len(categories[category]) >= 25:
            break

        title = story.get("title", "").lower()

        if any(word in title for word in keywords):
            cleaned_story = {
                "post_id": story.get("id"),
                "title": story.get("title", ""),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().isoformat()
            }

            categories[category].append(cleaned_story)

    time.sleep(2)

all_stories = []

for category_stories in categories.values():
    all_stories.extend(category_stories)

print("Total collected:", len(all_stories))

for category, category_stories in categories.items():
    print(category, ":", len(category_stories))
import os
import json

os.makedirs("data", exist_ok=True)

date = datetime.now().strftime("%Y%m%d")
file_path = f"data/trends_{date}.json"

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(all_stories, file, indent=4, ensure_ascii=False)

print(f"Collected {len(all_stories)} stories. Saved to {file_path}")