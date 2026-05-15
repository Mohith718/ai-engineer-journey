import os
from dotenv import load_dotenv
load_dotenv()
def read_leads():
    with open("leads_data.txt","r") as f:
        content=f.readlines()
        try:
            dlist=[]
            for i in content:
                line=i.strip().split(",")
                linedict={"name":line[0],"company":line[1],"email":line[2],"score":int(line[3])}
                dlist.append(linedict)
            return dlist
        except (KeyError,IndexError) as e:
            return f"error: the is {e}"
def filter_hot_leads(leads, threshold):
    data=[]
    for j in leads:
        if j["score"]>=threshold:
            data.append(j)
    return data
def save_report(leads,filename):
    with open(filename,"w") as l:
        count=0
        for k in leads:
            l.write(f"{k['name']},{k['company']},{k['email']},{k['score']}\n")
            count=count+1
        return count
def main():
    threshold = int(os.getenv("SCORE_THRESHOLD"))
    leads = read_leads()
    hot = filter_hot_leads(leads, threshold)
    count = save_report(hot, "hot_leads.txt")
    print(f"Total leads: {len(leads)}")
    print(f"Hot leads: {len(hot)}")
    print(f"Report saved: hot_leads.txt ({count} leads written)")
main()