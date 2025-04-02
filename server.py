from flask import Flask, Response
import requests

app = Flask(__name__)

M3U_URL = "https://m3u.ygxworld.in/p/Kzp32CQjHyEe/playlist.m3u"

def modify_m3u(content):
    # Convert .mpd links to .m3u8 for SS IPTV compatibility
    return content.replace("manifest.mpd", "index.m3u8")

@app.route("/")
def index():
    response = requests.get(M3U_URL)
    if response.status_code == 200:
        modified_content = modify_m3u(response.text)
        return Response(modified_content, mimetype="audio/x-mpegurl")
    return "Failed to fetch M3U", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

