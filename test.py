def filter_matches(matches):
    horizontal_matches = []
    vertical_matches = []

    for match in matches:
        if all(x == match[0][0] for x, y in match):
            horizontal_matches.append(match)
        elif all(y == match[0][1] for x, y in match):
            vertical_matches.append(match)

    return horizontal_matches, vertical_matches

# Example matches list
matches = [
    [(1, 0), (1, 1), (1, 2), (2, 2)],
    [(1, 4), (2, 4), (3, 4)]
]

horizontal_matches, vertical_matches = filter_matches(matches)

print("Horizontal matches:", horizontal_matches)
print("Vertical matches:", vertical_matches)
