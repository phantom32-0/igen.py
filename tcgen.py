import random

def generate_tc_no():
    digits = []
    digits.append(random.randint(1, 9))
    for i in range(1, 9):
        digits.append(random.randint(0, 9))
    digits.append((sum(digits[::2]) * 7 - sum(digits[1::2])) % 10)
    digits.append(sum(digits) % 10)
    tc_no = ''.join(map(str, digits))
    return tc_no

if __name__ == "__main__":
    print(generate_tc_no())
