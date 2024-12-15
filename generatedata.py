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
      items = transaction['Items']
      profits = transaction['Profits']
      quantities = transaction['Quantities']
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
import random
random.seed(1)
def partition_and_process_items(D, positive_ratio=0.4, negative_ratio=0.4, hybrid_ratio=0.2):
    """
    Segment items into three distinct categories and process profits.
    
    Parameters:
    D: List of transactions (each as a dictionary with 'Items' and 'Profits').
    positive_ratio: Fraction of items to categorize as positive profit only.
    negative_ratio: Fraction of items to categorize as negative profit only.
    hybrid_ratio: Fraction of items to categorize as hybrid (positive or negative).
    
    Returns:
    processed_transactions: List of transactions with processed profits.
    """
    all_items = set(item for transaction in D for item in transaction['Items'])
    total_items = len(all_items)
    
    # Ensure the ratios add up to 1
    assert abs(positive_ratio + negative_ratio + hybrid_ratio - 1) < 1e-6, "Ratios must sum to 1"
    
    # Shuffle and divide items into groups based on the ratios
    shuffled_items = list(all_items)
    random.shuffle(shuffled_items)
    split1 = int(total_items * positive_ratio)
    split2 = split1 + int(total_items * negative_ratio)
    
    positive_items = set(shuffled_items[:split1])
    negative_items = set(shuffled_items[split1:split2])
    hybrid_items = set(shuffled_items[split2:])
    
    # Process profits for each transaction
    processed_transactions = []
    for transaction in D:
        items = transaction['Items']
        profits = transaction['Profits']
        processed_profits = []
        
        for item, profit in zip(items, profits):
            if item in positive_items:
                processed_profits.append(profit)  # Keep as positive
            elif item in negative_items:
                processed_profits.append(-abs(profit))  # Make negative
            elif item in hybrid_items:
                flag = random.choice([-1, 1])  # Randomly choose positive or negative
                processed_profits.append(profit * flag)
        
        processed_transactions.append({
            "TID": transaction["TID"],
            "Items": items,
            "Quantities": transaction["Quantities"],
            "Profits": processed_profits
        })
    
    return processed_transactions, positive_items, negative_items, hybrid_items


D = []
i = 0
with(open("mushroom.txt", "r")) as f:
    for line in f:
        i += 1
        line = line.strip()
        data_split = line.split(":")
        items = data_split[0].split(" ")
        quantities = [1 for _ in range(len(items))]

        if (len(data_split[2]) == 1):
            utilities = list(map(int, data_split[2]))
        else:
            utilities = list(map(int, data_split[2].split(" ")))
        D.append({
            "TID": i,
            "Items": items,
            "Quantities": quantities,
            "Profits": utilities
          })
rho, delta, eta, rtwu_dict = partion_items(D)

# Example usage
processed_transactions, positive_items, negative_items, hybrid_items = partition_and_process_items(D)

# Outputs
print(f"Positive items: {len(positive_items)}")
print(f"Negative items: {len(negative_items)}")
print(f"Hybrid items: {len(hybrid_items)}")

def calculate_rtwu(transaction):
    profits = transaction["Profits"]
    quantities = transaction["Quantities"]
    rtwu = sum(p * q for p, q in zip(profits, quantities) if p > 0)
    return rtwu

# Ghi dữ liệu vào file với RTWU
output_file = "mushroom.txt"

with open(output_file, "w") as f:
    for transaction in D:
        items = " ".join(transaction["Items"])
        rtwu = calculate_rtwu(transaction)
        profits = " ".join(map(str, transaction["Profits"]))
        line = f"{items}:{rtwu}:{profits}\n"
        f.write(line)

print(f"Dữ liệu đã được ghi vào file {output_file}")