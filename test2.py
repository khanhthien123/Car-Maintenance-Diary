cases = int(input())

problems = []

for i in range(cases):
    case = [
        [0, 0, 0],
        [0, None, 0],
        [0, 0, 0]
    ]
    first_line = input().split()
    for j in range(3):
        case[0][j] = int(first_line[j])
        
    second_line = input().split()
    case[1][0] = second_line[0]
    case[1][2] = second_line[1]
    
    third_line = input().split()
    for j in range(3):
        case[2][j] = int(third_line[j])
    
    problems.append(case)

def solve(case):
    #case is a 3x3 array
    possible_nums = [0] * 4
    possible_nums[0] = (case[0][0] + case[2][2]) / 2
