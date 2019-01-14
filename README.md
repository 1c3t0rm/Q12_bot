# Q12_Bot
![License: MIT][ico-license]

This software must be use only with educational purposes, any other use with no educational intent is at your own risk. This Python script are not developed with any intention of damaging [Q12][link-q12]. I do not encourage anyone to use this during a live game and this is purely for educational purposes.

This bot is an inspired version of [sushant10's][link-sush] HQ_Bot

## TO-DO list
- [ ] Make a requirements file
- [ ] Real multithreading URLs.
- [ ] Simplify questions.
- [ ] Processing of JSON file.
- [ ] Implement wikipedia library instead of googlesearch.
- [ ] Collect Screenshots and log of answers.


## Packages Used


Use Python 3 and ADB. In particular the packages/libraries used are...

* Google-Search-API - Google searching
* Requests - Requests library
* beautifulsoup4 - Parse google searches/html
* lxml - Beautifulsoup parser
* pytesseract - Google's free/open source OCR (requires seperate installtion)
* opencv2 - Image maniplulation
* Time and Os libraries
* Parallel and delayed from joblib

## Usage

I recommend before any use to change values of coordinates according to your mobile screenshot in functions `parse_question_lines()` and `parse_options()`. With the help of [Image-Map][image-map] you can do this. 

Remember that OpenCV doesn't have the same conversion as Image-Map

```
OpenCV:     gray[y:y+h,x:x+w]
# Box

Image-Map:  coords="129,1037,923,1115" 
# Uppper-left edge and Downer-Right edge
```

Make sure all packages above are installed.**The code expects the phone to be plugged in Debugging mode. (Only Android supported)** 

```bash
$ git clone https://github.com/1c3t0rm/Q12_bot
$ cd Q12_bot
$ pip3 install -r requirements.txt (NOT DONE YET)
$ python3 parallel_q12_bot.py
Press s to screenshot or q to quit:
s
```
## Screenshots

![Sample Usage](/Screens/sample.png)
![Sample Image-Map Usage](/Screens/sample_image_map.png)

## Credits

- [1c3t0rm][link-author]

- For the idea: [Sushant10][link-idea-author]


## Useful links

- [Google-Search-API][link-gapi]
- [Tesseract][link-tesseract]
- [ADB][link-adb]

## License

The MIT License (MIT)

[ico-license]: https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square
[link-sush]: https://github.com/sushant10/HQ_Bot
[link-idea-author]: https://github.com/sushant10
[link-author]: https://github.com/1c3t0rm
[link-gapi]: https://github.com/abenassi/Google-Search-API
[link-tesseract]: https://github.com/tesseract-ocr/tesseract/wiki
[link-adb]: https://developer.android.com/studio/command-line/adb?hl=es-419
[link-q12]: http://q12.live
[screenshots]: /Screens
[sample-use]: /Screens/sample.png
[image-map]: https://www.image-map.net/