import requests
import pandas as pd
import time

def fetch_all_openalex_articles(query, output_file="data/openalex(PSU)_results_all.csv", per_page=200):
    base_url = "https://api.openalex.org/works"
    cursor = "*"
    all_articles = []
    total_fetched = 0
    page = 1

    while cursor:
        params = {
            "search": query,
            "per-page": per_page,
            "cursor": cursor
        }

        try:
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break

        data = response.json()
        results = data.get("results", [])
        cursor = data.get("meta", {}).get("next_cursor")

        for work in results:
            article = {
                "id": work.get("id"),
                "title": work.get("title"),
                "doi": work.get("doi"),
                "publication_year": work.get("publication_year"),
                "type": work.get("type"),
                "cited_by_count": work.get("cited_by_count"),
                "authors": ", ".join([a["author"]["display_name"] for a in work.get("authorships", [])]),
                "host_venue": work.get("host_venue", {}).get("display_name"),
                "publisher": work.get("host_venue", {}).get("publisher"),
                "concepts": ", ".join([c["display_name"] for c in work.get("concepts", [])])
            }
            all_articles.append(article)

        total_fetched += len(results)
        print(f"Page {page}: fetched {len(results)} articles (total so far: {total_fetched})")
        page += 1

        if not results:
            print("No more results.")
            break

        time.sleep(1)  # ป้องกัน server overload

    # Save to CSV
    df = pd.DataFrame(all_articles)
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"\nCompleted. Total {len(df)} articles saved to {output_file}")

if __name__ == "__main__":
    fetch_all_openalex_articles("Prince of Songkla University")
