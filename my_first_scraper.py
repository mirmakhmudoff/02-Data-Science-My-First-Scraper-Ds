import requests
from bs4 import BeautifulSoup


def request_github_trending(url):
    return requests.get(url)


def extract(page):
    soup = BeautifulSoup(page.text, "html.parser")
    return soup.find_all("article", class_="Box-row")


def transform(html_repos):
    result = []
    for row in html_repos:
        temp = row.select_one("h2.h3.lh-condensed").text.strip().split("/")
        dev_name = temp[0]
        repo_name = temp[-1].strip()
        nbr_stars = row.select_one("a.Link.Link--muted.d-inline-block.mr-3").text.strip()
        result.append(
            {
                "developer": dev_name,
                "repository_name": repo_name,
                "nbr_stars": nbr_stars
            }
        )
    return result


def format(repositories_data):
    with open("github_trends.csv", "w+") as file:
        file.write("Developer Name, Repository Name, Number of Stars\n")
        for row in repositories_data:
            file.write(f"{row['developer']}, {row['repository_name']}, {row['nbr_stars']}\n")
    print("Successfully saved")


response = request_github_trending("https://github.com/trending")
extracted_data = extract(response)
transformed_data = transform(extracted_data)
format(transformed_data)