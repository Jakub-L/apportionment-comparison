# Apportionment Method Comparator

Python script to compare apportionment methods. This script has been tuned for the data from Polish 2023 elections, but it could be adapted to other election data in non-First-Past-The-Post elections.

## Features

- **Filtering Votes**: The script filters votes based on a national threshold (the percentage of total national votes that a party must reach, to be eligible for any seats). In order to simulate the Polish electoral system, three thresholds are defined:
  - *Coalition Threshold*: applies to coalition committees (by default 8%),
  - *Minority Threshold*: applies to national minority committees (by default 0%),
  - *Base Threshold*: applies to generic committees (by default 5%)
- **Apportionment Methods**: The following apportionment methods are implemented:
  - *Greatest divisor methods**: D'Hondt and Sainte-Laguë methods,
  - *Largest remainder methods*: Hare, Droop, Hagenbach-Bischoff, and Imperiali quota.

## Usage

```bash
python main.py <directory>
```

Where `<directory>` is the path to the directory containing the `votes.json` and `seats.json` files (see [Data](#data) below).

Additional supported flags and options:
- `-h`, `--help`: show help message and exit,
- `-ct VALUE`, `--coalition-threshold VALUE`: set coalition threshold to `VALUE`,
- `-mt VALUE`, `--minority-threshold VALUE`: set minority threshold to `VALUE`,
- `-bt VALUE`, `--base-threshold VALUE`: set base threshold to `VALUE`,


## Data
The main data directory is expected to contain two files in a specific format:
- `votes.json`: contains the votes for each committee in each district,
- `seats.json`: contains the number of seats for each district.

The format of each file is as follows:
```python
# Dictionary keyed by district number, with values being another dictionary
# keyed by committee name with values being the vote count.
type Votes = dict[str, dict[str, int]]

# Dictionary keyed by district number, with values being the number of seats.
type Seats = dict[str, int]
```

There is a `data-processor.py` file in the `data` directory that can be used to generate the required data files from the raw data provided by the National Electoral Commission of Poland.

## License

[MIT](LICENSE.md)
