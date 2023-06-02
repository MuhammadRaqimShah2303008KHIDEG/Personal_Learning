from fastapi import FastAPI
import requests
import uvicorn
import redis

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/api")
def get_data():
    # Check if data exists in Redis cache
    if redis_client.exists('distance'):
        distance = redis_client.get('distance')
        return {"distance": distance.decode()}

    url = f"https://api.tomtom.com/routing/1/calculateRoute/52.50931,13.42936:52.50274,13.43872/json?key=ir7kpwjOTDBQAvJ9vhYV1gSPuWLIvsD8"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data["routes"][0]["summary"]["lengthInMeters"]

        # Store data in Redis cache
        redis_client.set('distance', rate)
        
        return {"distance": rate}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
dist = redis_client.get('distance')
print("Distance:",int(dist))

# if __name__ == '__main__':
#     uvicorn.run(app='main:app', reload=True, host='0.0.0.0', port=8000)


#Cronjob Code:
# * * * * * /usr/bin/python3 /home/syedmuhammadraqimali/Documents/ETL/cron_job/main.py >> /home/syedmuhammadraqimali/Documents/ETL/cron_job/log_file.log 2>&1

