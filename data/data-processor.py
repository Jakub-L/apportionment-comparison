import argparse
import csv
import os


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


def get_seats(folder_path: str) -> dict[int, int]:
    """
    Reads the 'constituencies.csv' file located in the specified folder path and returns a dictionary
    with the number of seats for each constituency.

    Args:
        folder_path (str): The path to the folder containing the 'constituencies.csv' file.

    Returns:
        dict[int, int]: A dictionary with the number of seats for each constituency, where the key is
        the constituency number and the value is the number of seats.
    """
    with open(
        os.path.join(folder_path, "constituencies.csv"), "r", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file, delimiter=";")
        return {int(row["Numer okręgu"]): int(row["Liczba mandatów"]) for row in reader}


def get_results(folder_path: str) -> dict[int, dict[str, int]]:
    """
    Reads a CSV file containing election results and returns a dictionary of dictionaries.
    The outer dictionary has keys representing the constituency number, and the values are
    inner dictionaries. The inner dictionaries have keys representing the committee name and
    values representing the number of votes received by that committee in the constituency.

    Args:
        folder_path (str): The path to the folder containing the CSV file.

    Returns:
        dict[int, dict[str, int]]: A dictionary of dictionaries representing the election results.
    """
    with open(
        os.path.join(folder_path, "votes.csv"), "r", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file, delimiter=";")
        return {
            int(row["Nr okręgu"]): {
                key: int(row[key] or 0) for key in row if key.startswith("KOMITET")
            }
            for row in reader
        }


def main():
    directory = read_directory()
    seats = get_seats(directory)
    results = get_results(directory)


if __name__ == "__main__":
    main()
