# =============================================================================
# 
#      After collecting the data and before training the model we wrote this piece of code to get
#      an idea of the human level performance in classifying our dataset
#      so the code would shuffle images from our dataset show N number of random images
#      and shows the accuracy, false negatives/positives and true negatives/positives
#     
# =============================================================================

import cv2
import glob
import random
import numpy as np


def shuffle(listOfImages):
    print('shuffling all images')
    shuffeled=[]
    sizeOfList=len(listOfImages)
    while(sizeOfList>0):
        randomImage=random.randint(0, (sizeOfList-1) )
        shuffeled.append(listOfImages.pop(randomImage))
        sizeOfList-=1
    return shuffeled    


# =============================================================================
#  the following function reads all the images from their directory and returns a shuffled list
#  of all images in random ordering
# =============================================================================
def read():
    print('reading images now')

    pathRust  = glob.glob('dataset/rust/*')
    pathNoRust= glob.glob('dataset/notRust/*')

    allImages=[]
    n=len(pathRust)+len(pathNoRust)
    i=0
    p=-1
    for img in pathRust:
        i+1
        image = cv2.imread(img)
        allImages.append([image,1])
        percentage=int(((i/n * 100)))
        if(p!=percentage):
            print('percentage of images read is '+ str(percentage)+"%")
            p=percentage
    print('rust images loaded')
    for img in pathNoRust:
        i+1
        image = cv2.imread(img)
        allImages.append([image,0])
        percentage=int(((i/n * 100)))
        if(p!=percentage):
            print('percentage of images read is '+ str(percentage)+"%")
            p=percentage

    print('Not rust images loaded')
        
    return shuffle(allImages)


allImages=read()
allImages=np.asarray(allImages)
print(allImages.shape)

print('how many entries do you want to test')
x= eval(input())

i=0
correctRust=0
correctNoRust=0
wrongRust=0
wrongNoRust=0

# =============================================================================
#     this part of the code views X number of images and lets the user choose for each image
#     whether it was a rust image or a not rust image then it evaluates the user   
# =============================================================================
for entry in allImages:
    i+=1
    image=entry[0]
    rust= entry[1]==1
    cv2.imshow('image',image)
    if( cv2.waitKey(0) & 0xFF==ord('q')): #QUIT
        break
    if( cv2.waitKey(0) & 0xFF==ord('r')): #RUST
        if(rust):
            correctRust+=1
        else:
            wrongRust+=1
    if( cv2.waitKey(0) & 0xFF==ord('n')): #NO RUST
        if(rust):
            wrongNoRust+=1
        else:
            correctNoRust+=1
            
    cv2.destroyAllWindows()
    
    if(x==i):
        break    
print('correctly classified as Rust '+ str(correctRust))
print('correctly classified as Not Rust '+ str(correctNoRust))

print('wrongfuly classified as Rust '+ str(wrongRust))
print('wrongfuly classified as Not Rust '+ str(wrongNoRust))

percentage= (correctRust+correctNoRust)/x * 100
print("accuracy = " + str(percentage) + "%")
