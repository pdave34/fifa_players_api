import requests
import json

print("-"*100)
print("Listing all players:")
print("-"*100)
result = requests.get("http://127.0.0.1:8000/").json()
print(json.dumps(result, indent=2))


print("-"*100)
print("Adding a player:")
print("-"*100)
result = requests.post("http://127.0.0.1:8000/",
                       json={'name': "Beckham",
                             'id': '4',
                             'position': "midfielder",
                             'skills': {'attack': 90, 'defense': 70}}
                       ).json()
print(json.dumps(result, indent=2))


print("-"*100)
print("Get player id = 2:")
print("-"*100)
result = requests.get("http://127.0.0.1:8000/players/2").json()
print(json.dumps(result, indent=2))


print("-"*100)
print("Update player id = 0 to midfielder:")
print("-"*100)
result = requests.put("http://127.0.0.1:8000/update/0?position=midfielder").json()
print(json.dumps(result, indent=2))


print("-"*100)
print("Deleting player id = 4")
print("-"*100)
result = requests.delete("http://127.0.0.1:8000/delete/4").json()
print(json.dumps(result, indent=2))


print("-"*100)
print("Listing all players:")
print("-"*100)
result = requests.get("http://127.0.0.1:8000/").json()
print(json.dumps(result, indent=2))


print("-"*100)
print("Querying fastest forward:")
print("-"*100)
result = requests.get("http://127.0.0.1:8000/players?position=forward&skill=speed").json()
print(json.dumps(result, indent=2))


print("-"*100)
print("Querying strongest midfielder:")
print("-"*100)
result = requests.get("http://127.0.0.1:8000/players?position=midfielder&skill=strength").json()
print(json.dumps(result, indent=2))


print("-"*100)
print("Querying best players (fastest forward, midfielder, and defender):")
print("-"*100)
result = requests.get("http://127.0.0.1:8000/best?skill=speed&pos=forward&pos=midfielder&pos=defender").json()
print(json.dumps(result, indent=2))
