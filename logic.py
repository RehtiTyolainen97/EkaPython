#API-kutsut Hue-sillalle
import requests
import json
#Verkkojuttuihin
import socket
#Kuvankäsittely
from PIL import Image, ImageTk
#Windows ja .env käsittely
import os
from dotenv import load_dotenv
#Funktiot

#Yhteystesti, input IP-osoite GUIsta
def TestHueConnection(bridgeIP):
    try:
        socket.inet_aton(bridgeIP)
        try:    
            url = f"https://{bridgeIP}/api/"
            response = requests.get(url, timeout=2, verify=False)
            return response.status_code
        except requests.exceptions.Timeout:
            return "Timeout"
        except requests.exceptions.ConnectionError:
            return "Unreachable"
    except socket.error:
        return "Invalid IP"


#Muutetaan kuvat läpinäkyviksi, jos valkoinen tausta häiritsee
def Make_Transparent(img_path, white_threshold=250):
    img = Image.open(img_path).convert("RGBA")
    datas = img.getdata()
    new_data = []
    for r, g, b, a in datas:
        # if pixel is (near) white, make it transparent
        if r >= white_threshold and g >= white_threshold and b >= white_threshold:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    return img

#Koitetaan tehdä mDNS-pohjainen sillan etsintä (ei toimi vielä)
#Palauttaa nyt IP-osoitteen tai virheilmoituksen, voiko tehdä fiksummin?
#Ei toimi VPN päällä, tähän pitäisi rakentaa backuppina mDNS haku
def BridgeDiscovery():
    url = "https://discovery.meethue.com/"
    answer = requests.get(url)
    if answer.status_code == 200:
        data = answer.json()
        if len(data) > 0:
            bridgeIP = data[0].get("internalipaddress")
            return bridgeIP
        else:
            return "Discovery failed: No bridges found"
    elif answer.status_code == 429:
        bridgeIP = "Discovery failed: Too many requests (429)"
        return bridgeIP
    else:
        bridgeIP = "Discovery failed " + str(answer.status_code)
        return bridgeIP

#Redditissä sanottiin, että sertifikaatissa on SSL-ongelma, joten ohitetaan varmennus kunnes fixi tulee Philipsiltä
#Tähän pitää miettiä ettei floodata loputtomalla määrällä käyttäjiä siltaa
def GetUserAndKey(bridgeIP):
    url = "https://"+bridgeIP+"/api"
    data = {
    "devicetype": "eliaspc",
    "generateclientkey": True
    }
    env_path = "media/.env"

    #Suoritetaan pyyntö, jos .env ei vielä ole API-tunnuksia
    if not os.path.exists(env_path):
        query = requests.post(url, json=data, verify=False)
        #firstKey on joko error tai success
        firstKey = next(iter(dict(query.json()[0])))

        if firstKey == "error":
            return False
        else:
            apiUsername = dict(query.json()[0])["success"]["username"]
            apiClientkey = dict(query.json()[0])["success"]["clientkey"]
            if not os.path.exists(env_path):
                with open(env_path, 'w') as file:
                    file.write(f"API_USERNAME={apiUsername}\n")
                    file.write(f"API_CLIENTKEY={apiClientkey}\n")
            return True
    else:
        return False
#Hakee laitelistan sillalta ja jäsentää
def FetchCommand(bridgeIp, apiKey):
    load_dotenv(r'media\.env')
    headers = {"hue-application-key": os.getenv("API_USERNAME")}
    print(headers)
    url = f'https://{bridgeIp}/clip/v2/resource/device'
    deviceQuery = requests.get(url, verify=False, headers=headers)
    print(deviceQuery.status_code)
    queryData = deviceQuery.json().get("data")

    products = {}

    for device in queryData:
        product_id = device["id"]
        products[product_id] = {
            "device": device["product_data"]["product_name"],
            "device name": device["metadata"]["name"]
        }
    
    for device_id, name in products.items():
        print(device_id, " ", name)

