# =============================================================================
# 
#     Since the dataset was collected capturing images, and videos of rusted and not Rusted pipes by hand
#     this algorithm was written to be able to classify images and frames of the vidoes into their own
#     directory (rust / notRust)
#
# =============================================================================
import cv2
import glob
# =============================================================================
# 
#     the following method runs on a folder of image and it lets you choose whether the image is a rust 
#     image or a notRust image then it puts each in its respective folder
#     
# =============================================================================
def ImageRead(path):
        i=1 # rust counter
        j=1 #not Rust counter
        for img in path:
            frame = cv2.imread(img)
            frame= cv2.resize(frame, dsize=(224, 224))
            cv2.imshow('frame',frame)
            if cv2.waitKey(0)  & 0xFF == ord('r'): #Rust
                    print("rust image")
                    cv2.imwrite('dataset/rust/R '+str(i)+'.jpg',frame) #CHANGE NAME OF IMAGE TO NOT OVERRIDE
                    i+=1
                    cv2.destroyAllWindows()
            if cv2.waitKey(0)  & 0xFF == ord('n'): #NoRust
                    print("no rust image")
                    cv2.imwrite('noRust/N '+str(j)+'.jpg',frame) #CHANGE NAME OF IMAGE TO NOT OVERRIDE
                    j+=1 
                    cv2.destroyAllWindows()
            if cv2.waitKey(0)  & 0xFF == ord('s'): #Skip
                    print("skipped")
                    cv2.destroyAllWindows()
# =============================================================================
#             
#    the following function was used to read a given video and let you choose for every frame whether it
#    was a frame containing rust or no rust image
#    we added a skip button as we did't wanna have much repeated frames  
#     
# =============================================================================

def videoRead(path):
        cap = cv2.VideoCapture(path)
        i=1 # Rust counter
        j=1 #No Rust counter
        
        if (cap.isOpened()== False): 
          print("Error opening video stream or file")
        
        while(cap.isOpened()):
          ret, frame = cap.read()
          if ret == True:
            frame= cv2.resize(frame, dsize=(224, 224))
            cv2.imshow('frame',frame)
            
            if cv2.waitKey(0) & 0xFF == ord('f'): #skip
                    pass
            if cv2.waitKey(0)  & 0xFF == ord('r'): #Rust
                    print("rust image")
                    cv2.imwrite('dataset/Rust/R '+str(i)+'.jpg',frame) #CHANGE NAME OF IMAGE TO NOT OVERRIDE
                    i+=1
            if cv2.waitKey(0) & 0xFF == ord('n'): #No rust
                    print("no rust image")
                    cv2.imwrite('dataset/noRust/N '+str(j)+'.jpg',frame) #CHANGE NAME OF IMAGE TO NOT OVERRIDE
                    j+=1
            if cv2.waitKey(0) & 0xFF == ord('q'):
                cap.release()  
                cv2.destroyAllWindows()
                return
          else: 
            break
         
        cap.release()
        cv2.destroyAllWindows()
    
#ImageRead(glob.glob("newDataFolder/*.jpg"))
#videoRead("newDataFolder/testVid.mp4")
            
    