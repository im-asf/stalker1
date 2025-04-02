from flask import Flask, Response, request
import requests

app = Flask(__name__)

USER_AGENT = "tv.accedo.airtel.wynk/1.97.1 (Linux;Android 11) ExoPlayerLib/2.19.1"

def modify_m3u(content):
    """ Convert DASH (.mpd) to HLS (.m3u8) and remove Kodi-specific lines """
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if "KODIPROP" in line:
            continue  # Remove unnecessary lines
        if "manifest.mpd" in line:
            line = line.replace("manifest.mpd", "index.m3u8")  # Convert to HLS
        new_lines.append(line)
    return "\n".join(new_lines)

@app.route("/")
def index():
    m3u_url = request.args.get("url")  # Get M3U URL from query parameter
    if not m3u_url:
        return "Error: Please provide a valid M3U URL using ?url=YOUR_M3U_LINK", 400

    headers = {"User-Agent": USER_AGENT}
    response = requests.get(m3u_url, headers=headers)

    if response.status_code == 200:
        modified_content = modify_m3u(response.text)
        return Response(modified_content, mimetype="audio/x-mpegurl")
    return f"Failed to fetch M3U (Status {response.status_code})", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
