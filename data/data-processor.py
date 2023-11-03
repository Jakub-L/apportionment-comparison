import argparse
import csv
import json
import os
import re


def read_directory():
    """
    Reads the directory path from the command line arguments and returns it.

    Returns:
    str: The path to the directory containing the files to process.
    """
    parser = argparse.ArgumentParser(
        prog="Election data processor",
        description="Converts the voting data (CSV) to a JSON file with just the vote counts per committee. Assumes the target directory will contain a file called 'votes.csv' with the vote counts per committee and a 'constituencies.csv' file containing the number of seats per constituency.",
    )
    parser.add_argument(
        "directory", help="The directory containing the files to process"
    )
    args = parser.parse_args()
    return args.directory


def get_seats(folder_path: str, config: dict[str, str]) -> dict[int, int]:
    """
    Reads the 'constituencies.csv' file located in the specified folder path and returns a dictionary
    with the number of seats for each constituency.

    Args:
        folder_path (str): The path to the folder containing the 'constituencies.csv' file.
        config (dict[str, str]): A dictionary containing the configuration for reading the CSV file.

    Returns:
        dict[int, int]: A dictionary with the number of seats for each constituency, where the key is
        the constituency number and the value is the number of seats.
    """
    with open(
        os.path.join(folder_path, config["filename"]), "r", encoding=config["encoding"]
    ) as file:
        reader = csv.DictReader(file, delimiter=config["delimiter"])
        return {
            int(row[config["constituencyHeader"]]): int(row[config["seatHeader"]])
            for row in reader
        }


def get_votes(folder_path: str, config: dict[str, str]) -> dict[int, dict[str, int]]:
    """
    Reads a CSV file containing election results and returns a dictionary of dictionaries.
    The outer dictionary has keys representing the constituency number, and the values are
    inner dictionaries. The inner dictionaries have keys representing the committee name and
    values representing the number of votes received by that committee in the constituency.

    Args:
        folder_path (str): The path to the folder containing the CSV file.
        config (dict[str, str]): A dictionary containing the configuration for reading the CSV file.

    Returns:
        dict[int, dict[str, int]]: A dictionary of dictionaries representing the election results.
    """
    pattern = re.compile(config["committeePattern"])
    with open(
        os.path.join(folder_path, config["filename"]), "r", encoding=config["encoding"]
    ) as file:
        reader = csv.DictReader(file, delimiter=config["delimiter"])
        return {
            int(row[config["constituencyHeader"]]): {
                key.title(): int(row[key] or 0) for key in row if pattern.match(key)
            }
            for row in reader
        }


def main():
    directory = read_directory()
    with open(os.path.join(directory, "config.json"), "r") as file:
        config = json.load(file)
    seats = get_seats(directory, config["seatsFile"])
    votes = get_votes(directory, config["votesFile"])

    with open(os.path.join(directory, "seats.json"), "w") as file:
        json.dump(seats, file, indent=4)
    with open(os.path.join(directory, "votes.json"), "w") as file:
        json.dump(votes, file, indent=4)


if __name__ == "__main__":
    main()
