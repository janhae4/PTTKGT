D = [
    {
        'TID': 'T1',
        'Transaction': ['a', 'b', 'c', 'd'],
        'Quantity': [1, 2, 2, 1],
        'Profit': [4, 3, 1, -1]
    },
    {
        'TID': 'T2',
        'Transaction': ['a', 'b', 'c', 'd', 'e'],
        'Quantity': [1, 3, 3, 2, 2],
        'Profit': [4, 3, 1, -1, 2]
    },
    {
        'TID': 'T3',
        'Transaction': ['a', 'c', 'e'],
        'Quantity': [1, 6, 3],
        'Profit': [4, 1, 2]
    },
    {
        'TID': 'T4',
        'Transaction': ['b', 'd', 'e'],
        'Quantity': [3, 5, 2],
        'Profit': [3, -1, 2]
    },
    {
        'TID': 'T5',
        'Transaction': ['b', 'c', 'd', 'e'],
        'Quantity': [1, 5, 1, 4],
        'Profit': [3, 1, -1, 2]
    },
    {
        'TID': 'T6',
        'Transaction': ['c', 'd', 'e'],
        'Quantity': [2, 1, 1],
        'Profit': [1, -1, 2]
    }
]



def iu(x, Tk):
    return Tk["Quantity"][Tk["Transaction"].index(x)] if x in Tk["Transaction"] else 0
print(iu("b", D[3]))

def eu(x, Tk = None):
    if Tk:
        return Tk["Profit"][Tk["Transaction"].index(x)]
    else:
        for Tk in D:
            if x in Tk["Transaction"]:
                return eu(x, Tk)
    return 0

def u(X, Tk=None):
    if Tk:
        return sum(
            iu(ix, Tk) * eu(ix, Tk)
            for ix in X
        )
    else:
        return sum(
            u(X, Tk)
            for Tk in D
            if all(ix in Tk["Transaction"] for ix in X)
        )
print(u("b", D[3]))
print(u("ce", D[5]))
print(u("ce"))

def tu(Tk):
    return sum(
        u(x, Tk)
        for x in Tk["Transaction"]
    )
print(tu(D[5]))

def twu(X):
    return sum (
        tu(Tk)
        for Tk in D
        if all(x in Tk["Transaction"] for x in X)
    )
print(twu("abc"))

def Ptu(Tk):
    return sum (
        u(x, Tk)
        for x in Tk["Transaction"]
        if u(x) > 0
    )
print(Ptu(D[1]))

def Ptwu(X):
    return sum (
        Ptu(Tk)
        for Tk in D
        if all(x in Tk["Transaction"] for x in X)
    )
print(Ptwu("ab"))

def PSU(a, y, D):
    X = [a] + [y]
    total = 0
    for Tk in D:
        if all(x in Tk["Transaction"] for x in X):
            if (eu(y, Tk) < 0):
                return u(x, Tk)
            else:
                items = Tk['Transaction']
                total += u(X, Tk)
                start = Tk["Transaction"].index(y) + 1
                for i in range(start,len(items)):
                    u_value = u([items[i]], Tk)
                    if (u_value > 0):
                        total += u([items[i]], Tk)
    return total

print("PSUU", PSU("b", "e", D))

def re(a, Tk):
    index = Tk['Transaction'].index(a)
    return sum (
        (Tk['Profit'][i] * Tk['Quantity'][i])
        for i in range(index, len(Tk['Transaction']))
        if Tk['Profit'][i] > 0
    )

def create_PSU_UA(D, a, secondaryItems):
    PSU_UA = {}
    for x in secondaryItems:
        PSU_UA[x] = PSU(a, x, D)
    return PSU_UA
 
def PLU(a, y, D):
    X = [a] + [y]
    total = 0
    for Tk in D:
        if all(ix in Tk['Transaction'] for ix in X):
            total += re(a, Tk)
    return total
print("PLU(b, c)", PLU("b", "e", D))
                
            
def get_sorted_key(x):
    if (eu(x) > 0):
        return (-1, Ptwu(x))
    else:
        return (1, Ptwu(x))

def sorted_transactions_items(D, items):
    ordered_map = {item: i for i, item in enumerate(items)}
    for transaction in D:
        zip_trans = list(zip(transaction['Transaction'], transaction['Profit'], transaction['Quantity']))
        sorted_item = sorted(zip_trans, key = lambda x: ordered_map.get(x[0]))
        transaction['Transaction'], transaction['Profit'], transaction['Quantity'] = zip(*sorted_item)
    return D

d = ['a', 'c', 'b', 'd', 'e']
d = sorted(d, key=lambda x: get_sorted_key(x))
print(d)

def Pru(X, Tk):
    last_item = X[-1]
    return sum (
        u(i, Tk)
        for i in Tk["Transaction"]
        if Tk["Transaction"].index(last_item) < Tk["Transaction"].index(i)
        and u(i,Tk) > 0    
    )
print(Pru("ab", D[0]))

def PRIU(x):
    return sum (
        u(x, Tk)
        for Tk in D
        if x in Tk["Transaction"] 
    )
    
def PRIU_strategy(PRIU=list, k=int):
    PRIU.sort(reverse=True)
    return PRIU[k]


def LIU(x, y):
    return  sum (
        u(z, Tk)
        for Tk in D
        if all(item in Tk["Transaction"] for item in [x, y])
        for z in Tk["Transaction"]
        if Tk["Transaction"].index(x) <= Tk["Transaction"].index(z) <= Tk["Transaction"].index(y)
    )
def print_transaction_db(transaction_db):
    # Find the maximum lengths for formatting
    max_tid_len = max(len(str(tx["TID"])) for tx in transaction_db)
    max_trans_len = max(len(str(tx["Transaction"])) for tx in transaction_db)
    max_quant_len = max(len(str(tx["Quantity"])) for tx in transaction_db)
    max_util_len = max(len(str(tx["Profit"])) for tx in transaction_db)
    # Print header
    print("\n" + "="*90)
    print(f"{'Transaction Database':^90}")
    print("="*90)
    
    # Print column headers
    header = (f"| {'TID':^{max_tid_len}} | "
             f"{'Transaction':^{max_trans_len}} | "
             f"{'Quantity':^{max_quant_len}} | "
             f"{'Profit':^{max_util_len}}|  "
             f"{'Utility':^{max_util_len}}   |"  )
    print(header)
    print("-"*len(header))
    
    # Print each transaction
    for tx in transaction_db:
        u = [tx['Quantity'][i] * tx['Profit'][i] for i in range(len(tx['Quantity']))]
        print(f"| {tx['TID']:^{max_tid_len + 2}} | "
              f"{str(tx['Transaction']):<{max_trans_len}} | "
              f"{str(tx['Quantity']):<{max_quant_len}} | "
              f"{str(tx['Profit']):<{max_util_len}} | "
              f"{str(u):<{max_util_len}}  | ")
    print("-"*len(header))
    print()
    
print_transaction_db(D)

print(f"|{'':^2} | {'b':<2} | {'c':<2} | {'e':<2} |")
print(f"{"-"*20}")
for x in ['a', 'b', 'c']:
    print(f"| {x:<1} |", end="")
    for y in ['b', 'c', 'e']:
        if x == y: 
            value = 0
        else:
            value = LIU(x, y)
        print(f" {value:<2} |", end="")
    print(f"\n{"-"*20}")
    
def remove_item_out_of_transaction(D, items):
    for Tk in D:
        for transaction in Tk["Transaction"]:
            if transaction not in items:
                index = Tk["Transaction"].index(transaction)
                Tk["Transaction"].pop(index)
                Tk["Quantity"].pop(index)
                Tk["Profit"].pop(index)
    return D
                
def PLIU_E_strategy(LIUS, PIQU_LIU, k, minUtil):
    PIQU_LIU.add(LIUS[0])
    if PIQU_LIU[k] > minUtil:
        return PIQU_LIU[k]
    return minUtil

def PLIU_LB_strategy(LIUS, PIQU_LIU, PIQU_LB_LIU, k):
    pass

def binarySearch(secondary, x):
    pass

def TKN(D, k):
    alpha = []
    x = set()
    eta = set()
    for Tk in D:
        for item in Tk["Transaction"]:
            if eu(item, Tk) > 0:
                x.add(item)
            else:
                eta.add(item)
    print("X, ETA", x, eta)

    TKHQ = []
    minUtil = 0
    UA = {}
    
    for item in x | eta:
        UA[item] = Ptwu(item)
    
    keys = sorted(UA.keys(), key=lambda x: (-1, Ptwu(x)) if eu(x) > 0 else (1, Ptwu(x)))
    UA = {k:UA[k] for k in keys}
    print(UA)
    
    PRIU_list = [PRIU(item) for item in x]
    print(PRIU_list)
    minUtil = PRIU_strategy(PRIU_list, k)
    secondary_items = [z for z in UA.keys() if Ptwu(z) >= minUtil]
    print(secondary_items)
    D = remove_item_out_of_transaction(D, secondary_items)
    D = sorted_transactions_items(D, secondary_items)
      
    PSU_UA = create_PSU_UA(D, alpha, secondary_items)
    LIUS = [[0 for _ in range(len(x))] for _ in range(len(x))]
    
    print(f"\n|{'':^2} | {'b':<2} | {'c':<2} | {'e':<2} |")
    print(f"{"-"*20}")
    
    item_x = sorted(list(x), key=lambda x: UA[x])
    for i in range(len(item_x) - 1):
        print(f"| {item_x[i]:<1} |", end="")
        for j in range(1, len(item_x)):
            if item_x[i] == item_x[j]: 
                value = 0                
            else:
                value = LIU(item_x[i], item_x[j])
            LIUS[i][j] = value
            print(f" {value:<2} |", end="")
        print(f"\n{"-"*20}")
    Q2 = []
    
    PLIU_E_strategy(LIUS, TKHQ, k, minUtil)
    print("minUtil: ", minUtil)
    PLIU_LB_strategy(LIUS, TKHQ, Q2, k)
    primary = [x for x in secondary_items if PSU(alpha, x) >= minUtil]
    topK = search(alpha, 0, eta, D, primary, secondary_items, minUtil, TKHQ, k)

def search(alpha, u, eta, D, primary, secondary, minUtil, TKHQ, k):
    for z in primary:
        B = [alpha] + [z]
        uB = u(B, D=D)
        
        if (uB >= minUtil):
            TKHQ.add([B, uB])
            if len(TKHQ) == k:
                minUtil = TKHQ[-1]
    return []
            
    
    
TKN(D, 3)
