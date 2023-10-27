import argparse
import csv
import os


def read_directory():
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
    with open(
        os.path.join(folder_path, "constituencies.csv"), "r", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file, delimiter=";")
        return {int(row["Numer okręgu"]): int(row["Liczba mandatów"]) for row in reader}


def get_results(folder_path: str) -> dict[int, dict[str, int]]:
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
