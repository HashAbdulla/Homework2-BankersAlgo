
## Banker's Algorithm Implementation
## Author: Hashim Abdulla
## Course: Intro Operating Systems
## Assignment: Homework 2 - Banker's Algorithm

## This py program implements Banker's Algorithm for deadlock avoidance,
## including the Safety Test and Resource Request handling



def print_matrix(name, matrix):
    """print matrices in a readable format."""
    print(f"\n{name}:")
    for i, row in enumerate(matrix):
        print(f"  P{i+1}: {row}")

def print_vector(name, vector):
    """Helper function to print vectors in a readable format."""
    print(f"{name}: {vector}")

def calculate_need(max_matrix, allocation_matrix):
    """
    Calculate the Need matrix.
    which is Max[i][j] - Allocation[i][j]
    """
    n = len(max_matrix)
    m = len(max_matrix[0])
    need = []
    for i in range(n):
        need_row = []
        for j in range(m):
            need_row.append(max_matrix[i][j] - allocation_matrix[i][j])
        need.append(need_row)
    return need

def is_less_or_equal(list1, list2):
    """Check if list1 <= list2 element-wise."""
    return all(a <= b for a, b in zip(list1, list2))

def add_vectors(vec1, vec2):
    """Add two vectors element-wise."""
    return [a + b for a, b in zip(vec1, vec2)]

def safety_test(allocation, max_matrix, available):
    """
    Perform the Safety Test
    
    Returns:
        tuple: (is_safe: bool, safe_sequence: list, trace: list)
    """
    n = len(allocation)
    m = len(allocation[0])
    
    # Calculating Need matrix
    need = calculate_need(max_matrix, allocation)
    
    print("\n" + "="*60)
    print("SAFETY TEST")
    print("="*60)
    
    print_matrix("Allocation", allocation)
    print_matrix("Max", max_matrix)
    print_matrix("Need", need)
    print_vector("\nAvailable", available)
    
    # Initialize Work and Finish
    work = available.copy()
    finish = [False] * n
    safe_sequence = []
    trace = []
    
    print("\n" + "-"*60)
    print("SAFETY ALGORITHM EXECUTION")
    print("-"*60)
    
    step = 0
    # Try to find a safe sequence
    while len(safe_sequence) < n:
        found = False
        
        # Find a process that can be satisfied
        # Tie-breaking: choose lowest index (P1 < P2 < P3 < P4 < P5)
        for i in range(n):
            if not finish[i] and is_less_or_equal(need[i], work):
                # Process i can be satisfied
                step += 1
                print(f"\nStep {step}:")
                print(f"  Process P{i+1} can be satisfied")
                print(f"  Need[P{i+1}] = {need[i]} <= Work = {work}")
                
                # Allocate resources (simulate process completion)
                work = add_vectors(work, allocation[i])
                finish[i] = True
                safe_sequence.append(i + 1)  # Store as P1, P2, etc.
                
                print(f"  After P{i+1} completes:")
                print(f"    Work = Work + Allocation[P{i+1}] = {work}")
                print(f"    Finish[P{i+1}] = True")
                
                trace.append({
                    'step': step,
                    'process': i + 1,
                    'need': need[i].copy(),
                    'work_before': add_vectors(work, [-a for a in allocation[i]]),
                    'allocation': allocation[i].copy(),
                    'work_after': work.copy(),
                    'finish': finish.copy()
                })
                
                found = True
                break
        
        if not found:
            # No process can proceed - system is unsafe
            print("\n  NO process can proceed with current Work vector")
            print(f"  Work = {work}")
            print("  Remaining processes and their needs:")
            for i in range(n):
                if not finish[i]:
                    print(f"    P{i+1}: Need = {need[i]}")
            return False, [], trace
    
    print("\n" + "-"*60)
    print(" OK All processes can finish - System is SAFE")
    print("-"*60)
    
    return True, safe_sequence, trace

def request_resources(process_id, request, allocation, max_matrix, available):
    """
    Handle a resource request from a process.
    
    args:
        process_id: Process index (0-based)
        request: List of requested resources
        allocation: Current allocation matrix
        max_matrix: Maximum need matrix
        available: Available resources vector
    
    returns:
        tuple: (granted: bool, message: str)
    """
    n = len(allocation)
    m = len(allocation[0])
    
    print("\n" + "="*60)
    print(f"RESOURCE REQUEST from P{process_id + 1}")
    print("="*60)
    print(f"Request: {request}")
    
    # Calculate need for this process
    need = calculate_need(max_matrix, allocation)
    process_need = need[process_id]
    
    # Check 1: Request <= Need
    if not is_less_or_equal(request, process_need):
        msg = f"ERROR: Request {request} exceeds Need {process_need}"
        print(f"{msg}")
        return False, msg
    
    print(f"OK Check 1 passed: Request {request} <= Need {process_need}")
    
    # Check 2: Request <= Available
    if not is_less_or_equal(request, available):
        msg = f"DENIED: Request {request} exceeds Available {available}"
        print(f"{msg}")
        return False, msg
    
    print(f"OK Check 2 passed: Request {request} <= Available {available}")
    
    # Pretend to allocate - create new state
    new_allocation = [row.copy() for row in allocation]
    new_available = available.copy()
    
    for j in range(m):
        new_allocation[process_id][j] += request[j]
        new_available[j] -= request[j]
    
    print("\nPretending to allocate resources...")
    print(f"New Allocation[P{process_id + 1}] would be: {new_allocation[process_id]}")
    print(f"New Available would be: {new_available}")
    
    # Check 3: Safety test with new state
    print("\nPerforming Safety Test on new state...")
    is_safe, safe_seq, trace = safety_test(new_allocation, max_matrix, new_available)
    
    if is_safe:
        msg = f"GRANTED: Request leads to safe state with sequence <P{',P'.join(map(str, safe_seq))}>"
        print(f"\n {msg}")
        return True, msg
    else:
        msg = "DENIED: Request would lead to unsafe state"
        print(f"\n{msg}")
        return False, msg

def main():
    """the main function to run Banker's Algorithm tests."""
    
    n = 5  # number of processes
    m = 3  # number of resource types
    total_resources = [10, 5, 7]  # Total instances of A, B, C
    
    # Initial snapshot at S0
    allocation = [
        [0, 1, 0],  # P1
        [2, 0, 0],  # P2
        [3, 0, 2],  # P3
        [2, 1, 1],  # P4
        [0, 0, 2]   # P5
    ]
    
    max_matrix = [
        [7, 5, 3],  # P1
        [3, 2, 2],  # P2
        [9, 0, 2],  # P3
        [2, 2, 2],  # P4
        [4, 3, 3]   # P5
    ]
    
    available = [3, 3, 2]  # Available at S0
    
    print("="*60)
    print("BANKER'S ALGORITHM - HOMEWORK 2, by Hashim Abdulla")
    print("="*60)
    print(f"\nSystem Configuration:")
    print(f"  Processes: {n} (P1 to P5)")
    print(f"  Resource Types: {m} (A, B, C)")
    print(f"  Total Resources: A={total_resources[0]}, B={total_resources[1]}, C={total_resources[2]}")
    
    # TEST 1: Baseline Safety Test at S0
    print("\n\n" + "#"*60)
    print("# TEST 1: BASELINE SAFETY TEST AT S0")
    print("#"*60)
    
    is_safe, safe_seq, trace = safety_test(allocation, max_matrix, available)
    
    if is_safe:
        print(f"\n{'='*60}")
        print(f"RESULT: System is SAFE")
        print(f"Safe Sequence: <P{',P'.join(map(str, safe_seq))}>")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print(f"RESULT: System is UNSAFE")
        print(f"{'='*60}")
    
    # TEST 2: Resource Request that should be DENIED
    print("\n\n" + "#"*60)
    print("# TEST 2: RESOURCE REQUEST - DENIED SCENARIO")
    print("#"*60)
    print("\nScenario: P1 requests (0, 4, 0)")
    print("Expected: DENIED (exceeds Need or leads to unsafe state)")
    
    # P1 is process index 0
    request_p1 = [0, 4, 0]
    granted, message = request_resources(0, request_p1, allocation, max_matrix, available)
    
    print(f"\n{'='*60}")
    print(f"RESULT: {'GRANTED' if granted else 'DENIED'}")
    print(f"Reason: {message}")
    print(f"{'='*60}")
    
    # TEST 3: Resource Request that should be GRANTED (optional additional test)
    print("\n\n" + "#"*60)
    print("# TEST 3: RESOURCE REQUEST - GRANTED SCENARIO")
    print("#"*60)
    print("\nScenario: P2 requests (1, 0, 2)")
    print("Expected: GRANTED (leads to safe state)")
    
    # P2 is process index 1
    request_p2 = [1, 0, 2]
    granted, message = request_resources(1, request_p2, allocation, max_matrix, available)
    
    print(f"\n{'='*60}")
    print(f"RESULT: {'GRANTED' if granted else 'DENIED'}")
    print(f"Reason: {message}")
    print(f"{'='*60}")
    
    print("\n\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)

if __name__ == "__main__":
    main()
