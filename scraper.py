import requests, json
from datetime import datetime

def scrape_all_ids():
    maps = {'espn_nfl_teams': {}, 'espn_cfb_teams': {}, 'nhl_teams': {}, 'players': {}}
    sports = {'nfl': 'football/nfl', 'cfb': 'football/college-football'}

    for sport, path in sports.items():
        url = f"https://site.api.espn.com/apis/site/v2/sports/{path}/teams?limit=1000"
        r = requests.get(url, timeout=15)
        data = r.json()
        for team in data.get('sports', [{}])[0].get('leagues', [{}])[0].get('teams', []):
            t = team['team']
            name = t['displayName']
            tid = t['id']
            maps[f'espn_{sport}_teams'][name] = tid

            roster_url = f"https://site.api.espn.com/apis/site/v2/sports/{path}/teams/{tid}/roster"
            rr = requests.get(roster_url, timeout=10)
            roster = rr.json()
            for athlete in roster.get('athletes', []):
                player = athlete['athlete']
                pname = player['fullName']
                pid = player['id']
                maps['players'][f"{pname} ({sport.upper()})"] = pid

    # NHL
    r = requests.get("https://api-web.nhle.com/v1/teams")
    teams = r.json().get('teams', [])
    for team in teams:
        name = team['name']
        tid = team['id']
        maps['nhl_teams'][name] = tid

        roster_url = f"https://api-web.nhle.com/v1/roster/{team['triCode']}/current"
        rr = requests.get(roster_url)
        roster = rr.json()
        for pos in roster.get('roster', []):
            player = pos['person']
            pname = player['fullName']
            pid = player['id']
            maps['players'][f"{pname} (NHL)"] = pid

    with open('all_ids.json', 'w') as f:
        json.dump(maps, f, indent=2)
    print(f"ID map updated: {datetime.now()}")

if __name__ == "__main__":
    scrape_all_ids()
