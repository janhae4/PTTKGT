# **EHMIN**

def EU(iX, Tk=None, Db=None):
  """
  Calculate the utility of a set of items in a transaction or a database

  Parameters:
  iX: A list of items.
  Tk: A transaction
  Db: A database

  Returns:
  The utility of iX in the transaction or the database of transactions.
  """
  if Tk:
      if (iX not in Tk['Items']):
          return 0
      index = Tk['Items'].index(iX)
      return Tk['Profits'][index]
  else:
      for transaction in Db:
          if iX in transaction['Items']:
              index = transaction['Items'].index(iX)
              return transaction['Profits'][index]
      return 0

def IU(iX, Tk):
  """
  Calculate the internal utility of a list of items in a transaction.

  Parameters:
  iX: A list of items.
  Tk: transaction

  Returns:
  The internal utility of item in the transaction
  """
  return Tk["Quantities"][Tk['Items'].index(iX)] if iX in Tk['Items'] else 0

def U(X, Tk=None, Db=None):
  """
  Calculate the utility of a set of items in a transaction Tk or a database

  Parameters:
  X: A list of items.
  Tk: A transaction
  Db: A
  Returns:
  The utility of item in the transaction or database
  """
  if not isinstance(X, list):
      X = [X]

  if Tk:
      return sum (
          IU(ix, Tk) * EU(ix, Tk)
          for ix in X
      )

  else:
      return sum (
          U(X, Tk)
          for Tk in Db
          if all(ix in Tk['Items'] for ix in X)
      )

def PU(X, Tk=None, Db=None):
  """
  Calculate the positive utility of a set of items in a transaction or database

  Parameters:
  X: A list of items.
  Tk: A transaction.
  Db: A database.

  Returns:
  The positive utility of X in the transaction or the database of transactions.
  """
  if Tk:
      return sum (
          IU(ix, Tk) * EU(ix, Tk)
          for ix in X
          if EU(ix, Tk) > 0
      )
  else:
      return sum (
          PU(X, Tk)
          for Tk in Db
          if all(ix in Tk['Items'] for ix in X)
      )

def PTU(Tk):
  """
  Calculate the positive utility of a transaction Tk.

  Parameters:
  Tk: A transaction

  Returns:
  float: The positive utility of Tk.
  """
  return sum (
      U(ix, Tk)
      for ix in Tk['Items']
      if EU(ix, Tk) > 0
  )

def PTWU(X, cache):
  """
  Calculate the positive total utility of a set of items in a database.

  Parameters:
  X: A list of items.
  cache: A dictionary containing the positive total utility of each transaction in Db.

  Returns:
  The positive total utility of X in Db.
  """
  return sum (
      Tk['PTWU']
      for Tk in cache.values()
      if all(ix in Tk['Items'] for ix in X)
        )

def sorted_transactions(D, items):
  """
  Sort the items, profits, and quantities within each transaction
  in the database based on a specified order of items.

  Parameters:
  items: A list specifying the desired order of items.
  D: Database

  Returns:
  The modified database with items, profits, and quantities sorted
  within each transaction according to the specified order.
  """
  map = {item: index for index, item in enumerate(items)}
  for Tk in D:
      zip_list = list(zip(Tk['Items'], Tk['Quantities'], Tk['Profits']))
      sorted_item = sorted(zip_list, key = lambda x: map.get(x[0], len(items)))
      Tk['Items'], Tk['Quantities'], Tk['Profits'] = zip(*sorted_item)
  return D

def RTWU(Tk):
  """
  Calculate the remaining total utility of a transaction.

  Parameters:
  Tk: A dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.

  Returns:
  The remaining total utility of the transaction,
  considering only items with positive profits.
  """
  return sum (
      Tk['Profits'][index] * Tk['Quantities'][index]
      for index, ix in enumerate(Tk['Items'])
      if Tk['Profits'][index] > 0
  )

def PRU(X, Tk=None, D=None):
  """
  Calculate the positive utility of a set of items in a transaction or database

  Parameters:
  X: A list of items.
  Tk: A dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.
  D : A list of transactions where each transaction is represented
  as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.

  Returns:
  The positive utility of X in the transaction or the database of transactions.
  """
  if not X:
      return 0

  if Tk and not D:
      transaction = Tk['Items']
      index = transaction.index(X[-1]) + 1
      RP = transaction[index :]
    #   print(X, Tk['Items'], index)
      total = 0
    #   for iRP in RP:
    #         print(iRP, U(iRP, Tk))
    #         if U(iRP, Tk) > 0:
    #             total += U(iRP, Tk)
    #   print(f"total = {total}")
      return sum (
          U(iRP, Tk)
          for iRP in RP
          if EU(iRP, Tk) > 0
      )
  else:
      print(X)
      print("HI")
      return sum (
          PRU(X, Tk)
          for Tk in D
          if all(item in Tk['Items'] for item in X)
      )

def first_scan(Db):
  """
  Perform the first scan of the database to classify items
  and calculate their support and remaining total utility (RTWU).

  Parameters:
  Db: A list of transactions where each transaction is represented
  as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.

  Global Variables:
  items_sorted: A list of items sorted by their classification
  (positive, hybrid, negative), RTWU, and support.

  Returns:
  list: The sorted list of items based on their classification, RTWU, and support.
  """
  global items_sorted
  items = {}

  positive = set()
  hybrid = set()
  negative = set()
  for Tk in Db:
      transaction = Tk['Items']
      for index, ix in enumerate(transaction):
          if Tk['Profits'][index] > 0:
              positive.add(ix)
          else:
              negative.add(ix)

          if ix in items:
              items[ix]["Supp"] += 1
              items[ix]["RTWU"] += RTWU(Tk)
          else:
              items[ix] = {
                  "RTWU": RTWU(Tk),
                  "Supp": 1
          }
  hybrid = positive & negative
  positive -= hybrid
  negative -= hybrid
  print(items)
  items_sorted = sorted(items, key = lambda x: (0 if x in positive else 1 if x in hybrid else 2, items[x]['RTWU'], -items[x]['Supp']))
  return items_sorted

def second_scan(Db, items):
  """
  Perform the second scan of the database to calculate the
  utility list (UL) and the remaining lower utility (RLU) matrix (EUCS).

  Parameters:
  Db (list of dict): A list of transactions where each transaction
  is represented as a dictionary containing 'TID', 'Items', 'Quantities', and 'Profits'.
  items (list): A list of items sorted by their classification
  (positive, hybrid, negative), RTWU, and support.

  Returns:
  A tuple containing the EUCS matrix and the UL list.
  """
  global EUCS

  Db = sorted_transactions(Db, items)

  UL_dict = {}
  EUCS_cache = {}
  for Tk in Db:
      tmp = {}

      for ix in Tk['Items']:
          tmp[ix] = U(ix, Tk)


      for idx, utility in tmp.items():
          pru = PRU([idx], Tk)
          if idx in UL_dict:
              existing_entry = UL_dict[idx]
              existing_entry["TI"].append({
                  "TID": Tk['TID'],
                  "Utility": utility,
                  "PRU": pru
              })
              existing_entry["Utility"] += utility
              existing_entry["PRU"] += pru
          else:
              UL_dict[idx] = ({
                  "Item": idx,
                  "Utility": utility,
                  "PRU": pru,
                  "TI": [
                      {
                          "TID": Tk['TID'],
                          "Utility": utility,
                          "PRU": pru
                      }
                  ]
              })

      EUCS_cache[Tk['TID']] = {
          "Items": Tk['Items'],
          "PTWU": RTWU(Tk)
      }
  print("UL calculated successfully...")
  n = len(items)
  EUCS = [[0 for _ in range(n)] for _ in range(n)]
  for i in range(n):
      print(i)
      for j in range(i + 1, n):
          item_set = {items[i], items[j]}
          EUCS[i][j] = PTWU(item_set, EUCS_cache)
  print("EUCS calculated successfully...")

  UL = list(UL_dict.values())
  UL = sorted(UL, key = lambda x: items.index(x['Item']))
  return EUCS, UL


def EHMIN_Combine(Uk={}, Ul={}, pfutils={}):
    """
    Combine two utility lists (Uk and Ul) into one, while considering the utilities of items
    and their prefix utilities in the transaction database. This function is part of the high-utility
    itemset mining algorithm (EHMIN), where it merges two itemsets based on shared transactions.

    Parameters:
    Uk (dict): The first utility list, which contains the following keys:
               - 'Item' (str): The item identifier.
               - 'Utility' (float): The utility of the item.
               - 'PRU' (float): The Prefix Remaining Utility (PRU) for the item.
               - 'TI' (list of dicts): A list of transactions that includes the following keys:
                 - 'TID' (int): The transaction ID.
                 - 'Utility' (float): The utility of the item in the transaction.
                 - 'PRU' (float): The Prefix Remaining Utility for the item in the transaction.

    Ul (dict): The second utility list, which contains the same structure as `Uk`, representing
               another itemset that will be combined with `Uk`.

    pfutils (dict): A dictionary containing the prefix utilities for each transaction. The key is
                    the transaction ID (`TID`), and the value is the prefix utility for that transaction.

    Returns:
    dict or None: A dictionary representing the combined utility list, which contains:
                  - 'Item' (str): The item identifier (same as `Ul['Item']`).
                  - 'Utility' (float): The total utility after merging the two itemsets.
                  - 'PRU' (float): The total PRU after merging the two itemsets.
                  - 'TI' (list of dicts): The list of transactions after merging the two itemsets.

                  If the combined utility is less than a minimum utility threshold (`min_util`),
                  the function returns `None`.
    """
    # Initialize the combined utility list dictionary.
    C = {
        "Item": Ul['Item'],  # Use the item from the second utility list (Ul).
        "Utility": 0,        # Initialize combined utility to 0.
        "PRU": 0,            # Initialize combined PRU to 0.
        "TI": []             # Initialize transaction list to empty.
    }

    # Calculate utility sum of Uk and PRU (Prefix Remaining Utility).
    x = Uk['Utility'] + Uk['PRU']
    y = Uk['Utility']

    # Get the transaction lists (TI) for both Uk and Ul.
    sk = Uk['TI']
    sl = Ul['TI']
    # if (Uk['Item'] == '20' and Ul['Item'] == '2'):
    #     print(Uk)
    #     print(Ul)
    i, j = 0, 0  # Initialize indices for traversing the transaction lists.
    pfutil = 0    # Initialize prefix utility.

    # Traverse both transaction lists and combine matching transactions.
    while i < len(sk) and j < len(sl):
        sk_tid, sk_util, sk_pru = sk[i].values()  # Get values for the i-th transaction in Uk.
        sl_tid, sl_util, sl_pru = sl[j].values()  # Get values for the j-th transaction in Ul.
        sk_id = int(sk_tid)  # Transaction ID from Uk.
        sl_id = int(sl_tid)  # Transaction ID from Ul.

        # Case 1: Matching transaction IDs
        if sk_tid == sl_tid:
            pfutil = pfutils.get(sk_tid, 0)  # Get the prefix utility for the matching transaction.

            # Calculate the utility and PRU after considering the prefix utility.
            util = sk_util + sl_util - pfutil
            rutil = min(sk_pru, sl_pru)
            if (not pfutils and Uk['Item'] == '20' and Ul['Item'] == '2'):
                      print(sk_tid, util)
            # Add the utility and PRU to the combined result.
            C["Utility"] += util
            C["PRU"] += rutil
            C["TI"].append({
                "TID": sk_tid,   # Add the transaction ID.
                "Utility": util, # Add the combined utility.
                "PRU": rutil     # Add the combined PRU.
            })

            # Move to the next transaction in both lists.
            i += 1
            j += 1

        # Case 2: Transaction ID in Uk is greater than in Ul, move to the next transaction in Ul.
        elif sk_id > sl_id:
            j += 1

        # Case 3: Transaction ID in Ul is greater than in Uk, update utility and move to the next transaction in Uk.
        else:
            x -= (sk_util + sk_pru)  # Deduct the utility and PRU from Uk.

            # If the combined utility goes below the minimum utility threshold, return None.
            if x < min_util:
                return None
            i += 1

    # If no valid combination was found, return None.
    if not C:
        return None
    # Return the combined utility list.
    return C


def EHMIN_Mine(P={}, Ul=[], pref=[]):
    """
    Mine high-utility itemsets from a given prefix tree by recursively combining utility lists
    and calculating the utility and PRU for candidate itemsets.

    This function is part of the High Utility Itemset Mining (EHMIN) algorithm, where it explores
    the search space of possible itemsets, merging candidate itemsets if their combined utility
    is greater than or equal to a minimum utility threshold (`min_util`).

    Parameters:
    P (dict): A prefix tree node containing the following keys:
              - 'Item' (str): The item identifier.
              - 'Utility' (float): The utility of the itemset.
              - 'PRU' (float): The Prefix Remaining Utility (PRU) of the itemset.
              - 'TI' (list of dicts): A list of transactions, each represented by:
                - 'TID' (int): Transaction ID.
                - 'Utility' (float): The utility of the item in the transaction.

    Ul (list): A list of utility lists, where each utility list contains the following keys:
              - 'Item' (str): The item identifier.
              - 'Utility' (float): The utility of the item.
              - 'PRU' (float): The Prefix Remaining Utility for the item.
              - 'TI' (list of dicts): A list of transactions that includes:
                - 'TID' (int): Transaction ID.
                - 'Utility' (float): Utility of the item in the transaction.
                - 'PRU' (float): Prefix Remaining Utility for the item in the transaction.

    pref (list): The current prefix, a list of items that forms the prefix of a candidate itemset.

    Returns:
    None: The function does not return any value but updates the global `HUP` list with the high-utility itemsets.
          Each high-utility itemset is represented as a list containing:
          - The itemset (list of item identifiers).
          - The total utility of the itemset.
    """
    pfutils = {}

    # Step 1: Extract prefix utilities from the transactions in the prefix tree node (P).
    if P:
        for s in P['TI']:
            pfutils[s['TID']] = s['Utility']  # Map transaction ID to utility.

    n = len(Ul)
    # Step 2: Iterate over the utility lists (Ul) to explore candidate itemsets.
    for i in range(n):
        uk = Ul[i]
        uk_key = uk['Item']  # Item identifier for the first itemset.

        # Step 3: If the utility of the itemset is greater than or equal to the minimum utility,
        # add the itemset to the list of high-utility itemsets (HUP).
        if uk["Utility"] >= min_util:
            res = pref + [uk_key]
            HUP.append([res, uk["Utility"]])  # Add the itemset and its utility to HUP.

        # Step 4: Skip items where the combined utility and PRU are less than the minimum utility.
        if uk["Utility"] + uk["PRU"] < min_util:
            continue

        # Step 5: Attempt to combine the current itemset (uk) with other itemsets (Ul) to form candidate itemsets.
        CL = []  # List to store combined itemsets.

        for j in range(i + 1, n):
            ul = Ul[j]
            ul_key = ul['Item']  # Item identifier for the second itemset.

            # Step 6: Check the EUCS (Extended Utility Co-occurrence Symmetry) matrix to ensure that
            # the pairwise utility between items is above the minimum utility threshold.
            index_i = items_sorted.index(uk_key)
            index_j = items_sorted.index(ul_key)
            if EUCS[index_i][index_j] < min_util:
                continue  # Skip itemsets with insufficient utility.
            if pref==[] and uk_key == '20' and ul_key== '2':
              print(uk)
              print(ul)
            # Step 7: Combine the two itemsets and check if the resulting itemset has sufficient utility.
            C = EHMIN_Combine(uk, ul, pfutils)
            if pref==[] and uk_key == '20' and ul_key== '2':
              print("CCC", C)
            if C is not None:
                CL.append(C)  # If valid, add the combined itemset to the candidate list.

        # Step 8: If candidate itemsets were generated, recursively mine high-utility itemsets.
        if CL:
            EHMIN_Mine(uk, CL, list(pref) + [uk_key])  # Recurse with the updated prefix.

        

def EHMIN(Db, minUtil, k):
  global min_util, HUP
  min_util = minUtil
  items = first_scan(Db)
  print(items)
  EUCS, UL = second_scan(Db, items)
  HUP = []
  for u in UL:
      print(u)
  print("EUCS", EUCS)
  EHMIN_Mine({}, UL, [])
  HUP = sorted(HUP, key = lambda x: x[1], reverse=True)
  return HUP[:min(k, len(HUP))]

D = []
i = 0
with(open("dataset.txt", "r")) as f:
    for line in f:
        i += 1
        line = line.strip()
        data_split = line.split(":")
        items = list(map(str, data_split[0].split(" ")))
        quantities = [1 for _ in range(len(items))]
        utilities = list(map(int, data_split[2].split(" ")))
        D.append({
            "TID": str(i),
            "Items": items,
            "Quantities": quantities,
            "Profits": utilities
          })

# D = [
#     {
#         'TID': '1',
#         'Items': ['a', 'b', 'd', 'e', 'f', 'g'],
#         'Quantities': [2, 2, 1, 3, 2, 1],
#         'Profits': [-2, 1, 4, 1, -1, -2]
#     },
#     {
#         'TID': '2',
#         'Items': ['b', 'c'],
#         'Quantities': [1, 5],
#         'Profits': [-1, 1]
#     },
#     {
#         'TID': '3',
#         'Items': ['b', 'c', 'd', 'e', 'f'],
#         'Quantities': [2, 1, 3, 2, 1],
#         'Profits': [-1, 1, 4, 1, -1]
#     },
#     {
#         'TID': '4',
#         'Items': ['c', 'd', 'e'],
#         'Quantities': [2, 1, 3],
#         'Profits': [1, 4, 1]
#     },
#     {
#         'TID': '5',
#         'Items': ['a', 'f'],
#         'Quantities': [2, 3],
#         'Profits': [2, -1]
#     },
#     {
#         'TID': '6',
#         'Items': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
#         'Quantities': [2, 1, 4, 2, 1, 3, 1],
#         'Profits': [1, 1, 1, 4, 1, -1, -2]
#     },
#     {
#         'TID': '7',
#         'Items': ['b', 'c', 'e'],
#         'Quantities': [3, 2, 2],
#         'Profits': [1, 2, 2]
#     }
# ]

res = EHMIN(D, 5e8, 10)
print()
for r in res:
    print(r)

