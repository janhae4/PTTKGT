def EHMIN(Db, min_util, k):
    def EU(iX, Tk=None):
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
    
    def get_sorted_key(x, positive, hybrid):
        if x in positive:
            return -1
        elif x in hybrid:
            return 0
        else:
            return 1
        

    def PTU(Tk):
        return sum (
            U(ix, Tk)
            for ix in Tk['Items']
            if EU(ix, Tk) > 0
        )

    def PTWU(X, cache=None):
        if not cache:
            return sum (
                PTU(Tk)
                for Tk in Db
                if all(ix in Tk['Items'] for ix in X)
            )

        else:
            return sum (
                Tk['PTWU']
                for Tk in cache.values()
                if all(ix in Tk['Items'] for ix in X)
            )
        
    def sorted_transactions(items):
        map = {item: index for index, item in enumerate(items)}
        for Tk in D:
            zip_list = list(zip(Tk['Items'], Tk['Quantities'], Tk['Profits']))
            sorted_item = sorted(zip_list, key = lambda x: map.get(x[0], len(items)))
            Tk['Items'], Tk['Quantities'], Tk['Profits'] = zip(*sorted_item)
        return Db     
    
 
    def RTWU(Tk):
        return sum (
            Tk['Profits'][index] * Tk['Quantities'][index]
            for index, ix in enumerate(Tk['Items'])
            if Tk['Profits'][index] > 0
        )
        
    def PRU(X, Tk=None):
        if X == "":
            return 0 
        
        if Tk:
            transaction = Tk['Items']
            index = transaction.index(X) + 1
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
                    items[ix]["RTWU"] += RTWU(Tk)
                else:
                    items[ix] = {
                        "RTWU": RTWU(Tk),
                        "Supp": 1
                }
        hybrid = positive & negative
        positive -= hybrid
        negative -= hybrid
        items_sorted = sorted(items, key = lambda x: (get_sorted_key(x, positive, hybrid), items[x]['RTWU'], items[x]['Supp']))
        return items_sorted
    
    def second_scan(Db, items):
        Db = sorted_transactions(items)

        UL_dict = {}
        EUCS_cache = {}
        for Tk in Db:
            tmp = {}

            for ix in Tk['Items']:
                tmp[ix] = U(ix, Tk)
                        
            for idx, utility in tmp.items():
                pru = PRU(idx, Tk)
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
            for j in range(i + 1, n):
                item_set = {items[i], items[j]}
                EUCS[i][j] = PTWU(item_set, EUCS_cache)      
        print("EUCS calculated successfully...")
        
        UL = list(UL_dict.values())
        UL = sorted(UL, key = lambda x: items.index(x['Item']))
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
                res = pref + [uk_key]
                HUP.append([res, uk["Utility"]])
                
            if uk["Utility"] + uk["PRU"] >= min_util:
                CL = []
                for j in range(i + 1, n):
                    ul= Ul[j]
                    ul_key = ul['Item']
                    
                    index_i = items_sorted.index(uk_key[0])
                    index_j = items_sorted.index(ul_key[0])

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

    global HUP
    items = first_scan(Db)
    EUCS, UL = second_scan(Db, items)
    HUP = []
    EHMIN_Mine({}, UL, [])
    # HUP = sorted(HUP, key = lambda x: x[1], reverse=True)
    return HUP[:min(k, len(HUP))]

D = []
i = 0
with(open("mushroom.txt", "r")) as f:
    for line in f:
        i += 1
        line = line.strip()
        data_split = line.split(":")
        items = data_split[0].split(" ")
        quantities = [1 for _ in range(len(items))]
        utilities = list(map(int, data_split[2].split(" ")))
        D.append({
            "TID": i,
            "Items": items,
            "Quantities": quantities,
            "Profits": utilities
          })

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

Result = EHMIN(D, 25, 100)
for r in Result:
      print(r)  
            
            
            

