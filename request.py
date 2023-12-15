# import ImageFromCam
# import ImageFromVideo
import requests

url =  "http://localhost:9000/function/files/"
filename = "test.jpg"

with open(filename, "rb") as f:
    contents = f.read()

files = {"file" : (filename, contents, "image/jpg")}

response = requests.post(url, files = files)
print(response.json())