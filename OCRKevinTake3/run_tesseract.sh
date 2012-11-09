#!/bin/bash

x=/afs/ir.stanford.edu/users/k/j/kjmiller

export TESSDATA_PREFIX=$x/cgi-bin/OCRplus/OCRKevinTake3/tesseract-ocr/tesseract-ocr
$x/local/bin/tesseract $1 $2 -l $3 $x/cgi-bin/OCRplus/OCRKevinTake3/tesseract-ocr/tessdata/configs/hocr
