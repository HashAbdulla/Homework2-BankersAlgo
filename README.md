# Homework-2- Banker's Algorithm
A Python program that implements the Banker's Algorithm for deadlock avoidance, including computation of the Need matrix and execution of the Safety Test to determine if the system is in a safe state.


CONTENTS
========
1. bankers_algo.py - Main implementation file
2. README.md - This file
3. bankersalgo-report.pdf - Detailed report with outputs and analysis

REQUIREMENTS
============
- Python 3.7 or higher
- No external libraries required (uses only Python standard library)

COMPILATION
===========
No compilation needed (Python is interpreted).

EXECUTION
=========

To run the program:

    python bankers_algo.py

Or on some systems:

    python3 bankers_algo.py

EXPECTED OUTPUT
===============

The program will execute three tests:

TEST 1: Baseline Safety Test at S0
- Input: Initial state with Allocation, Max, and Available
- Expected: SAFE
- Safe Sequence: <P2,P4,P1,P3,P5>

TEST 2: Denied Request Scenario
- Scenario: P1 requests [0, 4, 0]
- Expected: DENIED (exceeds available resources)
- Reason: Request for 4 units of B exceeds 3 available

TEST 3: Granted Request Scenario
- Scenario: P2 requests [1, 0, 2]
- Expected: GRANTED
- Safe Sequence: <P2,P4,P1,P3,P5>

PROGRAM STRUCTURE
=================

Main Functions:
- calculate_need(): Computes Need matrix (Max - Allocation)
- safety_test(): Implements the Safety Algorithm
- request_resources(): Handles resource requests with safety checking
- main(): Orchestrates all tests

Helper Functions:
- is_less_or_equal(): Vector comparison
- add_vectors(): Vector addition
- print_matrix(): Formatted matrix output
- print_vector(): Formatted vector output

IMPLEMENTATION NOTES
====================

1. Tie-Breaking: When multiple processes can proceed, the algorithm
   selects the process with the lowest index (P1 < P2 < P3 < P4 < P5).

2. Pretend-Allocate: The request handler creates copies of state
   before testing, ensuring the original state is never modified
   unless the request is granted.

3. Output Format: The program provides detailed step-by-step traces
   showing Work and Finish vectors at each selection step.

TESTING
=======

The program includes three comprehensive tests:
- Baseline safety test (should be SAFE)
- Request exceeding available (should be DENIED)
- Valid request leading to safe state (should be GRANTED)

All tests use the exact dataset specified in the assignment.

AI TOOL DISCLOSURE
==================

Tool: Claude (Claude Sonnet 4.5)

See bankersalgo-report.pdf Section 0 for detailed AI usage disclosure.
