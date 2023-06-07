import cv2
import numpy as np
import pyautogui
import time
import random
import pytesseract


def wait_random():
    wait_time = random.uniform(2, 7)  # Generate a random floating-point number between 2 and 15
    time.sleep(wait_time)  # Pause the execution for the generated wait time


def find_and_click(target_image):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    target = cv2.imread(target_image, 0)
    result = cv2.matchTemplate(screenshot, target, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.9:
        pyautogui.moveTo(max_loc)
        pyautogui.click()
        return True
    return False

def get_mouse_position_after_delay(delay=10):
    print(f"Waiting for {delay} seconds before getting mouse position...")
    time.sleep(delay)
    position = pyautogui.position()
    return position

# Usage
# pos = get_mouse_position_after_delay()
# print(f"The mouse position after 10 seconds delay is {pos}")


# Make sure you update the path below with the actual path of your tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def find_text_on_screen(target_text):
    print("6 sec sleep to find text")
    time.sleep(6)
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    result = pytesseract.image_to_data(screenshot_gray, output_type=pytesseract.Output.DICT)

    for i in range(len(result["text"])):
        if target_text.lower() in result["text"][i].lower():
            x = result["left"][i]
            y = result["top"][i]
            return (x, y)

    return None

# Usage
# pos = find_text_on_screen("New chat")
# if pos:
#     print(f"Position of the target text on screen is {pos}")
# else:
#     print("Target text not found on screen.")

time.sleep(5)



def find_and_click_phrase(word1, word2, near=None):  #word2 is the word closest to the other word.  #near is x and y coordinates so implement it as find_and_click_phrase('New', 'chat', near=(x, y))
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Display the screenshot
    cv2.imshow('Screenshot', screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    data = pytesseract.image_to_data(screenshot_gray, output_type=pytesseract.Output.DICT)
    
    word1_locs = []
    word2_locs = []
    for i in range(len(data['text'])):
        if word1.lower() == data['text'][i].lower():
            word1_locs.append((data['left'][i], data['top'][i]))
        if word2.lower() == data['text'][i].lower():
            word2_locs.append((data['left'][i], data['top'][i]))

    # Print the number of occurrences and their coordinates
    print(f"'{word1}' found {len(word1_locs)} times at {word1_locs}")
    print(f"'{word2}' found {len(word2_locs)} times at {word2_locs}")

    if word1_locs and word2_locs:  # Both words are found
        # If near is specified, find the combination of word1 and word2 that are near each other and also near the specified coordinate
        min_distance = float('inf')
        min_locs = None
        for loc1 in word1_locs:
            for loc2 in word2_locs:
                if abs(loc1[0] - loc2[0]) < 50 and abs(loc1[1] - loc2[1]) < 50:  # The words are near each other
                    if near:  # If near is specified, use the distance from the phrase to near
                        distance = ((near[0] - loc1[0])**2 + (near[1] - loc1[1])**2)**0.5 + ((near[0] - loc2[0])**2 + (near[1] - loc2[1])**2)**0.5
                        if distance < min_distance:
                            min_distance = distance
                            min_locs = (loc1, loc2)
                    else:  # If near is not specified, use the y-coordinate (the higher, the better)
                        if min_locs is None or loc1[1] < min_locs[0][1] or loc2[1] < min_locs[1][1]:
                            min_locs = (loc1, loc2)

        if min_locs:  # Found a suitable combination of words
            center_x = min_locs[1][0] + (min_locs[0][0] - min_locs[1][0]) // 2
            center_y = min_locs[1][1] + (min_locs[0][1] - min_locs[1][1]) // 2
            pyautogui.click(center_x, center_y)
            print(f"Clicked on the phrase '{word1} {word2}' at location ({center_x}, {center_y})")
        else:
            print(f"The words '{word1}' and '{word2}' were found but are not near each other or not near the specified coordinate.")
    else:
        print("Could not find the phrase for some reason")

# find_and_click_phrase("New", "chat")  #This works at clicking the most superior one.

#It will find and click an image.. it requires you to take a screenshot of the smaller image and save it locally so you can include the path. 
def find_and_click_image(target_image_path, threshold=0.8, method=cv2.TM_CCOEFF_NORMED):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    target_image = cv2.imread(target_image_path, 0)

    result = cv2.matchTemplate(screenshot_gray, target_image, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val > threshold:
        match_width = target_image.shape[1]
        match_height = target_image.shape[0]
        match_center_x = max_loc[0] + match_width // 2
        match_center_y = max_loc[1] + match_height // 2

        pyautogui.moveTo(match_center_x, match_center_y)
        pyautogui.click()
        print("Clicked it")
        return True
    else:
        print("Cannot find object")
        return False



#this block is to use to like stories on instagram.
for i in range(50):
    print(i)
    wait_random()
    find_and_click_image(r"C:/Users/johnc/OneDrive/Desktop/John_Script/opencvtracking/chromeautomation/pics/Capture.png", 0.8, cv2.TM_CCOEFF_NORMED)
    wait_random()
    find_and_click_image(r"C:/Users/johnc/OneDrive/Desktop/John_Script/opencvtracking/chromeautomation/pics/nextstory.png", 0.8, cv2.TM_CCOEFF_NORMED)
