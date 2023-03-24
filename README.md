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

## Ideas

- Plot a facet grid of scatterplots for stack/reach vs other variables of a certain class of bikes (e.g. Mountain).
- Plot the median head tube angle of a certain class of bikes (e.g. > 140 mm rear travel MTBs) as a line chart over the years.
- Plot histograms of some geometry values for a certain class of bikes (e.g. <= 130 mm rear travel MTBs) over the years.
- Manufacturer sizing is very arbitrary. Develop a model for sizing based on variables stack and reach. Find a relationship using a scatterplot and some regression model
- Try to predict the category of a bike given only a limited set of geometry values.
- Try to predict the model year given only a limited set of geometry values.
- Try to predict the suspension travel given only a limited set of geometry values.

## Errata

The API currently has no category for electric bikes. It has a variable `has_motor` but it is always false. This is probably a bug in the API or not recorded in the database (yet).  
I have included it in the data set as `Motorized` for future-proofing but you can safely drop it for now.
