# Apportionment Method Comparator

Python script to compare apportionment methods. This script has been tuned for the data from Polish 2023 elections, but
it could be adapted to other election data in non-First-Past-The-Post elections.

## Features

- **Filtering Votes**: The script filters votes based on a national threshold (the percentage of total national votes
  that a party must reach, to be eligible for any seats). In order to simulate the Polish electoral system, three
  thresholds are defined:
  - _Coalition Threshold_: applies to coalition committees (by default 8%),
  - _Minority Threshold_: applies to national minority committees (by default 0%),
  - _Base Threshold_: applies to generic committees (by default 5%)
- **Apportionment Methods**: The following apportionment methods are implemented:
  - \*Greatest divisor methods\*\*: D'Hondt and Sainte-Laguë methods,
  - _Largest remainder methods_: Hare, Droop, Hagenbach-Bischoff, and Imperiali quota.

## Usage

```bash
python main.py <directory>
```

Where `<directory>` is the path to the directory containing the `votes.json` and `seats.json` files (see [Data](#data)
below).

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

### Processing Data

There is a `data-processor.py` file in the `data` directory that can be used to generate the required data files from
the raw data provided by the National Electoral Commission of Poland. The script takes one positional argument:

```bash
python data-processor.py <directory>
```

Where `<directory>` is the path to the directory containing the `config.json` file. The format of the config file should
match the following:

```json
{
  "seatsFile": {
    "filename": "Name of the file containing the number of seats for each district, with respect to the directory argument",
    "delimiter": "Delimiter used in the file",
    "encoding": "Encoding used in the file",
    "constituencyHeader": "The header on the column containing the constituency identifiers",
    "seatsHeader": "The header on the column containing the number of seats"
  },
  "votesFile": {
    "filename": "Name of the file containing the number of seats for each district, with respect to the directory argument",
    "delimiter": "Delimiter used in the file",
    "encoding": "Encoding used in the file",
    "constituencyHeader": "The header on the column containing the constituency identifiers",
    "committeePatter": "The regex pattern used to identify columns containing committee information"
  }
}
```

When run, the data processor will generate the `votes.json` and `seats.json` files in the same directory as the config.

## License

[MIT](LICENSE.md)
