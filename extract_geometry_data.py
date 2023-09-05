#!/usr/bin/python

# About:    Scraping Bicycle Geometry Data from geometrics.mtb-news.de
# Author:   Dorian Prill
# Date:     2023-03-22
# License:  MIT

import requests
import json
from time import sleep
from bs4 import BeautifulSoup
import polars as pl

entry_url = 'https://geometrics.mtb-news.de/bikes'
# call api directly e.g. https://geometrics.mtb-news.de/api/bikes?variants=4453,4454,4455,4456,4457,4458
# (easier than waiting for xhr to finish)
bike_api_url = 'https://geometrics.mtb-news.de/api/bikes?variants='
# bikes are nested in lists named "mtbnews-geometry__bike-list" (0-9, A-Z) under the entry_url
target_class_list = 'mtbnews-geometry__bike-list'

savename = './data/geometrics.mtb-news.de'

# the desired columns
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

dtypes = [
    pl.Utf8, 
    pl.Utf8, 
    pl.Utf8, 
    pl.Int32, 
    pl.Utf8, 
    pl.Boolean, 
    pl.Utf8, 
    pl.Utf8, 
    pl.Utf8, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32, 
    pl.Float32
] 

# create empty entry dict
values = [[] for name in columns]
data = dict(zip(columns, values))

# create shema ziplist
schema = list(zip(columns, dtypes))

# translate categories to english
category_map = {
    'Mountainbike':'Mountain',
    'Rennrad':'Road',
    'Gravel-Bike/CycloCross-Bike':'Gravel/CX',
    'Sonstiges':'Other', # rare
}


### GO SCRAPE ###

# Get the page
try: 
    page = requests.get(entry_url)
except Exception as e:
    print(f'Could not fetch {entry_url} because of {e}')
    exit(1)

soup = BeautifulSoup(page.content, 'html.parser')

# select the bike manufacturer starting letter sublists (0-9, A-Z)
sublists = soup.find_all('ul', attrs={'class':target_class_list})




# follow links to individual bikes (default tab on load lists all bike categories)
for ul in sublists:
    # print(ul.find_all('li'))
    # for all bike entries in the sublists
    for li in ul.find_all('li'):

        # experiment with rate limiting, 0.2 was too fast
        sleep(0.3)

        # follow href to individual bike page 
        bikeurl = li.find('a').get('href')
        bikepage = requests.get(bikeurl)
        bikesoup = BeautifulSoup(bikepage.content, 'html.parser')
        
        # find detail table link from button with text 'Diese Geometrien untereinander vergleichen'
        # currently there is only one btn-primary on the page, but this might change in the future
        button = bikesoup.find('a', attrs={'class':'btn btn-primary'})

        if button is None or ' '.join(button.get_text().split()) != 'Diese Geometrien untereinander vergleichen':
            print('No button for detail table found - skipping')
            continue

        table_url = button.get('href')
        
        # and disassemble it to get the bike IDs for the API call
        # (we're going to call the detail table api directly, as it's easier than waiting for XHR to finish with bs4/selenium)
        api_variants = table_url.split('/')[-1].split('@')[0].replace('_', ',')
        api_call = f'{bike_api_url}{api_variants}'
        biketable = requests.get(api_call)

        print(
            f'Bike URL:\t{bikeurl}\n'
            f'Table URL:\t{table_url}\n'
            f'Assembled API:\t{api_call}\n'
        )

        # get the dict from json 
        # if the bike is listed but has no data yet/no variants exist -> loop will be skipped
        # bikes that do have data but are not yet marked as published or are not 
        # reviewed, marked (a::after is GESUCHT or ENTWURF), are not included
        model_variants = []
        try:
            model_variants = biketable.json()['data']
        except Exception as e:
            print(f'No variants found for {bikeurl} because of {e} - skipping')
            continue
        
        for entry in model_variants:

            # prints full json for every variant - verbose!
            #print(f'JSON:\n{json.dumps(entry, indent=2)}')

            data['URL'].append(entry['model']['url'])
            data['Brand'].append(entry['model']['brand']['name'])
            data['Model'].append(entry['model']['model_name'])
            data['Year'].append(entry['model']['year'])
            data['Category'].append(category_map[entry['model']['type']])
            data['Motorized'].append(entry['model']['has_motor'])
            data['Frame Size'].append(entry['frame_size'])
            data['Frame Config'].append(entry['frame_config'])
            data['Wheel Size'].append(entry['wheelsize'])
            data['Reach'].append(entry['reach'])
            data['Stack'].append(entry['stack'])
            data['STR'].append(entry['stack_to_reach'])
            data['Front Center'].append(entry['front_center'])
            data['Head Tube Angle'].append(entry['head_angle'])
            data['Seat Tube Angle Effective'].append(entry['seat_angle_effective'])
            data['Seat Tube Angle Real'].append(entry['seat_angle_real'])
            data['Top Tube Length'].append(entry['top_tube_length'])
            data['Top Tube Length Horizontal'].append(entry['top_tube_horizontal_length'])
            data['Head Tube Length'].append(entry['head_tube_length'])
            data['Seat Tube Length'].append(entry['seat_tube_length'])
            data['Standover Height'].append(entry['standover_height'])
            data['Chainstay Length'].append(entry['chainstay_length'])
            data['Wheelbase'].append(entry['wheel_base'])
            data['Bottom Bracket Offset'].append(entry['bottom_bracket_offset'])
            data['Bottom Bracket Height'].append(entry['bottom_bracket_height'])
            data['Fork Installation Height'].append(entry['fork_installation_height'])
            data['Fork Offset'].append(entry['fork_offset'])
            data['Fork Trail'].append(entry['fork_trail'])
            data['Suspension Travel (rear)'].append(entry['travel_rear'])
            data['Suspension Travel (front)'].append(entry['travel_front'])



# construct data frame from dict
# we're going to infer the schema from all samples for a start, change this if the database grows
df = pl.DataFrame(data=data, infer_schema_length=len(data['Model']))
#df = pl.DataFrame(data=data, schema=schema) 
print(df.head())
print(df.dtypes)
df.write_csv(savename+'.csv', sep=';')
df.write_ipc(savename+'.arrow', compression='zstd')

