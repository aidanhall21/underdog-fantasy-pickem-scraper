import requests
import pandas as pd
import json
import os

class UnderdogScraper:
    def __init__(self):
        self.config = None
        self.underdog_props = None

        self.load_config()

    def load_config(self):
        with open(
            os.path.join(os.path.dirname(__file__), "config.json"),
            encoding="utf-8-sig",
        ) as json_file:
            self.config = json.load(json_file)

    def fetch_data(self):
        ud_pickem_response = requests.get(self.config["ud_pickem_url"], headers=self.config["headers"])

        if ud_pickem_response.status_code != 200:
            raise Exception("Request failed")

        pickem_data = json.loads(ud_pickem_response.text)

        return pickem_data

    def combine_data(self, pickem_data):
        players = pd.DataFrame(pickem_data["players"])
        appearances = pd.DataFrame(pickem_data["appearances"])
        # games = pd.DataFrame(pickem_data["games"])
        over_under_lines = pd.DataFrame(pickem_data["over_under_lines"])

        return players, appearances, over_under_lines
    
    def apply_name_corrections(self, df):
        name_corrections = {
            # ... If you're working with other data sets use this dictionary match names
        }
        df["full_name"] = df["full_name"].map(name_corrections).fillna(df["full_name"])
        return df

    def process_data(self, players, appearances, over_under_lines):
        players = players.rename(columns={"id": "player_id"})
        appearances = appearances.rename(columns={"id": "appearance_id"})

        player_appearances = players.merge(appearances, on=["player_id", "position_id", "team_id"], how="left")

        over_under_lines = over_under_lines.reset_index(drop=True)
        over_under_lines_expanded = over_under_lines.explode("options")
        
        options_df = pd.json_normalize(over_under_lines_expanded["options"])
        
        over_under_lines_expanded = pd.concat([over_under_lines_expanded.drop("options", axis=1).reset_index(drop=True), 
                                            options_df.reset_index(drop=True)], axis=1)

        over_under_lines_expanded["appearance_id"] = over_under_lines_expanded["over_under"].apply(lambda x: x["appearance_stat"]["appearance_id"])
        over_under_lines_expanded["stat_name"] = over_under_lines_expanded["over_under"].apply(lambda x: x["appearance_stat"]["stat"])

        columns_to_remove = ['expires_at', 'live_event', 'live_event_stat']
        over_under_lines_expanded = over_under_lines_expanded.drop(columns=columns_to_remove, errors='ignore')

        over_under_lines_expanded["choice"] = over_under_lines_expanded["choice"].map({"lower": "under", "higher": "over"}).fillna(over_under_lines_expanded["choice"])

        underdog_props = player_appearances.merge(over_under_lines_expanded, on="appearance_id", how="left", suffixes=("", "_over_under"))
        underdog_props["full_name"] = underdog_props["first_name"] + " " + underdog_props["last_name"]

        underdog_props = self.apply_name_corrections(underdog_props)

        return underdog_props

    def filter_data(self, df):
        # df = df[df["sport_id"].isin(["MLB"])]
        df = df[df["status"] != "suspended"]

        columns_to_remove = ['country', 'image_url', 'badges', 'lineup_status_id', 'match_id', 'match_type', 'over_under', 'rank', 'status']
        df = df.drop(columns=columns_to_remove, errors='ignore')
        df = df.reset_index(drop=True)

        return df

    def scrape(self):
        all_pickem_data = self.fetch_data()
        players, appearances, over_under_lines = self.combine_data(all_pickem_data)
        processed_props = self.process_data(players, appearances, over_under_lines)
        self.underdog_props = self.filter_data(processed_props)

        #print(self.underdog_props)

        # Save the DataFrame as a CSV file
        self.underdog_props.to_csv('underdog_props.csv', index=False)
        print("Data saved to underdog_props.csv")

# Usage example:
#scraper = UnderdogScraper()
#scraper.scrape()