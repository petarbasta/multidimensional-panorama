import cv2
import sys
import imutils

#parse top level pictures
topInput = []
topInput.append(sys.argv[1])
topInput.append(sys.argv[2])

#parse bottom level pictures
bottomInput = []
bottomInput.append(sys.argv[3])
bottomInput.append(sys.argv[4])

#stitch together top level
imgs = []
for currentImage in topInput:
    img = cv2.imread(currentImage)
    if img is None:
        print("Can't read image " + currentImage)
        sys.exit(-1)
    imgs.append(img)

stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
status, topStitched = stitcher.stitch(imgs)

if status != cv2.Stitcher_OK:
    print("Can't stitch images, not enough overlap!")
    sys.exit(-1)

#stitch together bottom level
imgs = []
for currentImage in bottomInput:
    img = cv2.imread(currentImage)
    if img is None:
        print("Can't read image " + currentImage)
        sys.exit(-1)
    imgs.append(img)

stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
status, bottomStitched = stitcher.stitch(imgs)

if status != cv2.Stitcher_OK:
    print("Can't stitch images, not enough overlap!")
    sys.exit(-1)

#rotate top and bottom layers to align axis
topStitchRotated = imutils.rotate_bound(topStitched, 270)
bottomStitchRotated = imutils.rotate_bound(bottomStitched, 270)

#stitch together whole picture
imgs = []
imgs.append(topStitchRotated)
imgs.append(bottomStitchRotated)

stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
status, wholePictureRotated = stitcher.stitch(imgs)

if status != cv2.Stitcher_OK:
    print("Can't stitch images, not enough overlap!")
    sys.exit(-1)

#rotate picture back to normal
wholePicture = imutils.rotate_bound(wholePictureRotated, 90)

#save all pictures
cv2.imwrite("bottomStitched.jpg", bottomStitched)
cv2.imwrite("bottomStitchRotated.jpg", bottomStitchRotated)
cv2.imwrite("topStitched.jpg", topStitched)
cv2.imwrite("topStitchRotated.jpg", topStitchRotated)
cv2.imwrite("wholePicture.jpg", wholePicture)
cv2.imwrite("wholePictureRotated.jpg", wholePictureRotated)