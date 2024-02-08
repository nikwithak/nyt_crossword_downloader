import os
import subprocess
import sys

from NewYorkTimesCrosswordDownloader import NewYorkTimesCrosswordDownloader
from datetime import date, timedelta


def get_files_on_tablet():
    os.system("rcu --autoconnect --cli --list-documents --no-compat-check")


def get_collections():
    raw_collections = (
        subprocess.check_output(
            ["rcu", "--autoconnect", "--cli", "--list-collections", "--no-compat-check"]
        )
        .decode()
        .split("\n")
    )
    collections = {}
    for collection in raw_collections:
        values = collection.split("\t")
        if len(values) > 1:
            collections[values[1]] = values[0]
    return collections


def get_files():
    raw_output = (
        subprocess.check_output(
            ["rcu", "--autoconnect", "--cli", "--list-documents", "--no-compat-check"]
        )
        .decode()
        .split("\n")
    )
    files = []
    for file_info in raw_output:
        values = file_info.split("\t")
        if len(values) > 1:
            files.append(values[1])
    return files


def send_to_remarkable(filepath, collection=None):
    command = ["rcu", "--autoconnect", "--cli", "--no-compat-check"]
    if collection:
        command.append("--upload-doc-to")
        command.append(filepath)
        command.append(collection)
    else:
        command.append("--upload-doc")
        command.append(filepath)
    subprocess.call(command)


if __name__ == "__main__":
    new_files = NewYorkTimesCrosswordDownloader().get_puzzles(
        date.today() - timedelta(days=14)
    )
    if len(sys.argv) > 1 and sys.argv.get(1) == "--remarkable":
        try:
            print(
                "WARNING: Support for syncing to remarkable is experimental. It requires RCU, and has not been tested with the latest versions of "
            )
            collection_id = get_collections().get("Crosswords", None)
            print(f"collection_id = {collection_id}")
            for file in new_files:
                print(f"Sending file {file} to remarkable")
                send_to_remarkable(file, collection_id)
        except Exception as e:
            print(f"Unable to sync with Remarkable: {e}")
    print(f"Finished downloading crosswords: {len(new_files)} Downloaded.")
