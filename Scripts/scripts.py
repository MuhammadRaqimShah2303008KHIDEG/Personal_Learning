from fastapi import FastAPI
import requests
import uvicorn
# import pandas as pd
# import redis

app = FastAPI()
# redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/api/account")
def get_data():
    # Check if data exists in Redis cache
    # if redis_client.exists('distance'):
    #     distance = redis_client.get('distance')
    #     return {"distance": distance.decode()}

    url = f"https://xloop-dummy.herokuapp.com/account"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        # df = pd.DataFrame(data)
        
        # # Save DataFrame to CSV
        # csv_filename = "data.csv"
        # df.to_csv(csv_filename, index=False)
        
        
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
@app.get("/api/appointment")
def get_data():
    # Check if data exists in Redis cache
    # if redis_client.exists('distance'):
    #     distance = redis_client.get('distance')
    #     return {"distance": distance.decode()}

    url = f"https://xloop-dummy.herokuapp.com/appointment"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    

@app.get("/api/availability")
def get_data():
    # Check if data exists in Redis cache
    # if redis_client.exists('distance'):
    #     distance = redis_client.get('distance')
    #     return {"distance": distance.decode()}

    url = f"https://xloop-dummy.herokuapp.com/availability"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
@app.get("/api/councillor")
def get_data():
    # Check if data exists in Redis cache
    # if redis_client.exists('distance'):
    #     distance = redis_client.get('distance')
    #     return {"distance": distance.decode()}

    url = f"https://xloop-dummy.herokuapp.com/councillor"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
@app.get("/api/patient")
def get_data():
    # Check if data exists in Redis cache
    # if redis_client.exists('distance'):
    #     distance = redis_client.get('distance')
    #     return {"distance": distance.decode()}

    url = f"https://xloop-dummy.herokuapp.com/patient"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
# dist = redis_client.get('distance')
# print("Distance:",int(dist))

if __name__ == '__main__':
    uvicorn.run(app='scripts:app', reload=True, host='0.0.0.0', port=8000)

