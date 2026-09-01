

import requests
import time
import json
import os
from datetime import datetime



top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"

headers = {
    "User-Agent": "TrendPulse/1.0"
}


categories = {
    "technology": [
        "ai", "software", "tech", "code", "computer",
        "data", "cloud", "api", "gpu", "llm"
    ],

    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],

    "sports": [
        "nfl", "nba", "fifa", "sport", "game",
        "team", "player", "league", "championship"
    ],

    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "nasa", "genome"
    ],

    "entertainment": [
        "movie", "film", "music", "netflix",
        "game", "book", "show", "award", "streaming"
    ]
}




try:

    response = requests.get(
        top_stories_url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    story_ids = response.json()

    story_ids = story_ids[:500]

    print("Successfully fetched", len(story_ids), "story IDs.")

except requests.RequestException as error:

    print("Failed to fetch top stories:", error)

    story_ids = []


all_stories = []



used_ids = set()




for category, keywords in categories.items():

    print("Processing category:", category)

    category_count = 0

    for story_id in story_ids:


        if category_count >= 25:
            break

        story_url = (
            f"https://hacker-news.firebaseio.com/v0/item/"
            f"{story_id}.json"
        )

        try:

            response = requests.get(
                story_url,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            story = response.json()

        except requests.RequestException as error:

            print(
                f"Failed to fetch story {story_id}:",
                error
            )
            continue


        

        title = story.get("title", "")

        #
        title_lower = title.lower()



        if any(keyword in title_lower for keyword in keywords):

            
            if story_id in used_ids:
                continue


            

            record = {
                "post_id": story.get("id"),
                "title": title,
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().isoformat()
            }


            # Add the record to our main list
            all_stories.append(record)

            # Remember this story ID
            used_ids.add(story_id)

            # Increase category count
            category_count += 1

            print(
                f"  Collected {category_count}/25:",
                title
            )




    time.sleep(2)



os.makedirs("data", exist_ok=True)



date_string = datetime.now().strftime("%Y%m%d")

filename = f"data/trends_{date_string}.json"



with open(filename, "w", encoding="utf-8") as file:

    json.dump(
        all_stories,
        file,
        indent=4,
        ensure_ascii=False
    )




print()
print(
    f"Collected {len(all_stories)} stories. "
    f"Saved to {filename}"
)
