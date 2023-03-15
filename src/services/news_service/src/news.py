"""This application is news service.

 The news service is a service that provides news information for a given location.
 It provides an endpoint to get the news information for a given location for the next day.
 The functionality is based in the Tagesschau API.
 """

from flask import Flask, jsonify, request
import requests
import dotenv
import os

dotenv.load_dotenv()
NYTimes_API_KEY = os.getenv("NYTIMES_API_KEY")

app = Flask(__name__)

@app.route('/news/tagesschau/here')
def get_tagesschau():
    """Weather information endpoint.

    This endpoint provides news information for a given location for the current moment.

    Args:
        regions: The region inside germany for the news
            Bundesland - 1=Baden-Württemberg, 2=Bayern, 3=Berlin, 4=Brandenburg, 5=Bremen, 6=Hamburg, 7=Hessen, 8=Mecklenburg-Vorpommern, 9=Niedersachsen, 10=Nordrhein-Westfalen, 11=Rheinland-Pfalz, 12=Saarland, 13=Sachsen, 14=Sachsen-Anhalt, 15=Schleswig-Holstein, 16=Thüringen. Mehrere Komma-getrennte Angaben möglich (z.B. regions=1,2).
            Available values : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
        ressorts: The topic of the news
            Available values : inland, ausland, wirtschaft, sport, video, investigativ, faktenfinder

    Returns:
        The news information that are currently available
    """
    if request.args.get("regions").isdigit() is None or request.args.get("ressort").isalpha() is None:
             return jsonify({"error": "Missing parameters"}), 400
    

    regions = request.args.get("regions")
    ressort =  request.args.get("ressort")

    url = f'https://www.tagesschau.de/api2/news/?"regions"={regions}&ressort={ressort}'
    response = requests.get(url)
    if response.status_code != 200:
        jsonify({'error': 'Error getting weather information'}), 500

    data = response.json()

    return jsonify(data)

@app.route('/news/tagesschau/homepage')
def get_tagesschau_homepage():
    """News information endpoint.

    This endpoint provides news information from the Tagesschau homepage.

    Args:
        
    Returns:
        The news information that are currently available
    """
     
    url = 'https://www.tagesschau.de/api2/homepage/'
    response = requests.get(url)
    if response.status_code != 200:
        jsonify({'error': 'Error getting news information'}), 500

    data = response.json()

    return jsonify(data)

@app.route('/news/nytimes')

def get_NY_Times():
    '''
    News information endpoint.

    This endpoint provides news information from the New York Times homepage.

    Args:
        api_key =
        category = possible options: arts,home,science,us,world
    Returns:
        The news information that are currently available
    https://api.nytimes.com/svc/topstories/v2/arts.json?api-key=yourkey
    https://api.nytimes.com/svc/topstories/v2/home.json?api-key=yourkey
    https://api.nytimes.com/svc/topstories/v2/science.json?api-key=yourkey
    https://api.nytimes.com/svc/topstories/v2/us.json?api-key=yourkey
    https://api.nytimes.com/svc/topstories/v2/world.json?api-key=yourkey
    '''
    if request.args.get("category") is None:
         return jsonify({"error": "Missing parameters"}), 400
    
    category = request.args.get("category")

    api_key = NYTimes_API_KEY
    url = f'https://api.nytimes.com/svc/topstories/v2/{category}.json?api-key=.{api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        jsonify({'error': 'Error getting news information'}), 500

    data = response.json()

    return jsonify(data)

   

if __name__ == '__main__':
    app.run()