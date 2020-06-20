import requests
import json
from dotenv import load_dotenv 
key = os.environ.get('key')
def get_data(containment_wards):
    #address= ', '.join(map(str, containment_wards['Area Name'][i].split(',')[:2])) 
    print(containment_wards['Sl no'])
    response=""
    received_data=""
    address=containment_wards['Address']
    address=address.upper()
    address=address.replace(" ST,"," STREET,")
    if(int(containment_wards['Ward'])==0):
        URL=str("https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key="+key)
        response=get_response(URL)
    elif(len(address)>0):   
        URL=str("https://maps.googleapis.com/maps/api/geocode/json?address="+address+", Ward "+str(int(containment_wards['Ward']))+", Kolkata"+"&key="+key)
        response=get_response(URL)
        received_data = json.loads(response.text)
    if(len(received_data)>0 and len(received_data['results'])==0 and len(str(containment_wards['Local area']))>0):
        URL=str("https://maps.googleapis.com/maps/api/geocode/json?address="+str(containment_wards['Local area'])+", Kolkata"+"&key="+key)
        response=get_response(URL)
        received_data = json.loads(response.text)
    try:
        print("Success")
        return ([received_data['results'][0]['geometry']['location']['lat'],received_data['results'][0]['geometry']['location']['lng'],containment_wards['Address']+" Ward: "+str(int(containment_wards['Ward']))])
    except:
        print(received_data)
    return ""
def get_response(URL):
    response=""
    tries=10
    for i in range(tries):
        try:
            response=requests.get(URL)
        except:
            if(i<tries):
                continue
        break
    if(response==""):
        print("FAILED")
    return response