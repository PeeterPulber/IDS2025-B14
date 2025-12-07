# History of the popularity of heavy metal subgenres in Estonia, Finland and Latvia
### Author: Uku Viispert

The goal of this project was to find patterns in the data about Estonian heavy metal bands included in the “Encyclopaedia Metallum” online metal archive, focusing on the bands’ genres and years of activity. This was done to get an overview of the historical “landscape” of the local metal scene and how it has shifted over the years. Another goal was to compare the trends of the Estonian metal scene with those of some other nearby countries. Namely, Latvia and Finland were chosen as these countries due to geographical proximity and cultural and historical ties to Estonia.

#### This repository includes:
* `scrape.py`

    This Python script was used to scrape data from [Encyclopaedia Metallum](https://www.metal-archives.com/). 
* `cleaner.py`
    
    This was used to clean the data gathered by the scraping script. 
* `plotting.ipynb`

    This jupyter notebook file contains the code used for visualising the data.
* Output files of the scraping script, which the cleaning script uses as input.
  * `bandsEE.jsonl`
  * `bandsLV.jsonl`
  * `bandsFI.jsonl`

* Output files of the cleaning script, used as input for plotting.
  * `bandsEE.csv`
  * `bandsLV.csv`
  * `bandsFI.csv`

    
#### How to replicate the analysis
(Steps 1 and 2 can be skipped as these purpose of these is to generate the data files, which are already present in this repository)
0. Install required packages 
1. Use `scrape.py` 3 times to scrape each of the 3 Encyclopaedia Metallum country pages (
   1. https://www.metal-archives.com/lists/EE,
   2. https://www.metal-archives.com/lists/LV, 
   3. https://www.metal-archives.com/lists/FI)
    
    Each time the input link and the output file must be specified in scrape.py (variables `url` and `filename`). The output file must be in jsonl format.
    
    Note: Scraping might take a long time for countries from which there are many bands. While scraping, the urls of pages from which data has already been gathered are saved in the output file, so if the scraping script is stopped and rerun again later, the pages already visited won't be scraped from again to save time.  
2. Run `cleaner.py` once. The names of the files to clean are to be written in the `filenames`array.
3. Use `plotting.ipynb` to plot the data from the cleaned csv files.