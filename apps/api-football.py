import os
import http.client
import pandas as pd
import requests
from dotenv import load_dotenv

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


def main(api_key):
    leagues_api = LeaguesAPI(api_key)
    fixtures_api = FixturesAPI(api_key)
    premier_league_id = "39"
    print(f"Fetching Fixtures for Premier League (ID {premier_league_id})...")
    seasons = ["2021", "2022", "2023"]
    fixture_data = []
    for season in seasons:
        fixtures = fixtures_api.get_fixtures_by_league(premier_league_id, season)
        if fixtures:
            for fixture in fixtures:
                home_winner = fixture["teams"]["home"]["winner"]
                away_winner = fixture["teams"]["away"]["winner"]
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
                        "Date": fixture["fixture"]["date"],
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


if __name__ == "__main__":
    # Replace with your API key
    api_key = os.getenv("API_FOOTBALL_KEY")
    main(api_key)
