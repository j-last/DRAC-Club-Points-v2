
import time
import requests
from bs4 import BeautifulSoup as bs

from Code.NameResolver import NameResolver


class WebScraper:

    def getTotalRaceTimingResults(url:str) -> dict[str:time]:
        """Web scrapes all dereham runners AC results from a totalracetiming website.
        Returns a dictionary with entries in the form {runnerName : runnerTime}
        """
        race_runners = {}

        page = requests.get(url)
        soup = bs(page.content, "html.parser")
        runners = soup.find_all("tr") # gets all 
        for runner in runners:
            runnerstring = runner.decode_contents()
            if "<td>Dereham Runners AC</td>" in runnerstring:
                name_start_index = runnerstring.find('"Open official result">') + len('"Open official result">')
                name_end_index = runnerstring.find("</b>")
                name = runnerstring[name_start_index:name_end_index].replace("<b>", "")

                time_start_index = runnerstring.find('results-col-chip"> ') + len('results-col-chip"> ')
                chipTime = runnerstring[time_start_index:time_start_index+8]
                chipTime = time.strptime(chipTime, "%H:%M:%S")

                race_runners[name] = chipTime
        
        return race_runners
    

    def getParkrunners(web_text:str) -> list[str]:
        """Searches through the text to find all Dereham Runenrs who did parkrun,
        and returns a list of these names."""
        endindex = web_text.find("Dereham Runners AC")
        runners = []

        while endindex != -1:
            index = endindex
            spacesfound = 0
            while spacesfound != 2:
                index -= 1
                if web_text[index] == "	":
                    spacesfound += 1
            name = web_text[index:endindex].strip()
            name = name.split(" ")
            if len(name) >= 2:
                newname = name[0]
                for i in range(1, len(name)):
                    name[i] = name[i].upper()
                    newname += " " + name[i]
                name = newname
                runners.append(NameResolver.capitalise(name))
            web_text = web_text[endindex + 1 :]
            endindex = web_text.find("Dereham Runners AC")

        return runners
    