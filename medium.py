from bs4 import BeautifulSoup
import requests


# Create a class for Medium links
class Medium:
    def __init__(self, link):
        self.link = link
        self.type = None
        self.data = BeautifulSoup(requests.get(self.link).text, "html5lib")
        self.title = self.data("title")[0].text
        self.author = self.title.replace(" – Medium","")
        self.authorNickname = "Unknown"

        # Scan through meta tags for author info
        for tag in self.data.find_all("meta"):
            if tag.get("name", None) == 'author':
                self.authorNickname = (tag.get('content',None))
            if tag.get("property", None) == 'article:author':
                self.author = (tag.get('content',None))
                if "https://medium.com/@" in self.author:
                    self.author = self.author.replace("https://medium.com/@","")
                elif ".medium.com" in self.author:
                    self.author = self.author.replace("https://","").replace(".medium.com","")
            if tag.get("property", None) == 'profile:username':
                self.author = (tag.get('content',None))
                self.type = 'Profile'
            if tag.get("property", None) == 'profile:username':
                self.author = (tag.get('content',None))
                self.type = 'Profile'

        # Detect profiles with the title
        if " – Medium" in self.title:
            self.type = "Profile"

        # Check if it's a paid post
        for script in self.data.find_all("script"):
            if script.string == None:
                pass
            elif "\"isAccessibleForFree\":\"False\"" in script.string:
                self.type = "Paid"

        # If it's not a paid post, then it's a free post
        if self.type == None:
            self.type = "Free"

    # Generate a response for reddit comments
    def response(self):
        if self.type == "Paid":
            message = "[This is not a free Medium article]({}).  Article was posted by {} ({})".format(self.link,self.authorNickname,self.author)
            return message
        elif self.type == "Free":
            message = "[This is a free Medium article]({}).  Article was posted by {} ({})".format(self.link,self.authorNickname,self.author)
            return message
        elif self.type == "Profile":
            message = "[This is a link]({}) to {}'s profile".format(self.link,self.author)
            return message
        else:
            return 0


# Search a submission for medium links in the body
def findLink(submission):
    results = []
    data = submission.selftext.split("\n")
    for entry in data:
        if "medium.com" in entry:
            temp = entry.split(" ")
            for part in temp:
                if "](" in part:
                    part = part.split("](")[0].replace("[","")
                if "medium.com" in part:
                    results.append(part)
    return results
