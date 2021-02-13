# Rust-Classification
Rust classification for oil/gas pipeline inspections and maintenance.

-A low-cost robot was built to navigate pipes and make predictions.

-An online server was also built to monitor multiple robots' behavior as well as see the predictions of each robot on the field.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

The code runs on python3
all needed libraries are present in the requirments.txt file,
the most important ones are;

```
keras, with tensorflow backend
```
This was used to build and train the model

```
Pillow
```
Was used to read the images from the url

```
opencv-python
```
Which was used to process the images


```
Flask
```
which was used to build the backend server.


### Installing



make sure you have a python3 setup up and running

then to install the needed libraries

```
pip install -r requirements.txt
```

A config file is needed, for our application we created a file
```
config.py
```
This file includes a class configure, with a function called getCloudInfo
this function returns the cloudName, apiKey, apiSecret to the cloudinary service.

### Break down into file system and Algorithms used


```
python server.py
```
Hosts the flask web application,
the application takes as parameter the url of an image the model then classifies the image to rust and not rust and returns the prediction.

```
fileUpload.py
```
Is a demo to how images are uploaded to cloudinary as well as how the server is updated with robot's location, and image location.

```
corrosion Detection.py
```
This file holds the computer vision approach along with trying to use the model to have some sort of rcnn based detection without the use of rcnns.
The idea is to break the image into multiple smaller images and classify each of them individually then combine rusted parts to form a boundingbox.

```
humanLevelPerformance.py
```
For some baseline accuracy of how humans perform, a simple survey was conducted.
The code shuffles the dataset, and picks a random number of images to show, then people are asked to classify them into rusted images and non-rusted images. The results later would show a baseline of how humans percieve the information about rust.


```
savingData.py
```
Since data was collected manually, a labeling tool was created to be able to go through all the dataset and label each image and move it to a seprate folder.
This sped up the labeling process.


```
vgg19Model.py
```
This file holds the creation and training of the VGG19 model trained on our dataset.




### Running the training
The dataset folder has sample images of the dataset.
run the vgg19Model.py file and the training will start on the dataset and use the images in test for testing.





#### Results
Results of 98% testing accuracy was achived on training and detection of rusted images.
The project also was able to use a raspberry pi to collect images of rusted pipelines and classify the rusted regions correctly.


