# Encoding: utf8
from name_gender import NameGender
from web_name_gender import WebNameGender

def get_decision(guesser, name):
    m,f = guesser.get_gender_scores(name)
    if m > 0.8:
        return "male"
    elif f > 0.8:
        return "female"
    elif m > 0 and f > 0:
        return "both"
    else:
        return "unknown"

# The fallback mechanism is searching for patterns via Yahoo! BOSS API
# In order to use this mecanism, obtain a BOSS aplication ID and put it here.
# See http://developer.yahoo.com/search/boss/
BOSS_API_KEY = ""

# Whole module is case-insensitive.
names = ["Bob",
         "Mary",
         "Jackson",
         "Sharon",         
         "Ahmed",
         "Walt",
         "Tab",
         "Massimo",
         "Mery",
         "Kurramkamerruk"]

# Give precedence to us_census data.
primary_guesser = NameGender("us_census_1990_males", "us_census_1990_females")
secondary_guesser = NameGender("popular_1960_2010_males","popular_1960_2010_females")

if BOSS_API_KEY:
    web_guesser = WebNameGender(BOSS_API_KEY)
else:
    web_guesser = None
    print "No BOSS APP ID is provided. Web-based fallback skipped."
for line in names:
    name = line.strip().lower()
    print name,
    gender = get_decision(primary_guesser, name)
    if gender in ["male", "female", "both"]:
        print gender, "(primary)"
    else: # gender unknown, use secondar guesser
        gender = get_decision(secondary_guesser, name)
        if gender in ["male", "female", "both"]:
            print gender, "(secondary)"
        elif web_guesser:
            m,f = web_guesser.get_gender_scores(name)
            if m > f:
                print "male (web)"
            elif f > m:
                print "female (web)"
            else:
                print "unknown"
        else:
            print "unknown"


    



