def EMHUN(D, minU, k):
    """
    Discover high-utility itemsets (HUIs) in a database of transactions with quantitative items.

    Parameters:
    D (list of dict): A list of transactions where each transaction is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.
    minU (int): The minimum utility threshold for an itemset to be considered as a HUI.
    k (int): The number of HUIs to return.

    Returns:
    None: The function prints the k HUIs with the highest utility.
    """

    def partion_items(D):
        """
        Partition items into three disjoint sets: rho (items with positive profit), delta (items with both positive and negative profit), and eta (items with negative profit).

        Parameters:
        D (list of dict): A list of transactions where each transaction is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.

        Returns:
        rho, delta, eta (set): Three disjoint sets of items.
        """
        rho, delta, eta = set(), set(), set()
        UL = {}
        for transaction in D:
            items = transaction['Items']
            profits = transaction['Profits']
            for item, profit in zip(items, profits):
                if item in UL:
                    UL[item] += rtwu(transaction)
                else:
                    UL[item] = profit
                if profit > 0:
                    rho.add(item)
                elif profit < 0:
                    eta.add(item)

        delta = rho.intersection(eta)
        rho.difference_update(delta)
        eta.difference_update(delta)
        return rho, delta, eta

    def u(X, transaction=None, D=None):
        
        if X == "":
            return 0
        
        if transaction and not D:
            return sum(
                transaction['Quantities'][i] * transaction['Profits'][i] 
                for i, item in enumerate(transaction['Items']) if item in X
            )

        if D and not transaction:
            return sum(
                u(X, transaction=transaction) 
                for transaction in D if all(item in transaction['Items'] for item in X)
            )
            
        return 0
        
                
    def rru(X, transaction):
        """
        Calculate the remaining utility of a set of items X in a transaction.

        Parameters:
        X (set or list): A set or list of items.
        transaction (dict): A dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.

        Returns:
        float: The remaining utility of the items in the transaction that appear after the last item in X.
        """
        X = list(X)
        items = transaction["Items"]
        RE = items[items.index(X[-1]) + 1:]
        print("X", X)
        print("REEE", RE)
        return sum(
            u(x, transaction) 
            for x in RE if u(x, transaction) > 0
        )

    def rlu(X, z, D):
        """
        Calculate the remaining lower utility of a set of items X with respect to a set of items z in a database of transactions D.

        Parameters:
        X (set or list): A set or list of items.
        z (set or list): A set or list of items.
        D (list of dict): A list of transactions where each transaction is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.

        Returns:
        float: The remaining lower utility of X with respect to z in D.
        """
        items = list(X) + list(z)
        print("X", X)
        return sum(
            u(X, transaction) + rru(X, transaction)
            for transaction in D if all(item in transaction["Items"] for item in items)
        )

    def rtu(transaction):
        """
        Calculate the total utility of a transaction.

        Parameters:
        transaction (dict): A dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.
        
        Returns:
        float: The total utility of the transaction.
        """
        items = transaction['Items']
        return sum(
            u(item, transaction) 
            for item in items if u(item, transaction) > 0
        )

    def rtwu(X, D=None):
        """
        Calculate the total utility of a set of items X in a database of transactions D.

        Parameters:
        X (set or list): A set or list of items.
        D (list of dict): A list of transactions where each transaction is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.

        Returns:
        float: The total utility of X in D.
        """
        items = X[0]
        return sum(
            rtu(transaction)
            for transaction in D if all(item in transaction["Items"] for item in items)
        )

    def rsu(X, z, D):
        
        """
        Calculate the remaining upper utility of a set of items X with respect to a set of items z in a database of transactions D.

        Parameters:
        X (set or list): A set or list of items.
        z (set or list): A set or list of items.
        D (list of dict): A list of transactions where each transaction is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.
        
        Returns:
        float: The remaining upper utility of X with respect to z in D.
        """
        items = list(X) + list(z)
        return sum(
            u(X, transaction) + u(z, transaction) + rru(z, transaction)
            for transaction in D if all(item in transaction["Items"] for item in items)
        )

    def create_RLU_UA(D, items=None, X=None):    
        """
        Create a dictionary mapping each item to its remaining lower utility (RLU) in the database.

        Parameters:
        D (list of dict): A list of transactions where each transaction is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.
        items (list, optional): A list of items to calculate the RLU for. If None, it uses the secondary items derived from the database.
        X (set or list, optional): A set or list of items. If provided, the RLU is calculated with respect to these items.

        Returns:
        dict: A dictionary where keys are items and values are their respective remaining lower utilities in the database.
        """
        items = secondary(D) if items is None else items
        return {item: (rtwu(item, D) if X is None else rlu(X, item, D)) for item in items}

    def create_RSU_UA(D, items=None, X=None):
        """
        Create a dictionary mapping each item to its remaining upper utility (RSU) in the database.

        Parameters:
        D (list of dict): A list of transactions where each transaction is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.
        items (list, optional): A list of items to calculate the RSU for. If None, it uses the secondary items derived from the database.
        X (set or list, optional): A set or list of items. If provided, the RSU is calculated with respect to these items.

        Returns:
        dict: A dictionary where keys are items and values are their respective remaining upper utilities in the database.
        """
        items = secondary(D) if items is None else items
        return {item: rsu("", item, D) if X is None else rsu(X, item, D) for item in items}

    def secondary(D):
        """
        Return a list of secondary items in the database D.

        An item is secondary if it is in the union of rho and delta and its total utility in D is at least minU.

        Parameters:
        D (list of dict): A list of transactions where each transaction is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.
        minU (int): The minimum utility threshold.

        Returns:
        list: A list of secondary items in the database D.
        """
        rho, delta, _ = partion_items(D)
        return [item for item in rho|delta if rtwu(item, D) >= minU]

    def remove_outside_items_database(D, items):
        """
        Remove items that are not in the given list from all transactions in the database.

        Parameters:
        D (list of dict): A list of transactions where each transaction is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.
        items (list): A list of items.

        Returns:
        list of dict: The modified database with items not in the given list removed from all transactions.
        """
        allowed_items = set(items)
        for transaction in D:
            filtered_data = [
                (item, qty, profit)
                for item, qty, profit 
                in zip(transaction["Items"], transaction["Quantities"], transaction["Profits"])
                if item in allowed_items
            ]
            if filtered_data:
                transaction["Items"], transaction["Quantities"], transaction["Profits"] = zip(*filtered_data)
            else:
                transaction["Items"], transaction["Quantities"], transaction["Profits"] = [], [], []
        return D
    def sorted_transaction_items(D, items):
        """
        Sort the items, profits, and quantities within each transaction in the database D based on a specified order of items.

        Parameters:
        D (list of dict): A list of transactions where each transaction is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.
        items (list): A list specifying the desired order of items.

        Returns:
        list of dict: The modified database with items, profits, and quantities sorted within each transaction according to the specified order.
        """
        ordered_map = {item: i for i, item in enumerate(items)} 
        for transaction in D:
            zipped_data = list(zip(transaction["Items"], transaction["Profits"], transaction["Quantities"]))
            sorted_data = sorted(zipped_data, key=lambda x: ordered_map.get(x[0], float("inf")))
            if sorted_data:
                transaction["Items"], transaction["Profits"], transaction["Quantities"] = zip(*sorted_data)
            else:
                transaction["Items"], transaction["Profits"], transaction["Quantities"] = [], [], [] 
        return D

    def sorted_transactions(D, items):
        """
        Sort the transactions in the database D based on the last item in each transaction. If two transactions have the same last item, they are sorted in descending order of the length of the transaction.
        
        Parameters:
        D (list of dict): A list of transactions where each transaction is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.
        items (list): A list specifying the desired order of items.
        
        Returns:
        list of dict: The sorted database.
        """
        
        ordered_map = {item: i for i, item in enumerate(items)}
        return sorted(D, key = lambda x: (ordered_map.get(x['Items'][-1], float('inf')), len(x['Items'])), reverse=True)

    def create_new_database(D, X):
        """
        Create a new database Dx from D by including only the items that come after X in each transaction of D.

        Parameters:
        D (list of dict): The original database of transactions.
        X (list): The prefix set of items.

        Returns:
        list of dict: The modified database with only the items that come after X in each transaction of D.
        """
        Dx = []
        for transaction in D:
            if X in transaction['Items']:
                print(X, transaction)
                index_x = transaction['Items'].index(X[-1]) + 1
                if index_x < len(transaction['Items']):
                    Dx.append({
                        'TID': transaction['TID'],
                        'Items': transaction['Items'][index_x:],
                        'Quantities': transaction['Quantities'][index_x:],
                        'Profits': transaction['Profits'][index_x:]
                    })
        return Dx
                
    def search(eta, X, Dx, primary_items, secondary_items, minU, countK, k):      
        """
        Perform a recursive search to identify itemsets with utility greater than or equal to a minimum threshold.

        This function explores combinations of primary and secondary items, calculating their utility in the given transactions,
        and recursively refining the search based on the remaining utility of secondary items.

        Parameters:
        eta (list): A sorted list of items with negative profit.
        X (set or list): The current itemset being evaluated.
        Dx (list of dict): The current database of transactions after filtering items.
        primary_items (list): A list of primary items to consider for expanding the current itemset.
        secondary_items (list): A list of secondary items for utility calculations.
        minU (float): The minimum utility threshold for an itemset to be considered.
        countK (int): The current count of high utility itemsets found.
        k (int): The desired number of high utility itemsets to find.

        Returns:
        None: The function prints itemsets that meet or exceed the minimum utility threshold.
        """  
        
        for i in primary_items:
            B = X + [i]
            uB = u(B, D=Dx)  
            
            if (uB >= minU):
                print(B, "= ", uB)
                countK += 1
                
            if countK == k:
                break 
            
            if (uB > minU):
                searchN(eta, B, Dx, minU, countK, k)
                
            UA_RLU = create_RLU_UA(Dx, secondary_items[secondary_items.index(i) + 1:], B)
            UA_RSU = create_RSU_UA(Dx, secondary_items[secondary_items.index(i) + 1:], B)
            print("RLU", UA_RLU)
            print("RSU", UA_RSU)
            primary_B = [z for z in secondary_items if z in UA_RSU and UA_RSU[z] >= minU]
            secondary_B = [z for z in secondary_items if z in UA_RLU and UA_RLU[z] >= minU]
            
            search(eta, B, Dx, primary_B, secondary_B, minU, countK, k)
            
    def searchN(eta, X, Dx, minU, countK, k):
        """
        Perform a recursive search to identify itemsets with utility greater than or equal to a minimum threshold.

        This function explores combinations of negative items, calculating their utility in the given transactions,
        and recursively refining the search based on the remaining utility of negative items.

        Parameters:
        eta (list): A sorted list of items with negative profit.
        X (set or list): The current itemset being evaluated.
        Dx (list of dict): The current database of transactions after filtering items.
        minU (float): The minimum utility threshold for an itemset to be considered.
        countK (int): The current count of high utility itemsets found.
        k (int): The desired number of high utility itemsets to find.

        Returns:
        None: The function prints itemsets that meet or exceed the minimum utility threshold.
        """ 
        for i in eta:      
            B = X + [i]
            uB = u(B, D=Dx)
            Db = create_new_database(Dx, B)

            if (uB >= minU):
                print(B, "= ", uB)
                countK += 1
                
            if countK == k:
                break 
            
            UA_RSU = create_RSU_UA(Db, eta[eta.index(i) + 1:], B)
            primary_B = [z for z in eta if z in UA_RSU and UA_RSU[z] >= minU]
            
            searchN(primary_B, B, Dx, minU, countK, k)

    X = []
    #Step 2, 3, 4
    rho, delta, eta = partion_items(D)
    
    #Step 5
    UA = create_RLU_UA(D)
    #Step 6, 7
    secondary_items = sorted(UA, key=lambda x: (0 if x in rho else 1 if x in delta else 2, UA[x], x))
    eta_sorted = sorted(eta, key=lambda x: (0 if x in rho else 1 if x in delta else 2, rtwu(x, D)))
    
    #Step 8,9,10
    items = secondary_items + eta_sorted
    D = remove_outside_items_database(D, items)
    D = sorted_transaction_items(D, items)
    D = sorted_transactions(D, items)
    
    #Step 11
    UA_SU = create_RSU_UA(D)
    print(UA_SU)
    #Step 12
    primary_items = [i for i in secondary_items if UA_SU[i] >= minU]
    print(primary_items)
    #Step 13
    print(search(eta_sorted, X, D, primary_items, secondary_items, minU, 0, k))
    
    
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

res = EMHUN(D, 100, 10)
for r in res:
    print(r)