# Challenge -1
name="mohith"
age="23"
print(f"my name is {name} and my age is {age}")

# Challenge -2

def detail(name,age):
    message=f"my name {name} and my age {age}"
    return message
output=detail("Mohith",23)
print(output)

# Challenge -3

def calculate_age_in_months(age):
    message=age*12
    return message
output=calculate_age_in_months(23)
print(output)

# Challenge -4

def calculate_age_in_months(age):
    months=age*12
    return months
def profile(name,age,city):
    months=calculate_age_in_months(age)
    return f"{name}, {age} years ({months} months), based in {city}"
print(profile("mohith",23,"HYD"))

# Challenge -5

def show_skills(name,my_skills):
    print(f"{name} knows these skills:")
    for index,i in enumerate(my_skills):
        print(f"{index+1}. {i}")
    return len(my_skills)
my_skills = ["n8n", "VAPI", "Python", "LangChain"]
total = show_skills("Mohith", my_skills)
print(f"Total skills: {total}")

# Challenge -6

def process_client(client):
    if client["is_returning"]==True:
        print(f"Welcome back, {client['name']}")
    else:
        print(f"New client: {client['name']}. Saving to CRM.")
    return f"{client['name']} - {client['phone']}"
client = {
    "name": "Rahul Sharma",
    "phone": "+91 98765 43210",
    "appointment": "2026-05-15",
    "is_returning": True
}
new_client = {
    "name": "Priya Reddy",
    "phone": "+91 91234 56789",
    "appointment": "2026-05-16",
    "is_returning": False
}
print(process_client(new_client))
print(process_client(client))

# Challenge -7

def process_leads(leads):
    hotleads=[]
    for i in leads:
        if i["score"]>=70:
            hotleads.append(i)
            print(f"HOT LEAD: {i['name']} from {i['company']}")
        else:
            print(f"COLD LEAD: {i['name']} — skipping")
    return hotleads
leads = [
    {"name": "Arjun", "company": "Redsage", "score": 85, "email": "arjun@redsage.in"},
    {"name": "Sneha", "company": "Fractal", "score": 45, "email": "sneha@fractal.ai"},
    {"name": "Vikram", "company": "Deccan AI", "score": 92, "email": "vikram@deccanai.com"},
    {"name": "Pooja", "company": "TCS", "score": 60, "email": "pooja@tcs.com"}
]

hot = process_leads(leads)
print(f"Total hot leads: {len(hot)}")