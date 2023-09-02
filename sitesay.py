from collections import defaultdict

# Read the input file and count occurrences of the 5th ID
count = defaultdict(int)
with open('kodlar.txt', 'r') as file:
    for line in file:
        ids = line.strip().split()
        if len(ids) >= 5:
            count[ids[4]] += 1

# Output the IDs and their counts in descending order
for id, frequency in sorted(count.items(), key=lambda x: x[1], reverse=True):
    print(f"{id} : {frequency}")

