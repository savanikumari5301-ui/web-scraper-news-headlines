import requests
from bs4 import BeautifulSoup


def scrape_news_headlines():
    # Target news website (Using BBC News as a reliable, public example)
    url = "https://www.bbc.com/news"

    # Define a User-Agent to mimic a real browser request and avoid being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Fetching data from {url}...")

    try:
        # Send a GET request to the website
        response = requests.get(url, headers=headers)

        # Check if the request was successful (Status Code 200)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all headline tags. BBC heavily uses <h2> for major headlines
        # (You can also search for 'title' or class names depending on the site)
        headlines = soup.find_all("h2")

        # Extract clean text and filter out empty or duplicate lines
        unique_headlines = []
        for h in headlines:
            text = h.get_text(strip=True)
            if text and text not in unique_headlines:
                unique_headlines.append(text)

        # Check if we found anything
        if not unique_headlines:
            print("No headlines found. The website structure might have changed.")
            return

        print(f"Successfully found {len(unique_headlines)} headlines!")

        # Save the headlines into a .txt file
        output_filename = "news_headlines.txt"
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write("=== TOP NEWS HEADLINES ===\n\n")
            for index, headline in enumerate(unique_headlines, 1):
                file.write(f"{index}. {headline}\n")

        print(f"Results successfully saved to '{output_filename}'")

    except requests.exceptions.RequestException as e:
        # Handle network-related errors gracefully
        print(f"An error occurred while fetching the webpage: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    scrape_news_headlines()