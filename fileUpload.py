import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests
from config import configure #config.py holds the api keys and uris 


config= configure()

cloudName,apiKey,apiSecret= config.getCloudInfo() #we get the cloudinary info for signing in

cloudinary.config( 
  cloud_name = cloudName, 
  api_key = apiKey , 
  api_secret = apiSecret 
)

result=cloudinary.uploader.upload(open('test.png','rb')) #this opens a file and uploads it to cloudinary
print(result) #this prints the json file returned from cloudinary


robot = {
    "imagesAndLocations": [{
        "image":result['url'], 
        #this sends the url of the image to the server where it can be downloaded
        
        "location":[0.0,0.0] 
        #this is a location of every image taken should be updated with the actual locations
        
        }],
    "robotLocation":[0.0,0.0] #this is the actual location of the robot
}

response= requests.put("http://localhost:8000/api/robots/addImages/5d2f6d014ea22c471ce58cde" ,json= robot)
#we send a put request to the server right now its using the local host but will be updated later 
#to use the deployed links


print(response.json())
#then we print the response for now to see if it works fine