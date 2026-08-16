"""x = int(input())
y = int(input())

print("\n"*y, end="")
print((int(x) - 1)*" " + "X")
print("\n"*(37-y))"""

"""
with open("pi_digits.txt", "r") as f:
    with open("new_digit.txt", "w") as new_f:
        for line in f.readlines():
            if line == "\n":
                continue

            line = line.replace(" ", "")
            new_f.write(line[:line.index(":")] + "\n")"""


PI_seq = [""]
count = 0
i = 0
with open("pi_digits.txt", "r") as f:
    for line in f.readlines():
        count += 1
        PI_seq[i] += line
        if count == 80:
            i += 1
            count = 0
            PI_seq.append("")
PI = PI_seq[0]
print(len(PI))