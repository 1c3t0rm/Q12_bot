# answering bot for q12
from bs4 import BeautifulSoup
from google import google
import requests

import pytesseract
import cv2

from halo import Halo
import time,os 

from joblib import Parallel, delayed

# for terminal colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# take screenshot of question
def screen_grab(to_save):
    os.system("adb shell screencap -p /sdcard/screen.png;\
    adb pull /sdcard/screen.png;\
    adb shell rm /sdcard/screen.png")

# get OCR text //questions and options
def parse_question_lines():
    global original, gray
    original = cv2.imread("screen.png", cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    im_line1 = gray[1030:1030+(1030-950), 71:71+(1021-71)]
    im_line2 = gray[1109:1109+(1109-1050), 132:132+(952-132)]
    im_line3 = gray[1165:1165+(1165-1099), 72:72+(1022-72)]
    im_line4 = gray[1222:1222+(1222-1140), 78:78+(1028-78)]

    quest_lines = [im_line1, im_line2, im_line3, im_line4]
    question = ""

    #DEBUG
    #for o in opts:
    #   cv2.imshow("Output", o)
    #   if cv2.waitKey(0):
    #           cv2.destroyAllWindows()

    for line in quest_lines:
        gray_quest = cv2.threshold(
            line, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        question = question + " " + \
            pytesseract.image_to_string(gray_quest, lang="spa") 

    return question.lower()


def parse_options():
    imopt1 = gray[1376:1376+(1481-1376), 134:134+(938-134)]
    imopt2 = gray[1544:1544+(1662-1544), 140:140+(932-140)]
    imopt3 = gray[1720:1720+(1827-1720), 136:136+(934-136)]

    opts = [imopt1, imopt2, imopt3]

    #DEBUG
    #for o in opts:
    #   cv2.imshow("Output", o)
    #   if cv2.waitKey(0):
    #           cv2.destroyAllWindows()

    options = list()

    for o in opts:
        gray_imopt = cv2.threshold(
            o, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        options.append(pytesseract.image_to_string(gray_imopt, lang="spa"))

    return options


def parse_question():
    screenshot_file = "Screens/ocr_"+str(time.time())+".png"
    screen_grab(screenshot_file)

    question = parse_question_lines()
    options = parse_options()

    return question, options

# get web page
def get_page(link):
    try:
        if link.find('mailto') != -1:
            return ''
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win7; x64)'}
        req = requests.get(link, headers)
        return req.text
    except (requests.URLError, requests.HTTPError, ValueError) as e:
        return ''

# split the string
def split_string(source):
    splitlist = ",!-.;/?@ ¿#"
    output = []
    atsplit = True
    for char in source:
        if char in splitlist:
            atsplit = True
        else:
            if atsplit:
                output.append(char)
                atsplit = False
            else:
                output[-1] = output[-1] + char
    return output

# answer by combining two words
def parallel_smart(el):
    if g_content.count(el[0]+" "+el[1]) != 0:
        return 1000
    else:
        return 0

def multiple_coincidence(content, qwords):  # PARALLEL IMPLEMENTATION
    global g_content
    g_content = content

    zipped = zip(qwords, qwords[1:])
    points = Parallel(n_jobs=-1)(delayed(parallel_smart)(el) for el in zipped)

    return sum(points)

def parallel_for(o):
    original = o.lower()
    o += ' wiki'

    # get google search results for option + 'wiki'
    search_wiki = google.search(o, 1)
    link = search_wiki[0].link
    content = get_page(link)    #Multiprocessing is not multithreading.
    soup = BeautifulSoup(content, "lxml")
    page = soup.get_text().lower()

    temp = 0

    # Count is faster than collections.counter in this case.
    for word in words:
        temp = temp + page.count(word)

    temp += multiple_coincidence(page, words)

    print(original, " ", temp)

    return [original, temp]


def identity(x):
    return x


def my_max(sequence, key_func=None):
    if not sequence:
        raise ValueError('empty sequence')

    if not key_func:
        key_func = identity

    maximum = sequence[0]

    for item in sequence:
        # Ask the key func which property to compare
        if key_func(item) > key_func(maximum):
            maximum = item

    return maximum

# use google to get wiki page
def google_wiki(sim_ques, options):
    global words

    best_opt = ""
    points = list()

    words = split_string(sim_ques)

    tupla = Parallel(n_jobs=-1)(delayed(parallel_for)(o) for o in options)

    best_opt = my_max(tupla, key_func=lambda x: x[1])

    for p in tupla:
        points.append(p[1])

    return points, best_opt[0]


# return points for live game // by screenshot
def get_points_live():
    question, options = parse_question()

    simq = question
    points = []

    best_opt = ""
    m = 1
    points, best_opt = google_wiki(simq, options)

    print("\n" + bcolors.UNDERLINE + question + bcolors.ENDC + "\n")

    for point, option in zip(points, options):
        if best_opt == option.lower():
            option = bcolors.OKGREEN+option+bcolors.ENDC
        print(option + " { points: " + bcolors.BOLD +
              str(point*m) + bcolors.ENDC + " }\n")


# menu// main func
if __name__ == "__main__":
    logo = '''
    @@@@@@@@@@@@((((((((((((((&@@@@@@@@@@@@@@@@                
    @@@@@@@@#(((((((((((((((((((((@@@@@@@%#%@@@                
    @@@@@@((((((((((((((((((((((((((##########&@@@@@@@@@@@@@ 
    @@@@((((((((((*,,,,,,,,,((((((((((############@@@@@@@@@@@@ 
    @@@((((((((,,,,,,,,,,,,,,,,((((((((#@@@@@######@@@@@@@@@@@ 
    @@(((((((,,,,,,,,,,,,,,,,,,,,(((((((%@@@@@######@@@@@@@@@@ 
    @(((((((,,,,,,,,,,,,,,,,,,,,,,(((((((@@@@@@#####@@@@@@@@@@ 
    @((((((,,,,,,,,,,,,,,,,,,,,,,,,((((((#@@@@@#####@@@@@@@@@@ 
    #((((((,,,,,,,,,,,,,##/,,,,,,,,(((((((@@@@@#####@@@@####@@ 
    #((((((,,,,,,,,,,,######/,,,,,,(((((((@@@@@#####@@######## 
    @((((((,,,,,,,,,##########/,,,,((((((#@@@@@#############@@ 
    @(((((((,,,,,,,,############/,(((((((@@@@@@###########@@@@ 
    @@(((((((,,,,,,,,,###/#######(((((((#@@@@@@#########@@@@@@ 
    @@@((((((((,,,,,,,,,,,,*####(((((((#@@@@@@@#######@@@@@@@@ 
    @@@@(((((((((*,,,,,,,,,,,(((((((((#@@@@@@@@#####@@@@@@@@@@ 
    @@@@@(((((((((((((((((((((((((((((((#@@@@@@###@@@@@@@@@@@@ 
          @@((((((((((((((((((((((((((((((#@@@@#@              
          @@@@@((((((((((((((((@@@@((((((((((@@                
          @@@@@@@@@@@@@@@@@@@@@@@@@@@(((((((@@@                
          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@(((@@@@@                        
    '''
    print(logo)
    while(1):
        keypressed = input(
            bcolors.WARNING + 'Press s to screenshot or q to quit:\n' + bcolors.ENDC)
        if keypressed == 's':
            start = time.time()
            get_points_live()
            end = time.time()
            print("\nTook", end - start, " seconds.")
        elif keypressed == 'q':
            break
        else:
            print(bcolors.FAIL + "\nUnknown input" + bcolors.ENDC)
