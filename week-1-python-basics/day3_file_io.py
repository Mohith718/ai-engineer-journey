# Writing to a file
# with open("leads.txt", "w") as f:
#     f.write("Arjun — Redsage — 85\n")
#     f.write("Sneha — Fractal — 45\n")
#     f.write("Vikram — Deccan AI — 92\n")
# Reading from a file
# with open("leads.txt", "r") as f:
#     content = f.read()
#     print(content)

# # Challenge -1
# def save_leads_report(leads):
#     count=0
#     with open("hot_leads.txt","w") as f:
#         for i in leads:
#             if i["score"]>=70:
#                 f.write(f"{i['name']} | {i['company']} | {i['email']} | Score: {i['score']}\n")
#                 count=count+1
#         return count
# leads = [
#     {"name": "Arjun", "company": "Redsage", "score": 85, "email": "arjun@redsage.in"},
#     {"name": "Sneha", "company": "Fractal", "score": 45, "email": "sneha@fractal.ai"},
#     {"name": "Vikram", "company": "Deccan AI", "score": 92, "email": "vikram@deccanai.com"},
#     {"name": "Pooja", "company": "TCS", "score": 60, "email": "pooja@tcs.com"}
# ]
# print(save_leads_report(leads))


# import os
# from dotenv import load_dotenv
# load_dotenv()
# name = os.getenv("MY_NAME")
# city = os.getenv("MY_CITY")
# print(f"{name} is from {city}")

