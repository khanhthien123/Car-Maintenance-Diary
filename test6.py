x = "abc"

def check_pal_1(s):
    n = len(s)
    i = 0
    j = n - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True

def check_pal_2(s):
    return s == s[::-1]

test_cases = ["abcba", "abba", "", "abcd", "racecar"]

for case in test_cases:
    print("self-built: ", check_pal_1(case))
    print("built-in: ", check_pal_2(case))
    print("-------------")