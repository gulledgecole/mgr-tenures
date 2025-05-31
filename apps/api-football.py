import os
import http.client
import glob
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

    def get_leagues_by_country(self, country_code):
        """Retrieve leagues for a specific country"""
        params = {"id": country_code}
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
        params = {"team": team_id}
        coach_data = self._get_request("coachs", params)
        if coach_data:
            return coach_data
        else:
            return "No coach data here!"


def split_iso_datetime(iso_str: str) -> tuple[str, str]:
    """
    Given an ISO timestamp like "2021-08-14T11:30:00+00:00",
    return (date_str, time_str) → ("2021-08-14", "11:30:00").
    GPT as hell but works lol
    """
    dt = datetime.fromisoformat(iso_str)
    return dt.date().isoformat(), dt.time().isoformat()


def return_results(api_key, league_id):
    leagues_api = LeaguesAPI(api_key)
    fixtures_api = FixturesAPI(api_key)
    print(f"Fetching Fixtures (ID {league_id})...")
    seasons = [
        # Only supported seasons for free trial..
        "2021",
        "2022",
        "2023",
    ]
    fixture_data = []
    for season in seasons:
        fixtures = fixtures_api.get_fixtures_by_league(league_id, season)
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
                        "fixture_id": fixture["fixture"]["id"],
                        "home_team": fixture["teams"]["home"]["name"],
                        "home_team_id": fixture["teams"]["home"]["id"],
                        "away_team_name": fixture["teams"]["away"]["name"],
                        "away_team_id": fixture["teams"]["away"]["id"],
                        "date": date,
                        "time": time,
                        "home_winner": home_winner,
                        "away_winner": away_winner,
                        "home_tie": home_tie,
                        "away_tie": away_tie,
                        "home_goals": fixture["goals"]["home"],
                        "away_goals": fixture["goals"]["away"],
                        "league_id": fixture["league"]["id"],
                        "league_name": fixture["league"]["name"],
                        "league_season": fixture["league"]["season"],
                        "round": fixture["league"]["round"],
                    }
                )

        else:
            print(
                f"No fixtures data found for {fixture['league']['name']} {season} season!."
            )

        df = pd.DataFrame(fixture_data)
        print(df.head())
        file_name = f"data/fixtures_{fixture['league']['name']}_{fixture['league']['season']}.csv"

        # Save to CSV
        df.to_csv(file_name, index=False)
        print(
            f"Fixture data saved for:{fixture['league']['name']} for {fixture['league']['season']} season! "
        )


def return_coachs(api_key):
    coachs_api = CoachsAPI(api_key)
    results_df = pd.read_csv(
        "/Users/colegulledge/code/mgr-tenures/fixtures_premier_league.csv"
    )
    team_ids = results_df["home_team_id"].unique().tolist()
    print(len(team_ids))
    rows = []
    for team in team_ids:
        coachs = coachs_api.get_coachs(team)
        for coach in coachs["response"]:
            coach_id = coach["id"]
            coach_name = coach["name"]
            first_name = coach["firstname"]
            last_name = coach["lastname"]
            nationality = coach.get("nationality")
            birthdate = coach.get("birth", {}).get("date")
            for tenure in coach.get("career", []):
                team_id = tenure["team"]["id"]
                team_name = tenure["team"]["name"]
                start_date = tenure["start"]
                end_date = tenure["end"]
                if not end_date:
                    end_date = "Current"
                rows.append(
                    {
                        "coach_id": coach_id,
                        "coach_name": coach_name,
                        "first_name": first_name,
                        "last_name": last_name,
                        "nationality": nationality,
                        "birthdate": birthdate,
                        "team_id": team_id,
                        "team_name": team_name,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                )
    df = pd.DataFrame(rows)

    df.to_csv("coaches_tenures_extended.csv", index=False)


if __name__ == "__main__":
    # Replace with your API key
    api_key = os.getenv("API_FOOTBALL_KEY")
    # league_api = LeaguesAPI(api_key)
    # league_data = league_api.get_leagues_by_country("45")
    # print(league_data)
    # return_coachs(api_key)
    # leagues =  ["3", "45", "528", "40", "48"]
    #return_results(api_key, "48")
    # for league in leagues:
    #     return_results(api_key, league)
    # results_df = pd.read_csv(
    #     "/Users/colegulledge/code/mgr-tenures/fixtures_premier_league.csv"
    # )
    # team_ids = len(results_df["home_team_id"].unique().tolist())
    # print(team_ids)
    # df = pd.read_csv(
    #     "/Users/colegulledge/code/mgr-tenures/coaches_tenures_extended.csv"
    # )
    # print(len(df["coach_id"].unique().tolist()))

    csv_files = glob.glob("data/*.csv")

    # 2. Initialize an empty set to collect unique home_team_id values
    unique_ids = set()

    # 3. Loop through each file, read it, and update the set
    for file in csv_files:
        df = pd.read_csv(file)
        if "home_team_id" in df.columns:
            # .dropna() in case there are missing values
            unique_ids.update(df["home_team_id"].dropna().unique())

    # 4. Convert back to a list (if you need ordering, you can sort here)
    unique_home_team_ids = list(unique_ids)

    print((unique_home_team_ids))
