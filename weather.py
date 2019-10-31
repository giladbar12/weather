import tkinter as tk
from tkinter import ttk
from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather
import googlemaps
from datetime import datetime

### set up API keys ###
global gmaps
global skyAPI
gmaps = googlemaps.Client(key='Your Google Key')
skyAPI = 'Your DarkSky Key'

### create tkinter window ###
win = tk.Tk()
win.title("Weather")

### creating tkinter container frames ###
weatherCitiesFrame = ttk.LabelFrame( text="Latest Observation for ")
weatherCitiesFrame.grid(column=0, row=0 , padx=8, pady=4)

weatherConditionsFrame = ttk.LabelFrame( text='Current Weather Conditions')
weatherConditionsFrame.grid(column=0, row=1,padx=8,pady=4)

### creating the tkinter labels and entry boxes for display ###
EntryWidth = 24

#loaction
ttk.Label(weatherCitiesFrame, text="City: ").grid(row=0, sticky='E')  
city = tk.StringVar()
locationEntry= ttk.Entry(weatherCitiesFrame, textvariable = city).grid(row=0, column=1, sticky='E')


#last updated
ttk.Label(weatherConditionsFrame,text="last Updated:").grid(column=0,row=2,sticky='E')
updated= tk.StringVar()
updatedEntry = ttk.Entry(weatherConditionsFrame, width =EntryWidth, textvariable=updated, state = 'readonly')
updatedEntry.grid(column=1,row =2, sticky='W')

#weather
ttk.Label(weatherConditionsFrame,text="Weather:").grid(column=0,row=3,sticky='E')
weathers= tk.StringVar()
weatherEntry = ttk.Entry(weatherConditionsFrame, width =EntryWidth, textvariable=weathers, state ='readonly')
weatherEntry.grid(column=1,row =3, sticky='W')

#Temperature
ttk.Label(weatherConditionsFrame,text="Temperature:").grid(column=0,row=4,sticky='E')
temp= tk.StringVar()
tempEntry = ttk.Entry(weatherConditionsFrame, width =EntryWidth, textvariable=temp, state ='readonly')
tempEntry.grid(column=1,row =4, sticky='E')

#Dewpoint
ttk.Label(weatherConditionsFrame,text="Dewpoint:").grid(column=0,row=5,sticky='E')
dew= tk.StringVar()
dewEntry = ttk.Entry(weatherConditionsFrame, width =EntryWidth, textvariable=dew, state ='readonly')
dewEntry.grid(column=1,row =5, sticky='E')

#Relative Humidity
ttk.Label(weatherConditionsFrame,text="Humidity:").grid(column=0,row=6,sticky='E')
relHum= tk.StringVar()
relHumEntry = ttk.Entry(weatherConditionsFrame, width =EntryWidth, textvariable=relHum, state ='readonly')
relHumEntry.grid(column=1,row =6, sticky='W')

#wind
ttk.Label(weatherConditionsFrame,text="Wind:").grid(column=0,row=7,sticky='E')
wind= tk.StringVar()
windEntry = ttk.Entry(weatherConditionsFrame, width =EntryWidth, textvariable=wind, state ='readonly')
windEntry.grid(column=1,row =7, sticky='W')

#visibility
ttk.Label(weatherConditionsFrame,text="Visibility:").grid(column=0,row=8,sticky='E')
visibility= tk.StringVar()
visibilityEntry = ttk.Entry(weatherConditionsFrame, width =EntryWidth, textvariable=visibility, state ='readonly')
visibilityEntry.grid(column=1,row =8, sticky='W')

#precipitation
ttk.Label(weatherConditionsFrame,text="Precipitation:").grid(column=0,row=9,sticky='E')
prec= tk.StringVar()
percEntry = ttk.Entry(weatherConditionsFrame, width =EntryWidth, textvariable=prec, state ='readonly')
percEntry.grid(column=1,row =9, sticky='W')

#UV-Index
ttk.Label(weatherConditionsFrame,text="UV-Index").grid(column=0,row=10,sticky='E')
uv= tk.StringVar()
uvEntry = ttk.Entry(weatherConditionsFrame, width =EntryWidth, textvariable=uv, state ='readonly')
uvEntry.grid(column=1,row =10, sticky='W')

# set padding 
for child in weatherConditionsFrame.winfo_children():
    child.grid_configure(padx=4, pady=2)


for child in weatherCitiesFrame.winfo_children():
    child.grid_configure(padx =5,pady=4)


#### the function sets up the API requests and populates the veriables ###
def setValues():
  location = str(city.get())
  if location[-3:]=='usa':
      usa=1
  else: 
      usa=0
  # Geocoding the city using GoogleMaps API
  geocode_result = gmaps.geocode(location)
  lat = geocode_result[0]['geometry']['location']['lat']
  lng = geocode_result[0]['geometry']['location']['lng']

  # set up darksky API to retreave weather data
  darksky = DarkSky(skyAPI)
  forecast = darksky.get_forecast(
    lat, lng,
    extend=False, # default `False`
    lang=languages.ENGLISH, # default `ENGLISH`
    units=units.AUTO, # default `auto`
    exclude=[weather.MINUTELY, weather.ALERTS] # default `[]`
    )

  # set the variables for display
  wind.set(str(round(forecast.currently.wind_speed,2))+ 'mph')
  updated.set(str(forecast.currently.time)[:-6])
  weathers.set(forecast.currently.summary)
  if usa == 0:
      tempC= round(forecast.currently.temperature)
      tempF= round(forecast.currently.temperature*1.8+32)
  else:
      tempF= round(forecast.currently.temperature)
      tempC= round((forecast.currently.temperature-32)/1.8)
  temp.set(str(int(tempC))+'℃ ' +str(int(tempF))+'℉ ')
  relHum.set(str(int(forecast.currently.humidity*100))+'%')
  visibility.set(str(round(forecast.currently.visibility,2))+'miles')
  if str(forecast.currently.precip_type) == 'None':
      prec.set(str(forecast.currently.precip_type))
  else:
      prec.set(str(int(forecast.currently.precip_probability))+"% "+str(forecast.currently.precip_type))
  uv.set(str(int(forecast.currently.uv_index)))
  if usa == 0:
      dewC= round(forecast.currently.dew_point)
      dewF= round(forecast.currently.dew_point*1.8+32)
  else:
      dewF= round(forecast.currently.dew_point)
      dewC= round((forecast.currently.dew_point-32)/1.8)
  dew.set(str(int(dewC))+'℃ ' +str(int(dewF))+'℉ ')
  

    
#### create tkinter button to get the weather ###
button1 =ttk.Button(weatherCitiesFrame, text="Get Weather", command=setValues).grid(row=3, column=0, sticky='W') 


#start Gui
win.resizable(0,0)
win.mainloop()


