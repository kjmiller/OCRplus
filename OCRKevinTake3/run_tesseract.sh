#!/bin/bash

x=/home/ubuntu

export TESSDATA_PREFIX=$x/OCRplus/OCRKevinTake3/tesseract-ocr
tesseract $1 $2 -l $3 $x/OCRplus/OCRKevinTake3/tesseract-ocr/tessdata/configs/hocr
