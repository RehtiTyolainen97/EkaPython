#API-kutsut Hue-sillalle
import requests
from PIL import Image, ImageTk
#Funktiot

#Yhteystesti, input IP-osoite GUIsta
def TestHueConnection(ip_address):    

    url = f"http://{ip_address}/api/"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException:
        return False
    
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