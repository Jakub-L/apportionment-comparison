import argparse
import collections
import json
import os
import pprint


def read_arguments():
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
    parser.add_argument(
        "--coalition-threshold",
        "-ct",
        type=float,
        default=0.08,
        help="Electoral threshold for coalitions",
    )
    parser.add_argument(
        "--minority-threshold",
        "-mt",
        type=float,
        default=0,
        help="Electoral threshold for minority committees",
    )
    parser.add_argument(
        "--base-threshold",
        "-bt",
        type=float,
        default=0.05,
        help="Electoral threshold for generic committees",
    )
    args = parser.parse_args()
    return args


def filter_by_national_threshold(
    votes: dict[str, dict[str, int]],
    committee_threshold: float,
    coalition_threshold: float,
    minority_threshold: float,
) -> dict[str, int]:
    """
    Filters a dictionary of votes by a threshold.

    Args:
        votes (dict[str, int]): A dictionary containing the number of votes received by each committee.
        committee_threshold (int): The vote threshold to be achieved by a party committee
        coalition_threshold (int): The vote threshold to be achieved by a coalition
        minority_threshold (int): The vote threshold to be achieved by a minority committee

    Returns:
        dict[str, int]: A dictionary containing the number of votes received by each committee that
        received at least the specified number of votes.
    """
    national_votes = collections.Counter()
    for _, results in votes.items():
        for committee, committee_votes in results.items():
            national_votes[committee] += committee_votes
    total_votes = sum(national_votes.values())
    filtered_results = {}

    for constituency, results in votes.items():
        filtered_results[constituency] = {}
        for committee, votes in results.items():
            if (
                (
                    "Koalicyjny" in committee
                    and national_votes[committee] > (coalition_threshold * total_votes)
                )
                or (
                    "Mniejszość" in committee
                    and national_votes[committee] > (minority_threshold * total_votes)
                )
                or (
                    "Koalicyjny" not in committee
                    and national_votes[committee] > (committee_threshold * total_votes)
                )
            ):
                filtered_results[constituency][committee] = votes

    return filtered_results


def greatest_divisor_method(
    votes: dict[str, int], seats: int, quotient_formula: callable
) -> dict[str, int]:
    """
    Calculates the number of seats won by each committee in a constituency using the greatest divisor method.

    Args:
        votes (dict[str, int]): A dictionary containing the number of votes received by each committee.
        seats (int): The number of seats to be allocated.
        quotient_formula (callable): A function that calculates the quotient for a committee.

    Returns:
        dict[str, int]: A dictionary containing the number of seats won by each committee.
    """

    seats_per_committee = {committee: 0 for committee in votes}
    while seats > 0:
        committee = max(
            votes, key=lambda c: quotient_formula(votes[c], seats_per_committee[c])
        )
        seats_per_committee[committee] += 1
        seats -= 1
    return seats_per_committee


def d_hondt_formula(committee_votes: int, current_committee_seats: int) -> float:
    return committee_votes / (current_committee_seats + 1)


def sainte_lague_formula(committee_votes: int, current_committee_seats: int) -> float:
    return committee_votes / (2 * current_committee_seats + 1)


def largest_remainder_method(
    votes: dict[str, int], seats: int, quota_function: callable
) -> dict[str, int]:
    """
    Calculates the number of seats won by each committee in a constituency using the largest remainder method.

    Args:
        votes (dict[str, int]): A dictionary containing the number of votes received by each committee.
        seats (int): The number of seats to be allocated.
        quota_function (callable): A function that calculates the quota for a constituency.

    Returns:
        dict[str, int]: A dictionary containing the number of seats won by each committee.
    """
    quota = quota_function(sum(votes.values()), seats)
    seats_per_committee = {c: int(v / quota) for (c, v) in votes.items()}
    remainders = sorted(
        [
            (committee, votes / quota - seats_per_committee[committee])
            for (committee, votes) in votes.items()
        ],
        key=lambda r: r[1],
        reverse=True,
    )
    remaining_seats = seats - sum(seats_per_committee.values())
    for i in range(remaining_seats):
        comittee = remainders[i][0]
        seats_per_committee[comittee] += 1
    return seats_per_committee


def hare_quota(total_votes: int, seats: int) -> float:
    return total_votes / seats


def droop_quota(total_votes: int, seats: int) -> float:
    return int(total_votes / (seats + 1)) + 1


def hagenbach_bischoff_quota(total_votes: int, seats: int) -> float:
    return total_votes / (seats + 1)


def imperiali_quota(total_votes: int, seats: int) -> float:
    return total_votes / (seats + 2)


def count_national_seats(results: dict[int, dict[str, int]]) -> dict[str, int]:
    """
    Counts the number of national seats won by each committee based on the results of the constituencies.

    Args:
        results (dict(int, dict[str, int])): A dictionary containing the results of each constituency.
    Returns:
        dict[str, int]: A dictionary containing the number of national seats won by each committee.
    """

    counts = collections.Counter()
    for constituency in results:
        for committee in results[constituency]:
            counts[committee] += results[constituency][committee]
    return dict(counts)


def main():
    args = read_arguments()
    directory, coalition_threshold, minority_threshold, base_threshold = (
        args.directory,
        args.coalition_threshold,
        args.minority_threshold,
        args.base_threshold,
    )
    with open(os.path.join(directory, "votes.json"), "r", encoding="utf-8-sig") as file:
        votes = json.load(file)
    with open(os.path.join(directory, "seats.json"), "r", encoding="utf-8-sig") as file:
        seats = json.load(file)

    filtered_votes = filter_by_national_threshold(
        votes, base_threshold, coalition_threshold, minority_threshold
    )
    longest_committee_name = max(
        [
            len(committee)
            for constituency in filtered_votes
            for committee in filtered_votes[constituency]
        ]
    )

    apportionment_methods = [
        {
            "name": "D'Hondt",
            "method": greatest_divisor_method,
            "aux_function": d_hondt_formula,
        },
        {
            "name": "Sainte-Laguë",
            "method": greatest_divisor_method,
            "aux_function": sainte_lague_formula,
        },
        {
            "name": "Hare",
            "method": largest_remainder_method,
            "aux_function": hare_quota,
        },
        {
            "name": "Droop",
            "method": largest_remainder_method,
            "aux_function": droop_quota,
        },
        {
            "name": "Hagenbach-Bischoff",
            "method": largest_remainder_method,
            "aux_function": hagenbach_bischoff_quota,
        },
        {
            "name": "Imperiali",
            "method": largest_remainder_method,
            "aux_function": imperiali_quota,
        },
    ]

    for apportionment_method in apportionment_methods:
        name, method, aux_function = apportionment_method.values()
        seat_totals = count_national_seats(
            {
                constituency: method(
                    filtered_votes[constituency], seats[constituency], aux_function
                )
                for constituency in filtered_votes
            }
        )
        print("{:-^{width}}".format(name, width=longest_committee_name + 6))
        for committee in seat_totals:
            print(
                "{:<{width}} - {:>3}".format(
                    committee, seat_totals[committee], width=longest_committee_name
                )
            )
        print("\n")

    # pprint.pprint(results)


if __name__ == "__main__":
    main()
