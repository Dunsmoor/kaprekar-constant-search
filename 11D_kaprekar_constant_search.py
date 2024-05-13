import string
import pickle

BASE10_DIGITS = string.digits

def get_digits(x: int, base: int = 10) -> str:
    return ''.join([BASE10_DIGITS[int(d)] for d in str(abs(x)).zfill(11)])

def kaprekar_cycle(x: int, base: int = 10, max_iterations: int = 100) -> tuple[list[int], list[str]]:
    seen = []
    calculations = []
    for _ in range(max_iterations):
        if x in seen:
            cycle = seen[seen.index(x):]
            return cycle, calculations
        seen.append(x)
        desc = get_digits(x, base)
        desc_val = int(''.join(sorted(desc, reverse=True)))
        asc_val = int(''.join(sorted(desc)))
        new_x = desc_val - asc_val
        calculations.append(f"{desc_val} - {asc_val} = {new_x}")
        print(f"Iteration: {_+1}, Descending: {desc_val}, Ascending: {asc_val}, Result: {new_x}")  # Added print statement
        x = new_x
    return [], calculations

def is_kaprekar_constant(num: int, cycle: list[int]) -> bool:
    return len(cycle) == 1 and cycle[0] == num

known_constants = [495, 6174, 549945, 631764, 63317664, 97508421, 554999445, 864197532, 6333176664, 9753086421, 9975084201]

known_patterns = [
    [int(num) for num in pattern.split()]
    for pattern in [
        '09 81 63 27 45 09', '53955 59994 53955', '61974 82962 75933 63954 61974',
        '62964 71973 83952 74943 62964', '420876 851742 750843 840852 860832 862632 642654 420876',
        '7509843 9529641 8719722 8649432 7519743 8429652 7619733 8439552 7509843',
        '43208766 85317642 75308643 84308652 86308632 86326632 64326654 43208766',
        '64308654 83208762 86526432 64308654', '865296432 763197633 844296552 762098733 964395531 863098632 965296431 873197622 865395432 753098643 954197541 883098612 976494321 874197522 865296432',
        '8655264432 6431088654 8732087622 8655264432', '8653266432 6433086654 8332087662 8653266432',
        '8765264322 6543086544 8321088762 8765264322', '8633086632 8633266632 6433266654 4332087666 8533176642 7533086643 8433086652 8633086632',
        '9775084221 9755084421 9751088421 9775084221'
    ]
]

new_patterns = []
found_new_constant = False
checkpoint_interval = 1000000

try:
    with open('checkpoint.pkl', 'rb') as file:
        start_num = pickle.load(file)
        new_patterns = pickle.load(file)
except FileNotFoundError:
    start_num = 10060000000  # Start from 10060000000

try:
    for num in range(start_num, 10**11):
        print(f"Processing number: {num}")  # Added print statement
        cycle, calculations = kaprekar_cycle(num, base=10, max_iterations=100)
        if cycle:
            if is_kaprekar_constant(num, cycle):
                if num not in known_constants:
                    print(f"{num} is a new 11-digit Kaprekar's constant:")
                    for calculation in calculations:
                        print(calculation)
                    found_new_constant = True
                    break
            elif cycle not in known_patterns:
                pattern_str = ' → '.join(str(x) for x in cycle)
                print(f"{num} follows a new pattern: {pattern_str}")
                new_patterns.append(cycle)
        if num % checkpoint_interval == 0:
            with open('checkpoint.pkl', 'wb') as file:
                pickle.dump(num, file)
                pickle.dump(new_patterns, file)
            print(f"Checkpoint saved at num = {num}")
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Saving checkpoint and exiting...")
    with open('checkpoint.pkl', 'wb') as file:
        pickle.dump(num, file)
        pickle.dump(new_patterns, file)
    exit()

if not found_new_constant and not new_patterns:
    print("No new 11-digit Kaprekar's constants or patterns found.")
else:
    print("New patterns found:")
    for pattern in new_patterns:
        print(' → '.join(str(x) for x in pattern))
    if found_new_constant:
        while True:
            user_input = input("Press Enter to continue or 'q' to quit: ")
            if user_input.lower() == 'q':
                break
            else:
                found_new_constant = False
                continue