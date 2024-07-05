"""
Flask Server
"""
from flask import Flask
from flask_cors import CORS

"""
Blueprint import
"""
#main
from src.route import wordList_route
from src.route import nameList_route
from src.route import nameList2_route
from src.route import yakiList_route
from src.route import yakiList_route
from src.route import schoolList_route
from src.route import haikuList_route
from src.route import imageList_route

#file
from src.route import karaokeList_route
from src.route import radioList_route
from src.route import ssbuList_route
from src.route import voiceList_route
from src.route import support_route
from src.route import movieList_route

#scraper
from src.route import twitter_route
from src.route import holosong_route
from src.route import holomovie_route
from src.route import holoarchive_route
from src.route import hololewd_route
from src.route import pixiv_route

#sub
from src.route import rembg_route

"""
Flask run
"""
app = Flask(__name__)
CORS(app)

"""
register blueprint
"""
#main
app.register_blueprint(wordList_route.app)
app.register_blueprint(nameList_route.app)
app.register_blueprint(nameList2_route.app)
app.register_blueprint(yakiList_route.app)
app.register_blueprint(schoolList_route.app)
app.register_blueprint(haikuList_route.app)
app.register_blueprint(imageList_route.app)
#file
app.register_blueprint(karaokeList_route.app)
app.register_blueprint(radioList_route.app)
app.register_blueprint(ssbuList_route.app)
app.register_blueprint(voiceList_route.app)
app.register_blueprint(support_route.app)
app.register_blueprint(movieList_route.app)
#scraper
app.register_blueprint(twitter_route.app)
app.register_blueprint(holosong_route.app)
app.register_blueprint(holomovie_route.app)
app.register_blueprint(holoarchive_route.app)
app.register_blueprint(hololewd_route.app)
app.register_blueprint(pixiv_route.app)
#sub
app.register_blueprint(rembg_route.app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)