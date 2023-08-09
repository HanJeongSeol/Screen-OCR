import numpy as np
import cv2
import easyocr
def test1(img) : 
    re = cv2.resize(img, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_CUBIC)
    blurred = cv2.GaussianBlur(re, (9,9), 0)
    sharpened = cv2.addWeighted(re, 1.7, blurred, -0.6, 0)
    return sharpened

def test2(img) : 
    re = cv2.resize(img, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_LANCZOS4)
    blurred = cv2.GaussianBlur(re, (9,9), 0)
    sharpened = cv2.addWeighted(re, 1.7, blurred, -0.6, 0)
    return sharpened

def test3(img) :
    re = cv2.resize(img, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_LANCZOS4)
    return re

def test4(img) : 
    re = cv2.resize(img, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_LANCZOS4)
    gray = cv2.cvtColor(re, cv2.COLOR_BGR2GRAY)
    return gray

# img = cv2.imread("talk1.png")
img = cv2.imread("music.png")
cv2.imwrite("step_1_original.png", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("step_2_gray.png", gray)
   
 # 2. Histogram Equalization (Optional)
# gray = cv2.equalizeHist(gray)
# cv2.imwrite("step_2_1_resized.png", gray)

resized = cv2.resize(gray, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_CUBIC)
# cv2.imwrite("step_3_resized.png", resized)

binary = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                               cv2.THRESH_BINARY_INV, 15, 1)
cv2.imwrite("step_4_binary.png", binary)

kernel = np.ones((1,1), np.uint8)
dilated = cv2.dilate(binary, kernel, iterations=1)

cv2.imwrite("step_5_dilated.png", dilated)

re = cv2.resize(img,None, fx=1.3, fy=1.3, interpolation=cv2.INTER_CUBIC)

# 기존 색 선명도 설정
blurred = cv2.GaussianBlur(re, (5,5), 0)

# # # Enhance sharpness using Unsharp Masking
sharpened = cv2.addWeighted(re, 1.5, blurred, -0.5, 0)

ttest1 = test1(img)
ttest2 = test2(img)
ttest3 = test3(img)
ttest4 = test4(img)
cv2.imwrite("final.png",ttest3)

reader = easyocr.Reader(['ko', 'en'], gpu=False)
text = reader.readtext("final.png", detail=0)
print(text)