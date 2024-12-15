import random
import os

def generate_transaction(item_count, max_item_id, max_utility):
    """Tạo một giao dịch ngẫu nhiên với danh sách item, RTWU và utility."""
    # Tạo danh sách item ngẫu nhiên và sắp xếp tăng dần
    items = sorted(random.sample(range(2, max_item_id + 1), item_count))
    
    # Tạo RTWU ngẫu nhiên
    rtw_value = random.randint(100, 500)
    
    # Tạo danh sách utility ngẫu nhiên
    utilities = [random.randint(-max_utility, max_utility) for _ in range(item_count)]
    
    # Format thành chuỗi theo yêu cầu
    transaction = f"{' '.join(map(str, items))}:{rtw_value}:{' '.join(map(str, utilities))}"
    return transaction

def generate_dataset(transaction_count, item_count, max_item_id, max_utility, output_file):
    """Tạo dataset và ghi vào file."""
    
    dataset = []
    for _ in range(transaction_count):
        transaction = generate_transaction(item_count, max_item_id, max_utility)
        dataset.append(transaction)
    
    # Ghi dataset vào file
    with open(output_file, "w") as f:
        for transaction in dataset:
            f.write(transaction + "\n")
    
    print(f"Dataset đã được tạo thành công và lưu tại {output_file}")

# Thông số dataset
transaction_count = 200  # Số lượng giao dịch
item_count = 10         # Số lượng item trong mỗi giao dịch
max_item_id = 25       # Giá trị lớn nhất của ID item
max_utility = 50          # Giá trị lớn nhất của utility
output_file = "dataset.txt"  # Tên file để lưu dataset

# Gọi hàm tạo dataset
generate_dataset(transaction_count, item_count, max_item_id, max_utility, output_file)
