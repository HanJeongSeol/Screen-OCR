from PIL import Image
import numpy as np
import pytesseract


filename = 'step_4_binary.png'
# config = ('-l kor+eng')
config = ('-l kor+eng --oem 3 --psm 11')
img1 = np.array(Image.open(filename))
text = pytesseract.image_to_string(img1, config=config)
print(text)