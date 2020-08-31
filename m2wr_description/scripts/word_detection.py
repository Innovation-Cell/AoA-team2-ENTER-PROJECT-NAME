import cv2 
import pytesseract 
  
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
  

def word(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
    contours = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    im2 = img.copy() 
    texts = [] 
    for cnt in contours:
        try:
            x, y, w, h = cv2.boundingRect(cnt) 
        
            cropped = im2[y:y + h, x:x + w] 
            
            text = pytesseract.image_to_string(cropped).lower()

            texts.append(text)
            if "umic" in text:
		print(texts)
                return 1 
        except:
            pass

    print(texts)
    return 0
img = cv2.imread("umic.png")
x = word(img)
if x == 1:
    print("UMIC found")
