import PySimpleGUI as sg
import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "rT6wCu7ekTjG9wRb42Cg4NBJ1SkuF8hs"
sg.theme("Purple")

layout = [

    [sg.Text('Where to?', font=('Times New Roman', 20))],
    [sg.Text('Origin:', font=('Times New Roman', 15), size =(10, 1)), sg.InputText()],
    [sg.Text('Destination',font=('Times New Roman', 15), size =(10, 1)), sg.InputText()],
    [sg.Submit("Enter"), sg.Exit()]

]

window = sg.Window('Input Details', layout)
while True: 
    event, values = window.read()
    url = main_api + urllib.parse.urlencode({"key":key, "from":values[0], "to":values[1]})
    window.close()

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        "URL: " + (url),
        "Directions from: " + values[0] + " to " + values[1],
        "Trip Duration: " + (json_data["route"]["formattedTime"]),
        "Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)),
        "Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)),
        directions = " "
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print ((each["narrative"]) + " (" + str ("{:.2f}".format ((each["distance"])*1.61) + " km) "))
            route = (each["narrative"]) + " (" + str ("{:.2f}".format ((each["distance"])*1.61) + " km) ")
            directions = (directions + "\n" + route)

        sg.popup_scrolled (
        
        'Directions from ' + values[0] + ' to ' + values[1],
        "Trip Duration: " + (json_data["route"]["formattedTime"]),
        "Kilometer: " + str ("{:.2f}".format((json_data["route"]["distance"])*1.61)),
        "Fuel Used (Ltr): " + str ("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)),
        directions,
        size = (70,15),
        title = "Route Details"
        )
        

            

    elif json_status == 402:
            print("Status Code: " + str(json_status) + "; Location input cannot be found")
            
            sg.popup(
                
                "Location input cannot be found",
                title = "Input error"
                
                )

    elif json_status == 611:
            print("Status Code: " + str(json_status) + "; Both fields must be filled up.")
            
            sg.popup(
                
                "Both fields must be filled up",
                title = "Input Error"
                
                )

    else:
            print("For Status Code: " + str(json_status) + "; Refer to:")
            print("https://developer.mapquest.com/documentation/directions-api/status-codes")
            
            sg.popup(

                "Status Code: " + str(json_status),
                "Refer to: https://developer.mapquest.com/documentation/directions-api/status-codes",
                title = "Input error"

                )