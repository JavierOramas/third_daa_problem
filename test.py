import random
import argparse
import numpy as np
from main import solve

def generator(n_tests: int):
    tests = []
    for i in range(n_tests):
        n_persons = random.randint(5, 100)
        k = random.randint(3, n_persons-1)
        
        persons = []
        for i in range(n_persons):
            n_edges = random.randint(0, n_persons-1)
            
            edges = np.random.choice(a=n_persons, replace=False, size=n_edges).tolist()
            
            if i in edges:
                edges.remove(i)
            
            persons.append({"id":i, "edges":edges})

        tests.append((persons,k))
    return tests

def check(people, result):
    ids  = set([p['id'] for p in people])
    id_to_check = ids - set(result)
    to_check = [p for p in people if p['id'] in id_to_check]
    # print("Checking solution")
    for p in to_check:
        
        negative_opinions = set(p['edges']).intersection(result)

        if len(negative_opinions) > 0:
            print(f"Wrong Answer: {p['id']} => {negative_opinions}")
            return False

    return True

def run_tests(n_tests, accept_blank=False):
    tests = generator(n_tests)
    mistakes = 0
    i = 1 
    while i <= n_tests:
        testcase = generator(1)[0]
        
        sol = solve(testcase[0], testcase[1], accept_blank=accept_blank)
        
        ans = check(testcase[0], sol[1])
        
        if not ans:
            mistakes += 1
        
        elif sol[0] == testcase[1]:
            print(f"{i} max k possible")
            
        if sol[0] != 0:
            i += 1
    # if mistakes > 0:
    print(f"{n_tests - mistakes}/{n_tests} correct") 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--accept_blank", action="store_true", help="Accept blank values")
    args = parser.parse_args()
    run_tests(50, accept_blank=args.accept_blank)
    