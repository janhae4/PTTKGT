D = [
    {
        'TID': 'T1',
        'Items': ['a', 'b', 'd', 'e', 'f', 'g'],
        'Quantities': [2, 2, 1, 3, 2, 1],
        'Profits': [-2, 1, 4, 1, -1, -2]
    },
    {
        'TID': 'T2',
        'Items': ['b', 'c'],
        'Quantities': [1, 5],
        'Profits': [-1, 1]
    },
    {
        'TID': 'T3',
        'Items': ['b', 'c', 'd', 'e', 'f'],
        'Quantities': [2, 1, 3, 2, 1],
        'Profits': [-1, 1, 4, 1, -1]
    },
    {
        'TID': 'T4',
        'Items': ['c', 'd', 'e'],
        'Quantities': [2, 1, 3],
        'Profits': [1, 4, 1]
    },
    {
        'TID': 'T5',
        'Items': ['a', 'f'],
        'Quantities': [2, 3],
        'Profits': [2, -1]
    },
    {
        'TID': 'T6',
        'Items': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        'Quantities': [2, 1, 4, 2, 1, 3, 1],
        'Profits': [1, 1, 1, 4, 1, -1, -2]
    },
    {
        'TID': 'T7',
        'Items': ['b', 'c', 'e'],
        'Quantities': [3, 2, 2],
        'Profits': [1, 2, 2]
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


unique_items = get_unique_items(D)
combinations = generate_all_combinations(unique_items)

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



def brute_force_topk(database, K):
    unique_items = get_unique_items(database)
    
    combinations = generate_all_combinations(unique_items)
    
    itemset_utilities = []
    for combination in combinations:
        utility = calculate_utility(combination, database)
        itemset_utilities.append((combination, utility)) 
    
    # Sort itemset_utilities in descending order
    itemset_utilities.sort(key=lambda x: x[1], reverse=True)
    
    return itemset_utilities[:K]
   

K = 3 
top_k_combinations = brute_force_topk(D, K)

for i, (combination, utility) in enumerate(top_k_combinations):
    print(f"Top {i+1} utilities: {combination} - Utility: {utility}")