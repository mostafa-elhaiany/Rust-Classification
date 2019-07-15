# =============================================================================
# this file holds the computer vision approach along with trying to use the model 
# to have some sort of rcnn based detection without the use of rcnns
# the idea is to break the image into multiple 224x224 images 
# and have the model predict all of them and return which parts it thinks there's rust
# however we then have the computer vision approach 
# the algorithm should classify which parts the model thinks its rusted
# which parts the cv thinks its rusted 
# and which parts they both agree on it 
# =============================================================================

import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2


# =============================================================================
# this is a computer vision approach suggested in a paper that classifies the image based on the 
# percentage of red in the image
# its faulty but assuming the pipelines won't be painted red or its shades it should have
# nice results
# =============================================================================
def filterRust(image1):   
    image= cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    lowerRed=np.array([0,50,50])
    upperRed=np.array([10,210,210])
    
    lowerRed2=np.array([175,50,50])
    upperRed2=np.array([176,210,210])
    
    mask1= cv2.inRange(image,lowerRed,upperRed)
    mask2=cv2.inRange(image,lowerRed2,upperRed2)
    mask=mask1+mask2
    ret,maskBin=cv2.threshold(mask,110,240,cv2.THRESH_BINARY)
    height,width=maskBin.shape
    size=height * width
    percentage=cv2.countNonZero(maskBin)/float(size)
    print(percentage)
    if(percentage>=0.002):
        return True
    else:
        return False

def filterImage(image):        #filters rust color from image and returns the start and end of rust
    
    image1= cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    image2= cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    mask1 = cv2.inRange(image2, (10,120,0), (20,190,20))
    mask2 = cv2.inRange(image1, (120,0,0), (200,255,255))
    mask3 = cv2.inRange(image1, (240,160,0), (225,244,220))
   
    mask=mask1+mask2
    mask-=mask3
    output = cv2.bitwise_or(image, image, mask = mask)
    points=[]
    size=0
    c=0
    for x in output:
        if(np.sum(x)!=0):
            points.append(c)
            size+=1
        c+=1
    if(filterRust(image)):
        return points,size #returns all the points where there's rust and the size of the array
    else:
        return [],0
def drawBoxImages(image):
    image= cv2.resize(image, dsize=(224, 224))
    rows,cols,_ = image.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    image2 = cv2.warpAffine(image,M,(cols,rows)) #Rotated Image

    pointsY,sizeY= filterImage(image) 
    pointsX,sizeX= filterImage(image2)
    if(sizeX>0):
        startX=pointsX[0] #the start point of the bounding box is the first X and first
        endX=pointsX[sizeX-1]-startX   #subtracting the last point with the first point from Both
    else:
        startX=0
        endX=0    
    if(sizeY>0):
        startY=pointsY[0] # Y from both arrays it states where the first (X,Y) for the bounding box to start  
        endY=pointsY[sizeY-1]-startY   # last X and Y points gives us the displacments
    else:
        startY=0
        endY=0    
    cv2.rectangle(image,(startX,startY),(endX,endY),(0,255,0),2)
    return image 

def drawBox(path):
    image= cv2.imread(path) #load image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image= cv2.resize(image, dsize=(200, 200))
    rows,cols,_ = image.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    image2 = cv2.warpAffine(image,M,(cols,rows)) #Rotated Image
    
    pointsY,sizeY= filterImage(image) 
    pointsX,sizeX= filterImage(image2)
    if(sizeX>0):
        startX=pointsX[0] #the start point of the bounding box is the first X and first
        endX=pointsX[sizeX-1]-startX   #subtracting the last point with the first point from Both
    else:
        startX=0
        endX=0    
    if(sizeY>0):
        startY=pointsY[0] # Y from both arrays it states where the first (X,Y) for the bounding box to start  
        endY=pointsY[sizeY-1]-startY   # last X and Y points gives us the displacments
    else:
        startY=0
        endY=0    
   
    fig,ax = plt.subplots(1) #plotting fig and ax to use the figure to draw the bounding box
    ax.imshow(image)   
    rect = patches.Rectangle((startX,startY),endX,endY,linewidth=4,edgecolor='r',facecolor='none')
                #creating the bounding box using the 2 points and displacments we got earlier
    ax.add_patch(rect) 
    
      #adding the bounding box to the figure we plotted earlier
    if(sizeX>0):
          return image[startX:pointsX[sizeX-1],startY:pointsY[sizeY-1]]  
    else:
          return None


# =============================================================================
# this was used to see effects of different filters on both images of rust and not rust
# to see if a certain filter could be applied to tell them appart right away
# =============================================================================
def compare(Rpath,Npath):
    i=0
    for idx in range(len(Rpath)):
       if(idx>500):
        Rimg=Rpath[idx]
        Nimg=Npath[idx]
        i+=1
        Rframe = cv2.imread(Rimg)
        Nframe = cv2.imread(Nimg)
        Rframe= cv2.resize(Rframe, dsize=(250, 200))
        Nframe= cv2.resize(Nframe, dsize=(250, 200))
        
        _,mask=cv2.threshold(Rframe,200,255,cv2.THRESH_TOZERO)
        edges = cv2.Canny(Rframe,100,200)
        cv2.imshow('Rframe',Rframe)
        cv2.imshow('Nframe',edges)
        if cv2.waitKey(0)  & 0xFF == ord('s'): 
              cv2.destroyAllWindows()
        if cv2.waitKey(0)  & 0xFF == ord('q'): #QUIT
              cv2.destroyAllWindows()
              return
    cv2.destroyAllWindows()            
       
#img=drawBox('noRust/4 100.jpg')
#img=drawBox('Rust/M6 55.jpg')
#compare(glob.glob("dataset/Rust/*"),glob.glob("dataset/Rust/*"))
#cv2.destroyAllWindows()


# =============================================================================
# this algorithm was created to cut the image into multiple images of the same size
# and classify each one using both models
# =============================================================================
def cookieCutter(img,plot=False):    
    print(img.shape)    
    i=0
    images=[]
    coordinates=[]
    while(i<imgSize):
        j=0
        while(j<imgSize):
            i2=i+224
            j2=j+224
            image=img[i:i2,j:j2]
            rust=filterRust(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if(plot):
                plt.figure()
                plt.xlabel(rust)
                plt.imshow(image)
            image= cv2.resize(image, dsize=(224,224))
            images.append(image)
            coordinates.append( (i,j) )
            j+=224
        i+=224
    return images,coordinates 
#we return the images and the x,y coordinates of each image for boundingBoxes drawing


import tensorflow as tf

model = tf.keras.models.load_model('model.h5')

img= cv2.imread('test data/1.jpg')
imgSize=224*10 #we resize the image by a multiple of 224 to be able to cut it into n 224x224 images
img= cv2.resize(img,dsize=(imgSize,imgSize))
images ,coordinates=cookieCutter(img,False)
images=np.asarray(images)
predictions=model.predict(images)
predictions=np.argmax(predictions, axis=1)
plot=False
fig,ax = plt.subplots(1) #plotting fig and ax to use the figure to draw the bounding box
ax.imshow(img)   
   
for idx,image in enumerate(images):
   p=predictions[idx]    
   if(p==1):
       x=coordinates[idx][0]
       print(x)
       y= coordinates[idx][1]
       print(y)
       print('----------------')
       rect = patches.Rectangle((x,y),x+224,y+224,linewidth=4,edgecolor='r',facecolor='none')
       ax.add_patch(rect) 

   if(plot):
       plt.figure()
       plt.xlabel(p)
       plt.imshow(image)

plt.figure()
plt.imshow(img)