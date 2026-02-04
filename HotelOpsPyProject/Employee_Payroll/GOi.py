import requests
from bs4 import BeautifulSoup

# Example: Scrape reviews from a URL
url = "https://www.goibibo.com/hotels/treebo-premium-akshaya-mahal-inn-hotel-in-mysore-3201987182997167974/"
headers = {"User-Agent": "your-user-agent"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Find reviews
reviews_section = soup.find(id="guest-reviews") # Adjust the class based on the actual HTML
if reviews_section:
    # Find all review elements within that section
    reviews = reviews_section.find_all("div", class_="bIyWTs")  # Replace with the correct tag and class name
    print(f"Found {len(reviews)} reviews.")
    for review in reviews:
        review_text = review.find("span", class_="cxlJmB").text  # Replace with the correct tag and class name
        print(review_text)
else:
    print("No review section found with that ID.")
# print(reviews)
# for review in reviews:
#     review_text = review.find("p", class_="review-text-class").text
#     print(review_text)
