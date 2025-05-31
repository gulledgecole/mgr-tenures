import os
import http.client
import pandas as pd
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class FootballAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": self.api_key,
        }

    def _get_request(self, endpoint, params=None):
        """Generic GET request handler"""
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}", headers=self.headers, params=params
            )
            response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
            return response.json()  # Return JSON data if request is successful
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None


class LeaguesAPI(FootballAPI):
    def __init__(self, api_key):
        super().__init__(api_key)

    def get_leagues_by_country(self, country_code, league):
        """Retrieve leagues for a specific country"""
        params = {"country": country_code}
        leagues_data = self._get_request("leagues", params)
        if leagues_data:
            return leagues_data["response"]
        else:
            return []


class FixturesAPI(FootballAPI):
    def __init__(self, api_key):
        super().__init__(api_key)

    def get_fixtures_by_league(self, league_id, season):
        """Retrieve fixtures for a given league and season"""
        params = {"league": league_id, "season": season}
        fixtures_data = self._get_request("fixtures", params)
        if fixtures_data:
            return fixtures_data["response"]
        else:
            return []
        
class CoachsAPI(FootballAPI): 
    def __init__(self, api_key):
        super().__init__(api_key)
    
    def get_coachs(self, team_id): 
        params =  {"team" : team_id}
        coach_data = self._get_request("coachs", params)
        if coach_data: 
            return coach_data
        else: 
            return "No coach data here!"
        
def split_iso_datetime(iso_str: str) -> tuple[str, str]:
    """
    Given an ISO timestamp like "2021-08-14T11:30:00+00:00",
    return (date_str, time_str) → ("2021-08-14", "11:30:00").
    """
    dt = datetime.fromisoformat(iso_str)
    return dt.date().isoformat(), dt.time().isoformat()



def return_results(api_key):
    leagues_api = LeaguesAPI(api_key)
    fixtures_api = FixturesAPI(api_key)
    premier_league_id = "39"
    print(f"Fetching Fixtures for Premier League (ID {premier_league_id})...")
    seasons = ["2021", "2022", "2023",]
    fixture_data = []
    for season in seasons:
        fixtures = fixtures_api.get_fixtures_by_league(premier_league_id, season)
        if fixtures:
            for fixture in fixtures:
                home_winner = fixture["teams"]["home"]["winner"]
                away_winner = fixture["teams"]["away"]["winner"]
                date, time = split_iso_datetime(fixture["fixture"]["date"])
                if not home_winner and not away_winner:
                    # Both teams did not win, so it's a tie
                    home_tie = True
                    away_tie = True
                    home_winner = (
                        False  # Explicitly setting both to False to indicate no winner
                    )
                    away_winner = (
                        False  # Explicitly setting both to False to indicate no winner
                    )
                else:
                    # If either team won, it's not a tie
                    home_tie = False
                    away_tie = False

                fixture_data.append(
                    {
                        "Fixture_ID": fixture["fixture"]["id"],
                        "Home_Team": fixture["teams"]["home"]["name"],
                        "Home_Team_ID": fixture["teams"]["home"]["id"],
                        "Away_Team_Name": fixture["teams"]["away"]["name"],
                        "Away_Team_ID": fixture["teams"]["away"]["id"],
                        "Date": date,
                        "Time" : time,
                        "Home_Winner": home_winner,
                        "Away_Winner": away_winner,
                        "Home_Tie": home_tie,
                        "Away_Tie": away_tie,
                        "Home_Goals": fixture["goals"]["home"],
                        "Away_Goals": fixture["goals"]["away"],
                        "League_ID": fixture["league"]["id"],
                        "League_Season": fixture["league"]["season"],
                    }
                )

        else:
            print(f"No fixtures data found for {season}.")
        # Create a DataFrame and display or save the data
    df = pd.DataFrame(fixture_data)
    print(df.head())  # Display first few fixtures

    # Save to CSV
    df.to_csv("fixtures_premier_league.csv", index=False)
    print("Fixture data saved to 'fixtures_premier_league.csv'")

def return_coachs(api_key): 
    coachs_api = CoachsAPI(api_key)
    results_df = pd.read_csv("/Users/colegulledge/code/mgr-tenures/fixtures_premier_league.csv")
    team_ids = results_df["Home_Team_ID"].unique().tolist()
    print(len(team_ids))
    rows = []
    for team in team_ids: 
        coachs = coachs_api.get_coachs(team)
        for coach in coachs['response']:
            coach_id = coach["id"]
            coach_name = coach['name']
            nationality = coach.get('nationality')
            birthdate = coach.get('birth', {}).get('date')
            for tenure in coach.get('career', []):
                team_id = tenure['team']['id']
                team_name = tenure['team']['name']
                start_date = tenure['start']
                end_date = tenure['end']
                if not end_date: 
                    end_date = "Current"
                rows.append({
                    'coach_id' : coach_id,
                    'coach_name': coach_name,
                    'nationality': nationality,
                    'birthdate': birthdate,
                    'team_id': team_id,
                    'team_name': team_name,
                    'start_date': start_date,
                    'end_date': end_date
                })
    df = pd.DataFrame(rows)

    df.to_csv('coaches_tenures_extended.csv', index=False)

def merge_coach_team(): 




if __name__ == "__main__":
    # Replace with your API key
    api_key = os.getenv("API_FOOTBALL_KEY")
    #return_coachs(api_key)
    #return_results(api_key)
    results_df = pd.read_csv("/Users/colegulledge/code/mgr-tenures/fixtures_premier_league.csv")
    team_ids = len(results_df["Home_Team_ID"].unique().tolist())
    print(team_ids)
    df = pd.read_csv("/Users/colegulledge/code/mgr-tenures/coaches_tenures_extended.csv")
    print(len(df["coach_id"].unique().tolist()))
