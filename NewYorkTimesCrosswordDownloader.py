import logging
import requests
import os
import time

from datetime import date, timedelta


class NewYorkTimesCrosswordDownloader:
    CONSTANTS = {
        "PUZZLES_API_URL": "https://www.nytimes.com/svc/crosswords/v3//puzzles.json",
        "PUZZLE_DOWNLOAD_URI": "https://www.nytimes.com/svc/crosswords/v2/puzzle/{puzzle_id}.pdf",
    }

    def __init__(self, save_dir: str = "./crosswords/"):
        self.save_dir = save_dir
        logging.info(f"Creating {save_dir}")
        os.makedirs(save_dir, exist_ok=True)
        self.cookies = self.load_cookies()

    @staticmethod
    def load_cookies():
        with open("nyt_cookies.txt") as file:
            cookies = file.readline().strip()
        return cookies

    def get_crossword_ids_for_date_range(self, start_date: date, end_date: date = None):
        params = {
            "publish_type": "daily",
            "sort_order": "asc",
            "sort_by": "print_date",
            "date_start": start_date.strftime("%Y-%m-%d"),
        }
        with requests.get(self.CONSTANTS["PUZZLES_API_URL"], params=params) as response:
            response.raise_for_status()
            return {
                puz["print_date"]: puz["puzzle_id"]
                for puz in response.json()["results"]
            }

    def download_crossword(self, puzzle_date: date, puzzle_id):
        filename = f"/{puzzle_date.strftime('%Y-%m-%d_%A')}.pdf"
        filepath = self.save_dir + filename
        if os.path.exists(filepath):
            logging.info(
                f"{filename} already exists in {self.save_dir}, skipping download"
            )
            return

        logging.info(f"Downloading {filename}")
        puzzle_url = self.CONSTANTS["PUZZLE_DOWNLOAD_URI"].format(puzzle_id=puzzle_id)

        with requests.get(puzzle_url, headers={"Cookie": self.cookies}) as response:
            with open(filepath, mode="wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        return filepath

    def get_puzzles(self, start_date):
        puzzles = self.get_crossword_ids_for_date_range(start_date)
        downloaded_files = []
        for puzzle_date, puzzle_id in puzzles.items():
            print(f"Downloading puzzle for {puzzle_date}")
            filepath = self.download_crossword(
                date.fromisoformat(puzzle_date), puzzle_id
            )
            if filepath:
                downloaded_files.append(filepath)
            # To prevent rate limiting / bot detection:
            time.sleep(5)
            print("Pausing for 5 seconds to avoid rate limiter")

        return downloaded_files
