# D = [
#     {
#         'TID': 'T1',
#         'Items': ['a', 'b', 'd', 'e', 'f', 'g'],
#         'Quantities': [2, 2, 1, 3, 2, 1],
#         'Profits': [-2, 1, 4, 1, -1, -2]
#     },
#     {
#         'TID': 'T2',
#         'Items': ['b', 'c'],
#         'Quantities': [1, 5],
#         'Profits': [-1, 1]
#     },
#     {
#         'TID': 'T3',
#         'Items': ['b', 'c', 'd', 'e', 'f'],
#         'Quantities': [2, 1, 3, 2, 1],
#         'Profits': [-1, 1, 4, 1, -1]
#     },
#     {
#         'TID': 'T4',
#         'Items': ['c', 'd', 'e'],
#         'Quantities': [2, 1, 3],
#         'Profits': [1, 4, 1]
#     },
#     {
#         'TID': 'T5',
#         'Items': ['a', 'f'],
#         'Quantities': [2, 3],
#         'Profits': [2, -1]
#     },
#     {
#         'TID': 'T6',
#         'Items': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
#         'Quantities': [2, 1, 4, 2, 1, 3, 1],
#         'Profits': [1, 1, 1, 4, 1, -1, -2]
#     },
#     {
#         'TID': 'T7',
#         'Items': ['b', 'c', 'e'],
#         'Quantities': [3, 2, 2],
#         'Profits': [1, 2, 2]
#     }
# ]

D = [
    {
        'TID': 'T1',
        'Items': ['a', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
        'Quantities': [2, 2, 1, 3, 2, 1, 2, 1, 4, 3, 2, 1, 3, 2, 2, 4, 1, 2, 3, 1, 4, 2, 3, 1, 2],
        'Profits': [-2, 1, 4, 1, -1, -2, 3, -1, 2, 0, 1, -3, 2, -1, 4, 0, 1, 2, -1, 3, 2, 1, -3, 2, 0]
    },
    {
        'TID': 'T2',
        'Items': ['b', 'c', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
        'Quantities': [1, 5, 2, 3, 1, 4, 2, 3, 1, 2, 3, 2, 4, 1, 3, 2, 1, 3, 2, 4, 1],
        'Profits': [-1, 1, 2, -3, 1, 2, 0, 4, 2, 1, 3, 2, -1, 2, -2, 3, 1, 0, 2, -3, 2]
    },
    {
        'TID': 'T3',
        'Items': ['b', 'c', 'd', 'e', 'f', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v'],
        'Quantities': [2, 1, 3, 2, 1, 2, 4, 1, 2, 3, 2, 3, 4, 2, 1, 3, 2, 2, 1, 3],
        'Profits': [-1, 1, 4, 1, -1, 2, -3, 0, 1, 2, 3, -2, 1, -1, 4, 2, 3, 1, 0, -3]
    },
    {
        'TID': 'T4',
        'Items': ['c', 'd', 'e', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x'],
        'Quantities': [2, 1, 3, 4, 2, 1, 2, 3, 2, 1, 3, 4, 2, 3, 1, 4, 2, 3, 1, 2],
        'Profits': [1, 4, 1, -2, 2, 3, -1, 2, 4, 1, 2, -3, 2, 1, 4, -2, 3, 1, -1, 2]
    },
    {
        'TID': 'T5',
        'Items': ['a', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x'],
        'Quantities': [2, 3, 1, 3, 2, 4, 1, 3, 2, 1, 2, 3, 4, 2, 3, 1, 2, 4, 1, 2],
        'Profits': [2, -1, -2, 1, -3, 4, 0, 2, 3, -1, 2, -2, 1, 3, 2, -3, 1, 2, 3, 1]
    },
    {
        'TID': 'T6',
        'Items': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's'],
        'Quantities': [2, 1, 4, 2, 1, 3, 1, 2, 1, 2, 3, 4, 2, 1, 3, 1, 4, 2, 1],
        'Profits': [1, 1, 1, 4, 1, -1, -2, 2, -3, 0, 1, 2, 4, -2, 3, 2, 1, -1, 2]
    },
    {
        'TID': 'T7',
        'Items': ['b', 'c', 'e', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v'],
        'Quantities': [3, 2, 2, 1, 3, 2, 4, 3, 2, 1, 2, 4, 3, 1, 2, 3, 1, 2, 3],
        'Profits': [1, 2, 2, 0, -1, 3, 2, -1, 2, 4, 1, 3, 2, 2, 1, 3, 0, 1, -2]
    },
    {
        'TID': 'T8',
        'Items': ['a', 'b', 'c', 'd', 'e', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'],
        'Quantities': [2, 3, 1, 2, 4, 1, 2, 3, 4, 2, 3, 1, 4, 3, 1, 3, 2],
        'Profits': [1, -1, 2, 0, 1, 3, -2, 2, 1, 4, 2, 3, -1, 2, 1, 0, -2]
    },
    {
        'TID': 'T9',
        'Items': ['d', 'e', 'f', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u'],
        'Quantities': [4, 1, 3, 2, 4, 1, 3, 2, 4, 1, 2, 3, 1, 4, 2, 3, 1],
        'Profits': [2, 3, -1, 2, -3, 1, 4, 2, 1, 2, 3, 1, 2, -1, 3, 2, 0]
    },
    {
        'TID': 'T10',
        'Items': ['a', 'c', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r'],
        'Quantities': [1, 2, 3, 4, 2, 3, 2, 3, 2, 1, 3, 4, 1, 2, 3, 2],
        'Profits': [2, 1, 4, -2, 3, 1, -3, 2, 1, -1, 2, 3, -2, 4, 2, 1]
    }
]

def get_unique_items(transactions):
    unique_items = set(item for transaction in transactions for item in transaction['Items'])
    return sorted(unique_items)

def generate_all_combinations(items):
    def helper(start, current_combination):
        if current_combination:
            result.append(current_combination[:])
        for i in range(start, len(items)):
            current_combination.append(items[i])
            helper(i + 1, current_combination)
            current_combination.pop()  

    result = []
    helper(0, [])
    return result

def calculate_utility(X, transactions):
    total_utility = 0 
    for transaction in transactions:
        if all(item in transaction['Items'] for item in X):
            utility = 0
            for item in X:
                idx = transaction['Items'].index(item)
                utility += transaction['Quantities'][idx] * transaction['Profits'][idx]
            total_utility += utility  
    return total_utility

def brute_force_topk(database, K, minU):
    unique_items = get_unique_items(database)
    combinations = generate_all_combinations(unique_items)
    
    itemset_utilities = []
    for combination in combinations:
        utility = calculate_utility(combination, database)
        if utility >= minU:  # Only consider itemsets with utility >= minU
            itemset_utilities.append((combination, utility)) 
    
    # Sort itemset_utilities in descending order
    itemset_utilities.sort(key=lambda x: x[1], reverse=True)
    
    return itemset_utilities[:K]

import time

# Assuming the previous code with the brute_force_topk function and data D is already defined

# Set the minimum utility threshold
minU = 200
K = 2

# Record the start time
start_time = time.time()

# Call the brute_force_topk function
top_k_combinations = brute_force_topk(D, K, minU)

# Record the end time
end_time = time.time()

# Calculate the running time
running_time = end_time - start_time

# Print the top K combinations
for i, (combination, utility) in enumerate(top_k_combinations):
    print(f"Top {i+1} utilities: {combination} - Utility: {utility}")

# Print the running time
print(f"Running time: {running_time:.6f} seconds")