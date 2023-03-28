# Bicycle Geometry Data Set

This repository contains the code used to extract a bicycle geometry data set from the `geometrics.mtb-news.de` website. An example dump is available as `.csv` and `.arrow` files in the `data` directory. I am updating the data dump from time to time but if you want more recent data, scrape it yourself with the povided script.

## Setup & Run

Install Python 3.11 and pip. Make sure `python` points to version 3.11, otherwise use the appropriate command.

Then run the following commands:

```Bash
python -m venv env
source env/bin/activate 
# Windows: env\Scripts\activate.bat
pip install -r requirements.txt
python extract_geometry_data.py
```

This will create a virtual environment, install the required packages and extract the data set. The data set will be saved in the `data` directory.  

## Data Set

The data set contains the following 30 columns:

```Python
columns = [
    'URL',
    'Brand',
    'Model',
    'Year',
    'Category',
    'Motorized',
    'Frame Size',
    'Frame Config',
    'Wheel Size',
    'Reach',
    'Stack',
    'STR',
    'Front Center',
    'Head Tube Angle',
    'Seat Tube Angle Effective',
    'Seat Tube Angle Real',
    'Top Tube Length',
    'Top Tube Length Horizontal',
    'Head Tube Length',
    'Seat Tube Length',
    'Standover Height',
    'Chainstay Length',
    'Wheelbase',
    'Bottom Bracket Offset',
    'Bottom Bracket Height',
    'Fork Installation Height',
    'Fork Offset',
    'Fork Trail',
    'Suspension Travel (rear)',
    'Suspension Travel (front)',
]
```

Multiple variants may be recorded for each model. Variants depend mostly on `Frame Size`, `Frame Config`, `Wheel Size`, `Suspension Travel (rear)`, `Suspension Travel (front)`.

Most of the columns are self-explanatory if you are into bikes. There may be many `null`s in the numeric columns since different manfuacturers may use a slightly different set of values and some values are normally only stated for a certain category of bikes.  
Some of these values can be computed with simple geometry.

The `URL` column contains the URL of the page from which the data was extracted. The last number in the URL is the database ID of the bike.

## Data Cleaning

Some geometry values are not as significant or commonly stated as others. It is an easy exercise to find out which, even if you are not familiar with bikes. 
Those columns can likely be dropped in most cases. 
The dataset has a handful of samples with extreme values in some columns, but not all of them are true outliers! Some of them are kids bikes and some of them are from faulty database entries. 

I will ususally report any errors I find on the website. But it is a good exercise to find them and then manually check if it is indeed an outlier or not. 

For bikes with kinked seat tubes, only the effective seat tube angle makes sense. For bikes with a straight seat tube, both effective and real angles are the same. You can use this to impute values for `Seat Tube Angle Effective` where it is missing but the `Seat Tube Angle Real` is given.

## Ideas for Visualization and Modeling

- Create a paired scatter plot grid (e.g. 4x4) for the columns with the most data points, color them by category and see which pairs separate the clusters best.
- Plot mean/median of a set of geometry values for category `Mountain` (most samples) as a line chart over the years.
- Plot faceted histograms of e.g. `Head Tube Angle` for each category of bike.
- Manufacturer sizing is very arbitrary. Develop a model for sizing based on variables stack and reach. Find a relationship using a scatterplot and some regression model
- Try to predict the category of a bike given only a limited set of geometry values.
- Try to predict the model year given only a limited set of geometry values and category.
- Try to predict the suspension travel given only a limited set of geometry values.

## Errata

The API currently has no category for electric bikes. It has a variable `has_motor` but it is always `False`. This is probably a bug in the API or not recorded in the database (yet).  
I have included it in the data set as `Motorized` for future-proofing but you can safely drop it for now.
