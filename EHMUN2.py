# **EHMUN**


def partion_items(D):
    """
    Partition items into three disjoint sets: rho (items with positive profit), delta (items with both positive and negative profit), and eta (items with negative profit).

    Parameters:
    D: A list of transactions where each transaction is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.

    Returns:
    rho, delta, eta: Three disjoint sets of items.
    rtwu_dict: A dictionary where the keys are items and the values are the total utility of each item in D.
    """
    rho, delta, eta = set(), set(), set()
    rtwu_dict = {}

    for transaction in D:
        items = transaction["Items"]
        profits = transaction["Profits"]
        quantities = transaction["Quantities"]
        rtwu_sum = sum(p * q for p, q in zip(profits, quantities) if p > 0)
        for item, profit in zip(items, profits):
            if profit > 0:
                rho.add(item)
            elif profit < 0:
                eta.add(item)

            if item in rtwu_dict:
                rtwu_dict[item] += rtwu_sum
            else:
                rtwu_dict[item] = rtwu_sum

    delta = rho.intersection(eta)
    rho.difference_update(delta)
    eta.difference_update(delta)
    return rho, delta, eta, rtwu_dict


def u(X, transaction=None, D=None):
    """
    Calculate the utility of a set of items X in
    a transaction or a database of transactions.

    Parameters:
    X: A set or list of items.
    transaction: A transaction of database
    D: databse

    Returns:
    The utility of X in the transaction or the database of transactions.
    """
    if X == "":
        return 0

    if transaction:
        return sum(
            transaction["Quantities"][i] * transaction["Profits"][i]
            for i, item in enumerate(transaction["Items"])
            if item in X
        )

    if D:
        return sum(
            u(X, transaction=transaction)
            for transaction in D
            if all(item in transaction["Items"] for item in X)
        )


def rlu(X, z, D=None, Tk=None):
    """
    Calculate the remaining lower utility of a set of items X with
    respect to a set of items z in a database of transactions D.

    Parameters:
    X: A set or list of items.
    z: A set or list of items.
    D: A list of transactions where each transaction
    is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.

    Returns:
    float: The remaining lower utility of X with respect to z in D.
    """
    if X == "":
        items = [z]
    else:
        items = X + [z]

    if Tk:
        if not X:
            return rtu(Tk)
        total = 0
        if all(item in Tk["Items"] for item in items):
            for x in X:
                total += u(x, Tk) + rru(x, Tk)
        return total

    return sum(
        u(x, transaction) + rru(x, transaction)
        for transaction in D
        if all(item in transaction["Items"] for item in items)
        for x in X
    )


def rru(X, transaction):
    """
    Calculate the remaining utility of a set of items X in a transaction.

    Parameters:
    X: A set or list of items.
    transaction: A transaction of database.

    Returns:
    fThe remaining utility of the items in the transaction
    that appear after the last item in X.
    """
    items = transaction["Items"]
    if X and X[-1] in items:
        RE = items[items.index(X[-1]) + 1 :]
    else:
        RE = items

    return sum(u(x, transaction) for x in RE if u(x, transaction) > 0)


def rtu(transaction):
    """
    Calculate the total utility of a transaction.

    Parameters:
    transaction: A transaction of database

    Returns:
    The total utility of the transaction.
    """
    items = transaction["Items"]
    return sum(u(item, transaction) for item in items if u(item, transaction) > 0)


def rtwu(X, D):
    """
    Calculate the total utility of a set of items X
    in a database of transactions D.

    Parameters:
    X: A set or list of items.
    D: Database

    Returns:
    The total utility of X in D.
    """
    items = [X]
    return sum(
        rtu(transaction)
        for transaction in D
        if all(item in transaction["Items"] for item in items)
    )


def rsu(X, z, D=None, Tk=None):
    """
    Calculate the remaining upper utility of a set of items X
    with respect to a set of items z in a database of transactions D.

    Parameters:
    X: A list of items.
    z: A list of items.
    D (list of dict): Database

    Returns:
    The remaining upper utility of X with respect to z in D.
    """
    if not X:
        items = z
    else:
        items = X + z
    
    if Tk:
        total = 0
        if all(item in Tk["Items"] for item in items):
            total += u(X, Tk) + u(z, Tk) + rru(z, Tk)
        return total
    return sum(
        u(X, transaction) + u(z, transaction) + rru(z, transaction)
        for transaction in D
        if all(item in transaction["Items"] for item in items)
    )


def create_RLU_UA(D, items, X=None):
    """
    Create a dictionary mapping each item to
    its remaining lower (RLU) in the database.

    Parameters:
    D: Database
    items: A list of items to calculate the RLU for.
    If None, it uses the secondary items derived from the database.
    X: A list of items.
    If provided, the RLU is calculated with respect to these items.

    Returns:
    dict: A dictionary where keys are items and values
    are their respective remaining lower utilities in the database.
    """
    return {item: (rtwu(item, D) if X is None else rlu(X, item, D)) for item in items}


def create_RSU_UA(D, items=None, X=None):
    """
    Create a dictionary mapping each item to its
    remaining upper utility (RSU) in the database.

    Parameters:
    D: A database
    items: A list of items to calculate the RSU for.
    If None, it uses the secondary items derived from the database.
    X: A set or list of items.
    If provided, the RSU is calculated with respect to these items.

    Returns:
    A dictionary where keys are items and values
    are their respective remaining upper utilities in the database.
    """
    X = [] if not X else X
    return {item: rsu(X, [item], D) for item in items}

def create_RSU_RLU_UA(D, Db, B, items):
    UA_dict = {}
    U_dict = {"".join(B + [z]): u(B + [z], D=Db) for z in items}
    for Tk in D:
        for item in items:
            
            if item not in Tk["Items"]:
                continue

            rsu_value = u([item], Tk) + rru(item, Tk)
            rlu_value = -u([item], Tk) + rru(B, Tk)

            if item in UA_dict:
                UA_dict[item]["RSU"] += rsu_value
                UA_dict[item]["RLU"] += rlu_value
            else:
                item_str = "".join(B + [item])
                UA_dict[item] = {"RSU": rsu_value + U_dict[item_str], "RLU": rlu_value + U_dict[item_str]}
    return UA_dict


def remove_items_outside_items_database(D, items):
    """
    Remove items that are not in the given list
    from all transactions in the database.

    Parameters:
    D: A database
    items: A list of items.

    Returns:
    The modified database with items
    not in the given list removed from all transactions.
    """
    items_set = set(items)
    for transaction in D:
        filtered = [
            (item, qty, prof)
            for item, qty, prof in zip(
            transaction["Items"], transaction["Quantities"], transaction["Profits"]
            )
            if item in items_set
        ]
        if filtered:
            transaction["Items"], transaction["Quantities"], transaction["Profits"] = (
                zip(*filtered)
            )
        else:
            transaction["Items"], transaction["Quantities"], transaction["Profits"] = (
                [],
                [],
                [],
            )
    return D


def sorted_transaction_items(D, items):
    """
    Sort the items, profits, and quantities within each transaction
    in the database D based on a specified order of items.

    Parameters:
    D: A database
    items: A list specifying the desired order of items.

    Returns:
    The modified database with items, profits, and quantities sorted
    within each transaction according to the specified order.
    """
    ordered_map = {item: i for i, item in enumerate(items)}
    for transaction in D:
        zip_trans = list(
            zip(transaction["Items"], transaction["Profits"], transaction["Quantities"])
        )
        sorted_item = sorted(
            zip_trans, key=lambda x: ordered_map.get(x[0], float("inf"))
        )
        transaction["Items"], transaction["Profits"], transaction["Quantities"] = zip(
            *sorted_item
        )
    return D


def sorted_transactions(D, items):
    """
    Sort the transactions in the database D based
    on the last item in each transaction.
    If two transactions have the same last item,
    they are sorted in descending order of the length of the transaction.

    Parameters:
    D: A database
    items: A list specifying the desired order of items.

    Returns:
    The sorted database.
    """
    ordered_map = {item: i for i, item in enumerate(items)}
    return sorted(
        D,
        key=lambda x: (ordered_map.get(x["Items"][-1], float("inf")), len(x["Items"])),
        reverse=True,
    )


def create_new_database(D, X):
    """
    Create a new database Dx from D by including
    only the items that come after X in each transaction of D.

    Parameters:
    D: The original database of transactions.
    X: The prefix set of items.

    Returns:
    The modified database with only the items
    that come after X in each transaction of D.
    """
    merging_dict = {}
    Dx = []
    i = 0
    for Tk in D:
        if X[-1] not in Tk["Items"]:
            continue

        index = Tk["Items"].index(X[-1]) + 1
        if index == len(Tk["Items"]):
            continue

        tid = Tk["TID"]
        items = Tk["Items"][index:]
        quantities = Tk["Quantities"][index:]
        profits = Tk["Profits"][index:]

        if items in merging_dict:
            old_index = merging_dict[items]["TID"]
            Dx[old_index]["Quantities"] = [
                x + y for x, y in zip(Dx[old_index]["Quantities"], quantities)
            ]
            Dx[old_index]["Profits"] = [
                x + y for x, y in zip(Dx[old_index]["Profits"], profits)
            ]
        else:
            merging_dict[items] = {"TID": len(Dx)}
            Dx.append({
                "TID": tid,
                "Items": items,
                "Quantities": quantities,
                "Profits": profits,
            })
        i += 1
    return Dx


def searchN(eta, X, Db, Dx, minU, res):
    """
    Perform a recursive search to identify itemsets with utility
    greater than or equal to a minimum threshold.
    This function explores combinations of negative items, calculating
    their utility in the given transactions, and recursively refining
    the search based on the remaining utility of negative items.

    Parameters:
    eta: A sorted list of items with negative profit.
    X: The current itemset being evaluated.
    Dx: The current database of transactions after filtering items.
    minU: The minimum utility threshold for an itemset to be considered.
    countK: The current count of high utility itemsets found.
    k: The desired number of high utility itemsets to find.

    """
    for i in eta:
        B = X + [i]
        uB = u(B, D=Db)
        if uB >= minU:
            res.append([B, uB])
        Dz = create_new_database(Dx, B)
        UA_RSU = {item: rsu(X, [item], Dx) for item in eta[eta.index(i) + 1 :]}
        
        primary_B = [z for z in eta if z in UA_RSU and UA_RSU[z] >= minU]
        searchN(primary_B, B, Db, Dz, minU, res)


def search(eta, X, Db, Dx, primary_items, secondary_items, minU, res):
    """
    Perform a recursive search to identify itemsets
    with utility greater than or equal to a minimum threshold.
    This function explores combinations of primary and secondary items,
    calculating their utility in the given transactions,and recursively
    refining the search based on the remaining utility of secondary items.

    Parameters:
    eta: A sorted list of items with negative profit.
    X: The current itemset being evaluated.
    Dx: The current database of transactions after filtering items.
    primary_items: A list of primary items to consider for expanding the current itemset.
    secondary_items: A list of secondary items for utility calculations.
    minU: The minimum utility threshold for an itemset to be considered.
    res: The list that contains result.

    Returns:
    The list of result have greater than min utility.
    """
    for i in primary_items:
        B = X + [i]

        uB = u(B, D=Db)
        Dz = create_new_database(Dx, B)
        if "8" in B:
            print(B, uB)
        if uB >= minU:
            # print("SUCCESS", B, "= ", uB)
            res.append([B, uB])

        if uB > minU:
            searchN(eta, B, Db, Dz, minU, res)

        if i not in secondary_items:
            continue

        UA_dict = create_RSU_RLU_UA(Dz, Db, B, secondary_items[secondary_items.index(i) + 1 :])

        primary_B = [
            z for z in secondary_items if z in UA_dict and UA_dict[z]["RSU"] >= minU
        ]
        secondary_B = [
            z for z in secondary_items if z in UA_dict and UA_dict[z]["RLU"] >= minU
        ]
        
        if "8" in B:
            print(UA_dict)
            print("PRIMARY", primary_B)
            print("SECONDARY", secondary_B)
        
        
        search(eta, B, Db, Dz, primary_B, secondary_B, minU, res)
    return res


def EMHUN(D, minU, k):
    X = []
    # Step 2, 3, 4
    rho, delta, eta, rtwu_dict = partion_items(D)

    # Step 5
    tmp = [item for item in rho | delta]
    UA = {item: rtwu_dict[item] for item in tmp if item in rtwu_dict}

    # Step 6, 7
    secondary_items = sorted(
        UA, key=lambda x: (0 if x in rho else 1 if x in delta else 2, UA[x], x)
    )

    eta_sorted = sorted(
        eta, key=lambda x: (0 if x in rho else 1 if x in delta else 2, rtwu(x, D))
    )

    # Step 8,9,10
    items   = secondary_items + eta_sorted
    D       = remove_items_outside_items_database(D, items)
    D       = sorted_transaction_items(D, items)
    Dx      = sorted_transactions(D, items)

    # Step 11
    UA_SU = {item: rsu(X, [item], Dx) for item in tmp}

    # Step 12
    primary_items = [i for i in secondary_items if UA_SU[i] >= minU]

    # Step 13
    res = search(eta_sorted, X, D, Dx, primary_items, secondary_items, minU, [])
    res = sorted(res, key=lambda x: x[1], reverse=True)

    return res[: min(len(res), k)]


D = []
i = 0
with open("accidents_negative.txt", "r") as f:
    for line in f:
        i += 1
        line = line.strip()
        data_split = line.split(":")
        items = data_split[0].split(" ")
        quantities = [1 for _ in range(len(items))]
        utilities = list(map(int, data_split[2].split(" ")))
        D.append(
            {
                "TID": str(i),
                "Items": items,
                "Quantities": quantities,
                "Profits": utilities,
            }
        )

# D = [
#     {
#         "TID": 1,
#         "Items": ["a", "b", "d", "e", "f", "g"],
#         "Quantities": [2, 2, 1, 3, 2, 1],
#         "Profits": [-2, 1, 4, 1, -1, -2],
#     },
#     {"TID": 2, "Items": ["b", "c"], "Quantities": [1, 5], "Profits": [-1, 1]},
#     {
#         "TID": 3,
#         "Items": ["b", "c", "d", "e", "f"],
#         "Quantities": [2, 1, 3, 2, 1],
#         "Profits": [-1, 1, 4, 1, -1],
#     },
#     {"TID": 4, "Items": ["c", "d", "e"], "Quantities": [2, 1, 3], "Profits": [1, 4, 1]},
#     {"TID": 5, "Items": ["a", "f"], "Quantities": [2, 3], "Profits": [2, -1]},
#     {
#         "TID": 6,
#         "Items": ["a", "b", "c", "d", "e", "f", "g"],
#         "Quantities": [2, 1, 4, 2, 1, 3, 1],
#         "Profits": [1, 1, 1, 4, 1, -1, -2],
#     },
#     {"TID": 7, "Items": ["b", "c", "e"], "Quantities": [3, 2, 2], "Profits": [1, 2, 2]},
# ]

res = EMHUN(D, 1e7, 10)
print()
for r in res:
    print(r)