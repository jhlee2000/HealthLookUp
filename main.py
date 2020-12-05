from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from HealthResult import HealthResult
import requests


app = Flask(__name__)


# health search
@app.route("/", methods=["POST", "GET"])
def test():
    if request.method == "POST":
        results_list = []

        query = request.form["query"]
        # TODO: Check for nulls, if None
        # WebMD
        url = "https://www.webmd.com/search/search_results/default.aspx?query=" + query
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/87.0.4280.88 Safari/537.36"}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id='ContentPane28')
        _results = results.find_all("div", class_="search-text-container")
        for i in _results:
            print("WEBMD")
            print(fuzz.ratio(query, i.find("a").text.strip()))
            print(i.find("a").text.strip())
            description = i.find("p", class_="search-results-doc-description")
            description = str(description)
            if fuzz.ratio(query, i.find("a").text.strip()) > 40:
                new_object = HealthResult("WebMD", i.find("a").text.strip(), description[42:-4].strip(),
                                          i.find("a")["href"])
                results_list.append(new_object)

        # Harvard Health
        url = "https://www.health.harvard.edu/search?q=" + query
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div", class_="search-result")
        for i in results:
            print("HARVARD")
            print(fuzz.ratio(query, i.find("a").text.strip()))
            print(i.find("a").text.strip())
            if fuzz.ratio(query, i.find("a").text.strip()) > 26:
                new_object = HealthResult("Harvard Health", i.find("a").text.strip(), "", i.find("a")["href"])
                results_list.append(new_object)

        return render_template("home.html", results_list=results_list)
    return render_template("home.html")


@app.route("/map", methods=["POST", "GET"])
def mapbox():
    return render_template("map.html")


@app.route("/exercise", methods=["POST", "GET"])
def exercise():
    return render_template("exercise.html")


if __name__ == "__main__":
    app.run()