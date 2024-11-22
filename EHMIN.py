def EHMIN(Db, rate, k):
    def EU(iX, Tk=None):
        if Tk:
            index = Tk['Items'].index(iX)
            return Tk['Profits'][index]
        else:   
            for transaction in Db:
                if iX in transaction['Items']:
                    index = transaction['Items'].index(iX)
                    return transaction['Profits'][index]
            return 0

    def IU(iX, Tk):
        return Tk["Quantities"][Tk['Items'].index(iX)] if iX in Tk['Items'] else 0

    def U(X, Tk=None):
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
        
    def PU(X, Tk=None):
        if Tk:
            for ix in X:
                print(ix, IU(ix, Tk), EU(ix, Tk))
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
    
    def get_sorted_key(x, positive, hybrid, negative):
        if x in positive:
            return (-1, RTWU(x))
        elif x in hybrid:
            return (0, RTWU(x))
        else:
            return (1, RTWU(x))
        

    def PTU(Tk):
        return sum (
            U(ix, Tk)
            for ix in Tk['Items']
            if EU(ix, Tk) > 0
        )

    def PTWU(X):
        return sum (
            PTU(Tk)
            for Tk in Db
            if all(ix in Tk['Items'] for ix in X)
        )

    def get_sort_key(x, items):
        eu_value = EU(x)
        if (eu_value > 0):
            return (-1, PTWU(x))
        else:
            return (1, items[x]["Supp"], -PTWU(x))
        
    def sorted_transactions(items):
        map = {item: index for index, item in enumerate(items)}
        for Tk in D:
            zip_list = list(zip(Tk['Items'], Tk['Quantities'], Tk['Profits']))
            sorted_item = sorted(zip_list, key = lambda x: map.get(x[0], len(items)))
            Tk['Items'], Tk['Quantities'], Tk['Profits'] = zip(*sorted_item)
        return Db     
    
    def sorted_database(items):
        map = {item: index for index, item in enumerate(items)}
        return sorted(Db, key = lambda x: (map.get(x['Items'][-1]), len(x['Items'])), reverse=True)

    def minUtil(delta):
        return delta * sum (
            PTU(Tk)
            for Tk in D
        ) 
 
    def RTWU(X):
        return sum (
            Tk['Profits'][index] * Tk['Quantities'][index]
            for Tk in Db
            for index, ix in enumerate(Tk['Items'])
            if all(x in Tk['Items'] for x in X)
            and Tk['Profits'][index] > 0
        )
        
    def PRU(X, Tk=None):
        if X == "":
            return 0 
        
        if Tk:
            transaction = Tk['Items']
            index = transaction.index(X[-1]) + 1
            RP = transaction[index :]
            return sum (
                U(iRP, Tk)
                for iRP in RP
                if EU(iRP, Tk) > 0
            )
        else:
            return sum (
                PRU(X, Tk)
                for Tk in D
                if all(item in Tk['Items'] for item in X)
            )
            
    def first_scan(Db):
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
                else:
                    items[ix] = {
                        "PTWU": PTWU(ix),
                        "RTWU": RTWU(ix),
                        "Supp": 1
                }
        hybrid = positive.intersection(negative)
        positive.difference_update(hybrid)
        negative.difference_update(hybrid)
        items_sorted = sorted(items, key = lambda x: get_sorted_key(x, positive, hybrid, negative))
        print(items)
        return items_sorted
    
    def second_scan(Db, items):
        min_util = minUtil(rate)
        Db = sorted_transactions(items)

        UL = []
        for Tk in Db:
            PTU_k = 0
            print("PTWU(a): ", PTWU("a"))
            for ix in Tk['Items']:
                if PTWU(ix) > min_util:
                    PTU_k += PU(ix, Tk)
            print(f"TOTAL={PTU_k}")
            tmp = {}
            newPTWU = 0
            for ix in Tk['Items']:
                tmp[ix] = U(ix, Tk)
                if (PTWU(ix) > min_util):
                    newPTWU += PTWU(ix) + PTU_k 
                    
            reverse_dict = dict(reversed(tmp.items()))
            for idx in reverse_dict:
                existing_entry = next((item for item in UL if item['Item'] == idx), None)
                if existing_entry:
                    existing_entry["Utility"] += reverse_dict[idx]
                    existing_entry["PRU"] += PRU(idx, Tk)
                    existing_entry["TI"].append({
                        "TID": Tk['TID'],
                        "Utility": reverse_dict[idx],
                        "PRU": PRU(idx, Tk)
                    })
                else:
                    UL.append({
                            'Item': idx,
                            "Utility": U(idx, Tk),
                            "PRU": PRU(idx, Tk),
                            "TI": [
                                {
                                "TID": Tk['TID'],
                                "Utility": reverse_dict[idx],
                                "PRU": PRU(idx, Tk)
                                }
                            ] 
                    })

        n = len(items)

        EUCS = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                item_set = {items_sorted[i], items_sorted[j]}
                EUCS[i][j] = PTWU(item_set) 

        print(items_sorted)
        print()
        print("\t", "\t".join(items_sorted))
        for i in range(len(UL)):
            print(items_sorted[i], end="\t")
            for j in range(len(UL)):
                print(EUCS[i][j], end="\t")
            print()
        print()

        UL = sorted(UL, key = lambda x: items_sorted.index(x['Item']))
        return EUCS, UL

    def EHMIN_Mine(P={}, Ul=[], pref=[]):   
        pfutils = {}
        
        if P:
            for s in P['TI']:
                pfutils[s['TID']] = s['Utility']
        
        n = len(Ul)
        
        for i in range(n):
            uk= Ul[i]
            uk_key = uk['Item']     

            if uk["Utility"] >= min_util:
                res = list(pref) + [uk_key]
                HUP.append([res, uk["Utility"]])
                
            if uk["Utility"] + uk["PRU"] >= min_util:
                CL = []
                for j in range(i + 1, n):
                    ul= Ul[j]
                    ul_key = ul['Item']
                    
                    index_i = items_sorted.index(uk_key[0])
                    index_j = items_sorted.index(ul_key[0])
                    print(uk_key, ul_key, index_i, index_j, EUCS[index_i][index_j])
                    if EUCS[index_i][index_j] >= min_util:
                        C = EHMIN_Combine(uk, ul, pfutils)
                        if C is not None:
                            CL.append(C)
                if CL:
                    EHMIN_Mine(uk, CL, list(pref) + [uk_key])
          
    def EHMIN_Combine(Uk={}, Ul={}, pfutils={}):
        C = {
            "Item": Ul['Item'],
            "Utility": 0,
            "PRU": 0,
            "TI":[]
        }
        x = Uk['Utility'] + Uk['PRU']
        y = Uk['Utility']
        
        sk = Uk['TI']
        sl = Ul['TI']
            
        i, j = 0, 0

        pfutil = 0
        while(i < len(sk) and j < len(sl)):
            sk_tid, sk_util, sk_pru = sk[i].values()
            sl_tid, sl_util, sl_pru = sl[j].values()
            
            if sk_tid == sl_tid:
                pfutil = pfutils.get(sk_tid, 0)
                util = sk_util + sl_util - pfutil
                rutil = min(sk_pru, sl_pru)
                
                C["Utility"] += util 
                C["PRU"] = rutil
                C["TI"].append({
                    "TID": sk_tid,
                    "Utility": util,
                    "PRU": rutil
                })
                
                y += sk_util + sl_util - pfutil
                if sk_pru == 0 and y < min_util:
                    return None
                
                i += 1
                j += 1
                
            elif sk_tid > sl_tid:
                j += 1
                
            else:
                x -= (sk_util + sk_pru)

                if x < min_util:
                    return None
                i += 1
            
        if not C:
            return None
        return C

    global min_util
    global HUP
    min_util = minUtil(rate)
    items = first_scan(Db)
    EUCS, UL = second_scan(Db, items)
    HUP = []
    EHMIN_Mine({}, UL, ())

    return HUP[:min(k, len(HUP))]

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


Result = EHMIN(D, 0.356, 20)
print(min_util)
for r in Result:
      print(r)  
            
            
            

