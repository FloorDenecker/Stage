# -*- coding: utf-8 -*-

'''
    __  ___      __    _ __     ____  _   _____
   /  |/  /___  / /_  (_) /__  / __ \/ | / /   |
  / /|_/ / __ \/ __ \/ / / _ \/ / / /  |/ / /| |
 / /  / / /_/ / /_/ / / /  __/ /_/ / /|  / ___ |
/_/  /_/\____/_.___/_/_/\___/_____/_/ |_/_/  |_|

ANNOTATE DATA FRAME WITH LOCATION DATA

-- Coded by Wouter Durnez
-- mailto:Wouter.Durnez@UGent.be
'''

import sys
import time

import geopy
import numpy as np
import pandas as pd
from progress.bar import ShadyBar

import mobdna_helper

# Dashboard variables
log = 0
zzz = .5

# Needed for geolocation
geolocator = geopy.Nominatim(timeout=10, scheme='http')


def get_location(la, lo, loc_dict: dict):
    """Get location variables based on latitude and longitude, while
    taking previous findings into account (no double look-ups)."""

    # If there are valid coordinates
    if la != 0 and lo != 0:

        # Did we look these up before?
        if (la, lo) in loc_dict:
            if log is 1:
                print("Coordinates already checked :) ")
            location = loc_dict[(la, lo)]

        # If not, look them up, then store them so we don't do double work
        else:
            try:
                location = geolocator.reverse(str(la) + ", " + str(lo), timeout=None)
                loc_dict[(la, lo)] = location
                time.sleep(zzz)
            except (geopy.exc.GeocoderTimedOut, geopy.exc.GeocoderServiceError) as e:
                if log is 1:
                    print("Error: geocode failed on input (%s, %s)" % (la, lo), e)
                location = np.nan

    else:
        location = np.nan

    return location


def update_df_with_location(df_old, loc_dict: dict) -> (pd.DataFrame, dict):
    """Update dataframes with columns (country_code, zip, state, city, village, road)"""

    # Progress bar
    bar = ShadyBar("Annotating locations", max=len(df_old))

    # Return copy (don't fuck with old df)
    df = df_old.copy(deep=True)

    # Initialize columns
    df["loc_country_code"] = np.nan
    df["loc_zip"] = np.nan
    df["loc_state"] = np.nan
    df["loc_city"] = np.nan
    df["loc_village"] = np.nan
    df["loc_road"] = np.nan

    for index, row in df.iterrows():

        # Intermediate saving of location dictionary
        if index % 1000 is 0:
            try:
                np.save("cache/loc_dict_temp.npy", loc_dict)
            except PermissionError as pe:
                pass

        if log == 1:
            print("Row ", index)

        la = row["latitude"]
        lo = row["longitude"]

        # Reverse geolocation
        loc = get_location(
            la,
            lo,
            loc_dict
        )

        # Set country code
        try:
            df["loc_country_code"].iloc[index] = loc.raw["address"]["country_code"]
        except:
            if log == 1:
                print("Could not find country code for", index)
        # Set zip code/postal code
        try:
            df["loc_zip"].iloc[index] = loc.raw["address"]["postcode"]
        except:
            if log == 1:
                print("Could not find country code for", index)
        # Set state
        try:
            df["loc_state"].iloc[index] = loc.raw["address"]["state"]
        except:
            if log == 1:
                print("Could not find country code for", index)
        # Set city
        try:
            df["loc_city"].iloc[index] = loc.raw["address"]["city"]
        except:
            if log == 1:
                print("Could not find city for", index)
        # Set village
        try:
            df["loc_village"].iloc[index] = loc.raw["address"]["village"]
        except:
            if log == 1:
                print("Could not find village for", index)
        # Set road
        try:
            df["loc_road"].iloc[index] = loc.raw["address"]["road"]
        except:
            if log == 1:
                print("Could not find road for", index)

        bar.next()

    bar.finish()

    # Return resulting df
    df = mobdna_helper.dataframe_cleanup(df)
    return df, loc_dict


# MAIN
if __name__ == "__main__":

    # Say hi
    mobdna_helper.hi()

    # Which dataset are we using?
    try:
        name = sys.argv[1]
    except:
        name = "charles"

    # Initialize
    init_dict = mobdna_helper.initialize(name)

    # Sort in variables
    data = init_dict['data']
    locations = init_dict['locations']
    applications = init_dict['applications']

    try:
        appevents = data['appevents_meta']
        export_name_df = name + '_appevents_loc_meta'
        print("Using app-annotated dataset.\n")
    except:
        appevents = data['appevents']
        export_name_df = name + '_appevents_loc'

    # Annotate data
    updated_appevents, updated_locations = update_df_with_location(appevents, locations)

    # Terminate
    export_name_loc = "loc_dict"
    export_name_meta = "app_dict"

    df_to_export = {
        export_name_df: updated_appevents
    }
    dicts_to_save = {
        export_name_loc: locations,
        export_name_meta: applications
    }

    mobdna_helper.terminate(df_to_export=df_to_export,
                            dict_to_numpy=dicts_to_save,
                            project=name,
                            pickle=True)
