
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://books.toscrape.com/"
dataset = []

while url:
    print("Scraping:", url)

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    for book in soup.select("article.product_pod"):
        title = book.h3.a["title"]
        price = book.select_one(".price_color").get_text(strip=True)
        availability = book.select_one(".availability").get_text(strip=True)

        # Normalize price text
        price = price.replace("Â", "").replace("£", "")

        dataset.append({
            "Title": title,
            "Price (£)": price,
            "Availability": availability
        })

    next_page = soup.select_one("li.next a")

    if next_page:
        url = urljoin(url, next_page["href"])
    else:
        url = None

with open("books_dataset.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["Title", "Price (£)", "Availability"]
    )
    writer.writeheader()
    writer.writerows(dataset)

print("\nWeb scraping completed!")
print("Total books collected:", len(dataset))
print("Saved to books_dataset.csv")
