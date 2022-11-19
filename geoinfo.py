import pandas as pd
from geopy.geocoders import Nominatim

myDf = pd.read_csv("data/output/averages.csv")

latList = []
lonList = []

for idx, row in myDf.iterrows():
    if row["uni"] == "Casamassima - G.Degennaro":
        uniname = "Casamassima"
    elif row["uni"] == "Rozzano (MI) Humanitas University":
        uniname = "Rozzano"
    else:
        uniname = row["uni"]
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(uniname)
    latList.append(getLoc.latitude)
    lonList.append(getLoc.longitude)

myDf["lat"] = latList
myDf["lon"] = lonList
myDf.to_csv("data/output/geocordinatesuni.csv", index=False)
