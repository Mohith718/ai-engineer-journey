# import asyncio

# async def say_hello():
#     print("Hello...")
#     await asyncio.sleep(2)
#     print("...world!")

# asyncio.run(say_hello())

# import asyncio
# import time

# async def call_api(name, seconds):
#     print(f"Starting {name}...")
#     await asyncio.sleep(seconds)
#     print(f"Finished {name}!")
#     return f"{name} data"

# async def main():
#     start = time.time()
    
#     results = await asyncio.gather(
#         call_api("OpenAI", 2),
#         call_api("Gemini", 3),
#         call_api("Claude", 1)
#     )
    
#     end = time.time()
#     print(f"\nAll results: {results}")
#     print(f"Total time: {end - start:.1f} seconds")

# asyncio.run(main())

from day5_error_handling import logger
class Lead:
    def __init__(self, name, company, email, score):
        self.name=name
        self.company=company
        self.email=email
        self.score=score
    def is_hot(self, threshold):
        return self.score >= threshold
    def summary(self):
        return f"{self.name} from {self.company} — Score: {self.score}"
    def to_dict(self):
        return {"name": self.name, "company": self.company, "email": self.email, "score": self.score}
class LeadManager:
    def __init__(self, filename):
        self.filename=filename
    
    @logger
    def load_leads(self):
        with open(self.filename,"r") as f:
            leads = []
            for line in f:
                parts = line.strip().split(",")
                lead = Lead(parts[0], parts[1], parts[2], int(parts[3]))
                leads.append(lead)
            return leads
    def get_hot_leads(self, threshold):
        parsed=self.load_leads()
        hotleads = [i for i in parsed if i.is_hot(threshold)]
        return hotleads
    def get_emails(self, threshold):
        hotlead=self.get_hot_leads(threshold)
        emailist=[i.email for i in hotlead]
        return emailist
    @logger
    def save_report(self, threshold, output_file):
        hot = self.get_hot_leads(threshold)
        with open(output_file, "w") as f2:
            for lead in hot:
                f2.write(f"{lead.summary()}\n")
            return len(hot)
manager = LeadManager("leads_data.txt")
hot = manager.get_hot_leads(70)
emails = manager.get_emails(70)
count = manager.save_report(70, "report.txt")

for lead in hot:
    print(lead.summary())
print(f"Emails: {emails}")
print(f"Saved {count} leads_to_report.txt")
        