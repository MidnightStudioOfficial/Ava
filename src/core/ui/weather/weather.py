import customtkinter as ctk
import requests
from PIL import Image
from datetime import date
from tkinter import messagebox

# Global variable for current dat, used inside the class
today = str(date.today())


class WeatherGUI(ctk.CTkFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.city_value = ctk.StringVar()
        self.location_var = ctk.StringVar()
        self.city_var = ctk.StringVar()
        self.long_var = ctk.StringVar()
        self.lat_var = ctk.StringVar()
        self.temp_var = ctk.StringVar()
        self.tempMin_var = ctk.StringVar()
        self.tempMax_var = ctk.StringVar()
        self.feelsLike_var = ctk.StringVar()
        self.feelsLike_varMin_var = ctk.StringVar()
        self.feelsLike_varMax_var = ctk.StringVar()
        self.wind_var = ctk.StringVar()
        self.speed_var = ctk.StringVar()
        self.gusts_var = ctk.StringVar()
        self.dir_var = ctk.StringVar()
        self.angle_var = ctk.StringVar()
        self.cloudCover_var = ctk.StringVar()
        self.press_var = ctk.StringVar()
        self.precip_var = ctk.StringVar()
        self.total_var = ctk.StringVar()
        self.type_var = ctk.StringVar()
        self.prob_var = ctk.StringVar()
        self.probPrecip_var = ctk.StringVar()
        self.storm_var = ctk.StringVar()
        self.freeze_var = ctk.StringVar()
        self.ozone_var = ctk.StringVar()
        self.humidity_var = ctk.StringVar()
        self.humidity = ctk.StringVar()
        self.weather_var = ctk.StringVar()
        self.visibility_var = ctk.StringVar()
        self.weather_var = ctk.StringVar()
        self.summary_var = ctk.StringVar()
        self.location_var.set("Location")
        self.city_var.set("City, Country")
        self.long_var.set("Longitude: ")
        self.lat_var.set("Latitude: ")
        self.weather_var.set("sunny")
        self.temp_var.set("°C")
        self.tempMin_var.set("Min Temperature: " + "°C")
        self.tempMax_var.set("Max Temperature : " + "°C")

        self.feelsLike_var.set("Feels Like : " + "°C")
        self.feelsLike_varMin_var.set("Min Feels Like: " + "°C")
        self.feelsLike_varMax_var.set("Max Feels Like : " + "°C")

        self.wind_var.set("Wind: ")
        self.speed_var.set("0") 
        self.gusts_var.set("Gusts: ")
        self.dir_var.set("Direction: ")
        self.angle_var.set("Angle: ")

        self.cloudCover_var.set("Cloud Cover: ")
        self.press_var.set("Pressure: ")

        self.precip_var.set("Precipitation: ")
        self.total_var.set("Total: ")
        self.type_var.set("Type: ")

        self.prob_var.set("Precipitation: ")
        self.probPrecip_var.set("0")
        self.storm_var.set("Storm: ")
        self.freeze_var.set("Freeze: ")

        self.ozone_var.set("Ozone: ")
        self.humidity_var.set("0")
        self.humidity.set("Humidity: ")
        self.visibility_var.set("Visibility: ")

        self.cityEntry = ctk.CTkEntry(parent, textvariable=self.city_value, fg_color="transparent",  
                                                width=280, height=40, font=('Arial', 14)).place(x=46, y=25)

        self.searchBtn = ctk.CTkButton(parent, command=self.showWeather, text="Check Weather", font=('Arial', 12), hover=True, 
                                                hover_color="black", height=40, width=130, border_width=2, corner_radius=10).place(x=46, y=83) # border_color= "#c75d55", fg_color= "#262626"  text_color="#c75d55",

        self.left_frame = ctk.CTkFrame(parent, width=300, height=300, corner_radius=5)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(25, 345), pady=(200, 350))
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.place(x=35, y=150)

        self.imgPath_var = "2"
        self.folder_path = "Data"
        self.path = f"{self.folder_path}\WeatherAppIcons\{self.imgPath_var}.png"
        self.img = ctk.CTkImage(Image.open(self.path), size=(200, 200))

        self.cityLbl = ctk.CTkLabel(self.left_frame, textvariable=self.city_var, font=('Arial', 25)).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)   
        self.icon = ctk.CTkLabel(self.left_frame, image=self.img, text="", anchor=ctk.CENTER).place(x=65, y=60)
        self.weatherLbl = ctk.CTkLabel(self.left_frame, textvariable=self.weather_var, font=('Arial', 22)).place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

        self.right_frame = ctk.CTkFrame(parent, width=300, height=300, corner_radius=5)
        self.right_frame.grid(row=0, column=0, sticky="nsew", padx=(355, 15), pady=(200, 350))
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.place(x=365, y=150)

        self.dateLbl = ctk.CTkLabel(self.right_frame, text=f"Date: {today}", font=('Arial', 25), anchor=ctk.CENTER).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        self.tempLbl = ctk.CTkLabel(self.right_frame, textvariable=self.temp_var, font=('Arial', 90)).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.feelsLbl = ctk.CTkLabel(self.right_frame, textvariable=self.feelsLike_var, font=('Arial', 18)).place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

        self.probPrecipLbl = ctk.CTkLabel(parent, textvariable=self.probPrecip_var, font=('Arial', 50)).place(x=140, y=500, anchor=ctk.CENTER) 
        self.speedLb1 = ctk.CTkLabel(parent, textvariable=self.speed_var, font=('Arial', 50)).place(x=352, y=500, anchor=ctk.CENTER)
        self.humidityLbl = ctk.CTkLabel(parent, textvariable=self.humidity_var, font=('Arial', 50)).place(x=562, y=500, anchor=ctk.CENTER)

        self.probPrecipH = ctk.CTkLabel(parent, textvariable=self.prob_var, font=('Arial', 22)).place(x=80, y=550)
        self.speedH = ctk.CTkLabel(parent, textvariable=self.wind_var, font=('Arial', 22)).place(x=325, y=550)
        self.humidityH = ctk.CTkLabel(parent, textvariable=self.humidity, font=('Arial', 22)).place(x=520, y=550)

        self.tabview = ctk.CTkTabview(parent, width=660, height=180, border_width=4)
        self.tabview.grid(row=0, column=0, padx=(10, 0), pady=(690, 0), sticky="nsew")
        self.tabview.place(x=20, y=600)
        self.tabview.add("Summary")
        self.tabview.add("Temperature")
        self.tabview.add("Wind")
        self.tabview.add("Probability")
        self.tabview.add("Others")

        self.textbox = ctk.CTkTextbox(self.tabview.tab("Summary"), width=630, height=127)
        self.textbox.place(x=8, y=0)

        self.tempMinLbl = ctk.CTkLabel(self.tabview.tab("Temperature"), textvariable=self.tempMin_var, font=('Arial', 14)).place(x=15, y=20)
        self.tempMaxLbl = ctk.CTkLabel(self.tabview.tab("Temperature"), textvariable=self.tempMax_var, font=('Arial', 14)).place(x=15, y=40)
        self.feelsMinLbl = ctk.CTkLabel(self.tabview.tab("Temperature"), textvariable=self.feelsLike_varMin_var, font=('Arial', 14)).place(x=15, y=60)
        self.feelsMaxLbl = ctk.CTkLabel(self.tabview.tab("Temperature"), textvariable=self.feelsLike_varMax_var, font=('Arial', 14)).place(x=15, y=80)

        self.gusts = ctk.CTkLabel(self.tabview.tab("Wind"), textvariable=self.gusts_var, font=('Arial', 14)).place(x=15, y=20)
        self.dir = ctk.CTkLabel(self.tabview.tab("Wind"), textvariable=self.dir_var, font=('Arial', 14)).place(x=15, y=40)
        self.angle = ctk.CTkLabel(self.tabview.tab("Wind"), textvariable=self.angle_var, font=('Arial', 14)).place(x=15, y=60)

        self.stormLbl = ctk.CTkLabel(self.tabview.tab("Probability"), textvariable=self.storm_var, font=('Arial', 14)).place(x=15, y=20)
        self.freezeLbl = ctk.CTkLabel(self.tabview.tab("Probability"), textvariable=self.freeze_var, font=('Arial', 14)).place(x=15, y=40)

        self.cloudCoverLbl = ctk.CTkLabel(self.tabview.tab("Others"), textvariable=self.cloudCover_var, font=('Arial', 14)).place(x=15, y=0)
        self.pressLbl = ctk.CTkLabel(self.tabview.tab("Others"), textvariable=self.press_var, font=('Arial', 14)).place(x=15, y=20)
        self.precipLbl = ctk.CTkLabel(self.tabview.tab("Others"), textvariable=self.precip_var, font=('Arial', 14)).place(x=15, y=40)
        self.totalLbl = ctk.CTkLabel(self.tabview.tab("Others"), textvariable=self.total_var, font=('Arial', 14)).place(x=15, y=60)
        self.typeLbl = ctk.CTkLabel(self.tabview.tab("Others"), textvariable=self.type_var, font=('Arial', 14)).place(x=15, y=80)
        self.ozoneLbl = ctk.CTkLabel(self.tabview.tab("Others"), textvariable=self.ozone_var, font=('Arial', 14)).place(x=270, y=0)
        self.visibilityLbl = ctk.CTkLabel(self.tabview.tab("Others"), textvariable=self.visibility_var, font=('Arial', 14)).place(x=270, y=20)
        self.locLbl = ctk.CTkLabel(self.tabview.tab("Others"), textvariable=self.location_var, font=('Arial', 14)).place(x=450, y=0)
        self.longLbl = ctk.CTkLabel(self.tabview.tab("Others"), textvariable=self.long_var, font=('Arial', 14)).place(x=470, y=25)
        self.latLbl = ctk.CTkLabel(self.tabview.tab("Others"), textvariable=self.lat_var, font=('Arial', 14)).place(x=470, y=50)

    def showWeather(self):
        if len(self.textbox.get("1.0", ctk.END)) >= 1: #check if the textbox is not empty
            self.textbox.delete("1.0", ctk.END) #if not, delete prev. summary

        city_name = self.city_value.get()

        if len(city_name) == 0:
            messagebox.showwarning("Warning", "Please input city name!")
        else:
            info_url = "https://ai-weather-by-meteosource.p.rapidapi.com/find_places"
            weather_url = "https://ai-weather-by-meteosource.p.rapidapi.com/daily"
            querystring = {"text": city_name}

            headers = {
                "X-RapidAPI-Key": "8d851cd213msh1c5da36d093dbe5p181de9jsn7e2cb91e4a2d", # Visit the link below, sign-up, subscribe, and copy the key then paste it here
                "X-RapidAPI-Host": "ai-weather-by-meteosource.p.rapidapi.com"
            }

            response = requests.request("GET", info_url, headers=headers, params=querystring)

            _info = response.json()

            place_id = _info[0]['place_id']
            city = _info[0]['name']
            country = _info[0]['country']
            coordinatesLong = _info[0]['lon']
            coordinatesLat = _info[0]['lat']

            infostring = {"place_id": place_id, "units": "metric"}

            weather_response = requests.request("GET", weather_url, headers=headers, params=infostring)
            weather_info = weather_response.json()

            weather = str(weather_info['daily']['data'][0]['weather'])
            summary = str(weather_info['daily']['data'][0]['summary'])

            temperature = float(weather_info['daily']['data'][0]['temperature'])
            temperature_min = str(weather_info['daily']['data'][0]['temperature_min'])
            temperature_max = str(weather_info['daily']['data'][0]['temperature_max'])
            feels_like = str(weather_info['daily']['data'][0]['feels_like'])
            feels_like_min = str(weather_info['daily']['data'][0]['feels_like_min'])
            feels_like_max = str(weather_info['daily']['data'][0]['feels_like_max'])

            speed = str(weather_info['daily']['data'][0]['wind']['speed'])
            gusts = str(weather_info['daily']['data'][0]['wind']['gusts'])
            dir = str(weather_info['daily']['data'][0]['wind']['dir'])
            angle = str(weather_info['daily']['data'][0]['wind']['angle'])

            cloud_cover = str(weather_info['daily']['data'][0]['cloud_cover'])
            pressure = str(weather_info['daily']['data'][0]['pressure'])

            total = str(weather_info['daily']['data'][0]['precipitation']['total'])
            type = str(weather_info['daily']['data'][0]['precipitation']['type'])

            precipitation = str(weather_info['daily']['data'][0]['probability']['precipitation'])
            storm = str(weather_info['daily']['data'][0]['probability']['storm'])
            freeze = str(weather_info['daily']['data'][0]['probability']['freeze'])

            ozone = str(weather_info['daily']['data'][0]['ozone'])
            humidity = str(weather_info['daily']['data'][0]['humidity'])
            visibility = str(weather_info['daily']['data'][0]['visibility'])

            icon = str(weather_info['daily']['data'][0]['icon'])

            cityCountry = str(city + ", " + country)
            if len(cityCountry) > 25:
                cityCountry = cityCountry[:22] + '...'

            self.location_var.set("Location")
            self.city_var.set(cityCountry)
            self.long_var.set("Longitude: " + coordinatesLong)
            self.lat_var.set("Latitude: " + coordinatesLat)

            rounded_temp = round(temperature, 1)

            self.temp_var.set(str(rounded_temp) + "°C")
            self.tempMin_var.set("Min Temperature: " + str(temperature_min) + "°C")
            self.tempMax_var.set("Max Temperature : " + str(temperature_max) + "°C")

            self.feelsLike_var.set("Feels Like : " + str(feels_like) + "°C")
            self.feelsLike_varMin_var.set("Min Feels Like: " + str(feels_like_min) + "°C")
            self.feelsLike_varMax_var.set("Max Feels Like : " + str(feels_like_max) + "°C")

            self.wind_var.set("Wind: ")
            self.speed_var.set(str(speed) + "km/h")
            self.gusts_var.set("Gusts: " + str(gusts))
            self.dir_var.set("Direction: " + str(dir))
            self.angle_var.set("Angle: " + str(angle))

            self.cloudCover_var.set("Cloud Cover: " + str(cloud_cover))
            self.press_var.set("Pressure: " + str(pressure))

            self.precip_var.set("Precipitation: ")
            self.total_var.set("Total: " + str(total))
            self.type_var.set("Type: " + str(type))

            self.prob_var.set("Precipitation: ")
            self.probPrecip_var.set(str(precipitation))
            self.storm_var.set("Storm: " + str(storm))
            self.freeze_var.set("Freeze: " + str(freeze))

            self.ozone_var.set("Ozone: " + str(ozone))
            self.humidity_var.set(str(humidity))
            self.visibility_var.set("Visibility: " + str(visibility))

            self.weather_var.set(str(weather.replace("_", " ")))

            self.textbox.insert("0.0", str(city + ", " + country + ": " + summary))

            self.imgPath_var = icon
            self.path = f"{self.folder_path}\WeatherAppIcons\\" + str(self.imgPath_var) + ".png"
            self.new_image = ctk.CTkImage(Image.open(self.path), size=(200, 200))
            self.icon = ctk.CTkLabel(self.left_frame, image=self.new_image, text="", fg_color="transparent").place(x=65, y=60)

        self.weather_var.set("Weather: " + str(weather))
        self.summary_var.set("Summary: " + str(summary))
