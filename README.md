# website-visitor-stat-app
A Flask server app which tracks visitor IP location and updates unique visitor count that can be integrated in a website. 
See the deplyoment here at [https://dutta-alankar.github.io/website-visitor-stat-app/](https://dutta-alankar.github.io/website-visitor-stat-app/).

[![PyPI](https://img.shields.io/badge/requires-Python%20≥%203.10-blue?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-310/)  
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/dutta-alankar/website-visitor-stat-app/main.svg)](https://results.pre-commit.ci/latest/github/dutta-alankar/website-visitor-stat-app/main)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/dutta-alankar/website-visitor-stat-app/main) 
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
![GitHub](https://img.shields.io/github/license/dutta-alankar/website-visitor-stat-app)


I have also provided a sample html client that can be modified and used in any webpage. The client also puts the geo-coordinates of the unique visitors on the map in a dynamic webpage. 
Make sure to change the `serverAddress` in the html javascript of the client to point to your server. 
`statserver.py` is the Flask server code that I'm using. I have hosted my server in [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/). 
You can choose whatever suits you. 

To run the server, install all the dependencies using `pip install -r requirements.txt`
