# Challenge -1

numbers = [10, 25, 3, 48, 72, 15, 90, 6]
newlist1= [i for i in numbers if i>20]
newlist2= [i*2 for i in numbers]
leads = [
    {"name": "Arjun", "company": "Redsage", "email": "arjun@redsage.in", "score": 85},
    {"name": "Sneha", "company": "Fractal", "email": "sneha@fractal.ai", "score": 45},
    {"name": "Vikram", "company": "Deccan AI", "email": "vikram@deccanai.com", "score": 92},
    {"name": "Ravi", "company": "Infosys", "email": "ravi@infosys.com", "score": 78}
]
newlist3= [i["email"] for i in leads if i["score"]>=70]
print(newlist1)
print(newlist2)
print(newlist3)

# Challenge -2
def clean_and_parse(messy):
    raw=messy.split(",")
    clean=[i.strip() for i in raw]
    city=clean[2].title()
    return {"name":clean[0],"email":clean[1],"city":city,"role":clean[3].lower()}
messy = "   Mohith Srinivas , mohithsrinivassomaraju@gmail.com , HYDERABAD ,  ai engineer   "
print(clean_and_parse(messy))

# Challenge -3
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
lead1 = Lead("Arjun", "Redsage", "arjun@redsage.in", 85)
lead2 = Lead("Sneha", "Fractal", "sneha@fractal.ai", 45)
lead3 = Lead("Vikram", "Deccan AI", "vikram@deccanai.com", 92)
print(lead1.summary())
print(lead2.summary())
print(lead3.summary())
print(lead1.is_hot(70))
print(lead2.is_hot(70))

# Challenge -4
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
class LeadProcessor:
    def __init__(self,filename,threshold):
        self.filename=filename
        self.threshold=threshold
    def load_leads(self):
        newlist=[]
        with open(self.filename,"r") as f:
            dlist=[]
            for i in f:
                line = i.strip().split(",")
                lead = Lead(line[0], line[1], line[2], int(line[3]))
                newlist.append(lead)
            return newlist
    def get_hot_leads(self):
        call=self.load_leads()
        raw=[]
        for i in call:
            if i.is_hot(self.threshold)==True:
                raw.append(i)
        return raw
    def generate_report(self):
        store=self.get_hot_leads()
        count=0
        for j in store:
            print(j.summary())
            count=count+1
        return count

processor = LeadProcessor("leads_data.txt", 70)
count = processor.generate_report()
print(f"Total hot leads: {count}")