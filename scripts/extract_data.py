import os
import csv
import time
from dotenv import load_dotenv

# Ensure we can import from src/
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.extraction import search_users_by_location, fetch_user_profile

def save_to_csv(rows, filename="data/processed/users.csv"):
    if not rows:
        print("No data to save.")
        return

    # Infer fields from the first row
    all_fields = list(rows[0].keys())

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅  Saved {len(rows)} users → {filename}")


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("GITHUB_TOKEN")
    
    if not TOKEN or TOKEN == "your_github_token_here":
        print("Error: Please valid GITHUB_TOKEN in your .env file.")
        sys.exit(1)

    # Step 1 – collect up to 1000 logins from search
    location = "peru"
    print(f"Searching for users in {location}...")
    logins = search_users_by_location(TOKEN, location=location, max_users=1000)
    print(f"\nFound {len(logins)} users in search results. Fetching full profiles …\n")

    # Step 2 – pull every profile individually
    rows = []
    for i, login in enumerate(logins, 1):
        profile = fetch_user_profile(TOKEN, login)
        if profile:
            rows.append(profile)

        if i % 50 == 0:
            print(f"  Progress: {i}/{len(logins)} profiles fetched")

        time.sleep(0.5)

    # Step 3 – write CSV
    save_to_csv(rows)
