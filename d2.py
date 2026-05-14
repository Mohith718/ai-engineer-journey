# Challenge -1
# def safe_get_lead_info(lead):
#     name=lead.get("name","no name")
#     company=lead.get("company","no company")
#     email=lead.get("email","no email")
#     score=lead.get("score",0)
#     return f"{name} from {company} - {email} (score: {score})"
# lead1 = {"name": "Arjun", "company": "Redsage", "email": "arjun@redsage.in", "score": 85}
# lead2 = {"name": "Sneha", "company": "Fractal"}
# print(safe_get_lead_info(lead1))
# print(safe_get_lead_info(lead2))

# import requests
# def get_random_user():
#     url = "https://randomuser.me/api/"
#     response = requests.get(url)
#     data = response.json()   
#     user = data["results"][0]
#     name = f"{user['name']['first']} {user['name']['last']}"
#     email = user["email"]
#     country = user["location"]["country"]   
#     return f"{name} — {email} — {country}"
# print(get_random_user())


# Challenge -2
# import requests
# def get_random_user():
#     try:
#          url = "https://randomuser.me/api/"
#          response = requests.get(url)
#          if response.status_code !=200:
#               return f"Error: API returned status {response.status_code}"
#          data = response.json()   
#          user = data["results"][0]  
#          name = f"{user['name']['first']} {user['name']['last']}"
#          email = user["email"]
#          country = user["location"]["country"]
#          print(response)
#          return f"{name} — {email} — {country}"
#     except (requests.exceptions.ConnectionError,KeyError) as e:
#          return f"Error: could not fetch user — {e}"
# print(get_random_user())


# Challenge -3
import requests
def fetch_multiple_users(count):
    try:
         url= f"https://randomuser.me/api/?results={count}"
         response=requests.get(url)
         if response.status_code !=200:
             return f"Error: API returned status {response.status_code}"
         data=response.json()
         user=data["results"]   
         empt=[]
         for i in user:
             name_data = i.get("name", {})
             name = f"{name_data.get('first', 'unknown')} {name_data.get('last', 'unknown')}"
             email=i.get("email")
             country=i.get("location",{}).get("country","unknown")
             dnry = {"name": name, "email": email, "country": country}
             empt.append(dnry)
         return empt
    except (requests.exceptions.ConnectionError,KeyError) as e:
          return f"Error: could not fetch user — {e}"
print(fetch_multiple_users(5))