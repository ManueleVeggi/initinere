import pandas as pd
import folium
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim


myDf = pd.read_csv("data/output/averages.csv")

latList = []
lonList = []

for idx, row in myDf.iterrows():
    if row["uni"] == "Casamassima - G.Degennaro":
        uniname = "Casamassima"
    elif row["uni"] == "Rozzano (MI) Humanitas University":
        uniname = "Rozzano"
    elif row["uni"] == "Salento":
        uniname = "Lecce"
    elif row["uni"] == "Sannio":
        uniname = "Benevento"
    else:
        uniname = row["uni"]
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(uniname)
    latList.append(getLoc.latitude)
    lonList.append(getLoc.longitude)

myDf["lat"] = latList
myDf["lon"] = lonList
myDf.to_csv("data/output/geocordinatesuni.csv", index=False)
