import requests
import pandas as pd


def fetch_matchweek_standings(
    season_id: int, competition_id: int, matchday: str
) -> pd.DataFrame:
    """
    Fetch the standings table for a given matchday via Pulselive’s JSON API,
    then convert it into a pandas DataFrame.
    """
    url = "https://footballapi.pulselive.com/football/standings"
    # url = "https://footballapi.pulselive.com/football/fixtures?comps=1&compSeasons=1&statuses=L&gameweekNumbers=1-6"
    # https://footballapi.pulselive.com/football/fixtures?comps=1&compSeasons=1&statuses=L&gameweekNumbers=1-6
    params = {
        "comps": competition_id,  # 1 == Premier League
        "compSeasons": season_id,
        "gameweekNumbers": matchday,
        "pageSize": 20,  # there are 20 teams in the PL
    }
    headers = {
        "Origin": "https://www.premierleague.com",
        "Referer": "https://www.premierleague.com/tables",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/100.0.4896.127 Safari/537.36",
    }
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    season = data.get("compSeason", {}).get("label")
    prefix, matchweek = matchday.split("-", 1)
    entries = data.get("tables", [])[0].get("entries", [])
    rows = []

    for entry in entries:
        # 1) Team info

        team_info = entry["team"]
        team_name = team_info["name"]
        team_id = team_info["id"]

        # 2) League position
        position = entry.get("position")

        # 3) Overall stats
        overall = entry.get("overall", {})
        played = overall.get("played")
        won = overall.get("won")
        drawn = overall.get("drawn")
        lost = overall.get("lost")
        goals_for = overall.get("goalsFor")
        goals_against = overall.get("goalsAgainst")
        goal_diff = overall.get("goalsDifference")
        points = overall.get("points")

        # 4) Home stats (optional; shown here for completeness)
        home = entry.get("home", {})
        home_played = home.get("played")
        home_won = home.get("won")
        home_drawn = home.get("drawn")
        home_lost = home.get("lost")
        home_goals_for = home.get("goalsFor")
        home_goals_against = home.get("goalsAgainst")
        home_goal_diff = home.get("goalsDifference")
        home_points = home.get("points")

        # 5) Away stats
        away = entry.get("away", {})
        away_played = away.get("played")
        away_won = away.get("won")
        away_drawn = away.get("drawn")
        away_lost = away.get("lost")
        away_goals_for = away.get("goalsFor")
        away_goals_against = away.get("goalsAgainst")
        away_goal_diff = away.get("goalsDifference")
        away_points = away.get("points")

        # 6) Any annotations (e.g. qualification or relegation markers)
        annotations = entry.get("annotations", [])
        # Concatenate types into a comma‐separated string (if you want)
        annotation_types = [ann.get("type") for ann in annotations]
        annotation_destinations = [ann.get("destination") for ann in annotations]

        # 7) Ground (stadium) info (optional)
        ground = entry.get("ground", {})
        stadium_name = ground.get("name")
        stadium_city = ground.get("city")

        # 8) Build one “row” dict
        row = {
            "season": season,
            "match_week": matchweek,
            "team_id": team_id,
            "team_name": team_name,
            "position": position,
            # Overall
            "played": played,
            "won": won,
            "drawn": drawn,
            "lost": lost,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "goal_difference": goal_diff,
            "points": points,
            # Home
            "home_played": home_played,
            "home_won": home_won,
            "home_drawn": home_drawn,
            "home_lost": home_lost,
            "home_goals_for": home_goals_for,
            "home_goals_against": home_goals_against,
            "home_goal_difference": home_goal_diff,
            "home_points": home_points,
            # Away
            "away_played": away_played,
            "away_won": away_won,
            "away_drawn": away_drawn,
            "away_lost": away_lost,
            "away_goals_for": away_goals_for,
            "away_goals_against": away_goals_against,
            "away_goal_difference": away_goal_diff,
            "away_points": away_points,
            "annotation_types": ",".join(annotation_types),
            "annotation_destinations": ",".join(annotation_destinations),
            "stadium_name": stadium_name,
            "stadium_city": stadium_city,
        }

        rows.append(row)

    df = pd.DataFrame(rows)
    df.fillna(pd.NA, inplace=True)
    df.replace("", pd.NA, inplace=True)
    return df


def fetch_full_season(
    season_id: int = 1, competition_id: int = 1, max_matchday: str = "1-38"
):
    """
    Loop from matchday 1 to matchday max_matchday and collect standings for each.
    Returns a single DataFrame with all matchweeks.
    """
    try:
        prefix, max_md_s = max_matchday.split("-", 1)
        max_md = int(max_md_s)
    except ValueError:
        raise ValueError(
            f"max_matchday_str must be 'X-N' (e.g. '1-38'), got '{max_matchday}'"
        )

    all_dfs = []
    for md in range(1, max_md + 1):
        gameweek_range = f"{prefix}-{md}"
        try:
            df_md = fetch_matchweek_standings(season_id, competition_id, gameweek_range)
            # print(df_md)
            all_dfs.append(df_md)
            print(f"Fetched matchday {md}")
        except Exception as e:
            print(f"Skipped matchday {md}: {e}")
    return pd.concat(all_dfs, ignore_index=True)


if __name__ == "__main__":
    # Super weird, its sequential... until its not in 2014. funtimes.
    season_map = {
        "1992-93": 1,
        "1993-94": 2,
        "1994-95": 3,
        "1995-96": 4,
        "1996-97": 5,
        "1997-98": 6,
        "1998-99": 7,
        "1999-00": 8,
        "2000-01": 9,
        "2001-02": 10,
        "2002-03": 11,
        "2003-04": 12,
        "2004-05": 13,
        "2005-06": 14,
        "2006-07": 15,
        "2007-08": 16,
        "2008-09": 17,
        "2009-10": 18,
        "2010-11": 19,
        "2011-12": 20,
        "2012-13": 21,
        "2013-14": 22,
        "2014-15": 27,
        "2015-16": 42,
        "2016-17": 54,
        "2017-18": 79,
        "2018-19": 210,
        "2019-20": 274,
        "2020-21": 363,
        "2021-22": 418,
        "2022-23": 489,
        "2023-24": 578,
        "2024-25": 719,
    }
    for season, season_id in season_map.items():
        df = fetch_full_season(
            season_id=season_id, competition_id=1, max_matchday="1-38"
        )
        df.to_csv(
            f"data/premier_league_standings_weekly_scrapped/{season}_standings.csv",
            index=False,
        )
