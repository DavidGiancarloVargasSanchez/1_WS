from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd

# 1. Assign the webpage to be scraped to the variable base_url
base_url = 'https://en.wikipedia.org/wiki/World_Soccer_(magazine)'

# 2. Obtain a response of the base_url (sendind an http request)
page = requests.get(base_url)

# 3. Verify if the response is successful
if page.status_code == requests.codes.ok:
    # get the whole page
    bs = BeautifulSoup(page.text, 'lxml')

# 4. Obtain the div container of the data we want
container = bs.find('div', class_='mw-parser-output')

# 5. Obtain all li tags
all_li_tags = container.find('div', class_=None).find('ul').find_all('li')

# 6. Get the last ten winners
last_ten_players = all_li_tags[-10:]

# 7. Create a dictionary to store the information
data = {
    'No': [],
    'Year': [],
    'Player': [],
    'Team':[],
    'Country':[]
}

# 8.  Storing data into the dictionary.
no = len(last_ten_players) + 1
for single_player in last_ten_players:
    no -= 1 
    year = single_player.find('span').previousSibling.split()[0]
    player = single_player.find('a').text
    team = single_player.find_all('a')[1].text
    country = single_player.find('abbr')['title']

    data['No'].append(no)
    
    if year:
        data['Year'].append(year)
    else:
        data['Year'].append('N/A')
    
    if player:
        data['Player'].append(player)
    else:
        data['Player'].append('N/A')
    
    if team:
        data['Team'].append(team)
    else:
        data['Team'].append('N/A')

    if country:
        data['Country'].append(country)
    else:
        data['Country'].append('N/A')

""" Using Pandas """
# 1. Create dataframe
df = pd.DataFrame(data, columns=['No', 'Year', 'Player', 'Team', 'Country'])

# 2. Order table by year descending
df = df.sort_values(by=['Year'], ascending=False)

# 3. Create the csv file
df.to_csv('best_players.csv', sep=',', index=False, encoding='utf-8')

# 4. Print done to indicate it's working
print('done')

# """ Using Pandas """
# If number 6 is not used, we can get the last ten with the following
# df = df.head(n=10)
