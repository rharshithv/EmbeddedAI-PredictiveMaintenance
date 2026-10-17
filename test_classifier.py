
import subprocess

# Compile the C test program
subprocess.run(
    ["clang", "-O2", "test_classifier.c", "-o", "test_classifier"],
    check=True,
)

# Run the compiled program
result = subprocess.run(
    ["./test_classifier"],
    capture_output=True,
    text=True,
    check=True,
)

print(result.stdout)

# Expected classifications for the five boundary tests
expected = [
    "normal",
    "normal",
    "normal",
    "abnormal",
    "abnormal",
]

actual = [
    line.split(" -> ")[-1]
    for line in result.stdout.strip().splitlines()
]

print("Expected predictions:", expected)
print("Actual predictions:  ", actual)

if actual == expected:
    print("\nBOUNDARY TESTS: PASS")
else:
    print("\nBOUNDARY TESTS: FAIL")
