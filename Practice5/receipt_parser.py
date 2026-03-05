import re
with open("Practice5/raw.txt", "r") as file:
    text = file.read()

#1.Extract all prices from the receipt
import re
pattern = r"(\d+,\d+)\s*x\s*([\d ]+,\d{2})"
matches = re.findall(pattern, text)
print("Receipt rows:")
for quantity, price in matches:
    q = float(quantity.replace(",", "."))
    p = float(price.replace(" ", "").replace(",", "."))
    total_price = q * p
    print(f"{total_price:.2f}")

#2.Find all product names
product_receipt = r"^\s*\d+\.\s*\n(.+)$"
products = re.findall(product_receipt, text, flags=re.MULTILINE)

print("Products: ", len(products))
for p in products:
    print(p)

#3.Calculate total amount
total_receipt = r"ИТОГО:\s*\n([\d ]+,\d{2})"
total = re.search(total_receipt, text)

if total:
    total = total.group(1)
    print("Total amount:", total)

#4.Extract date and time information
dt_receipt = r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})"
dt_match = re.search(dt_receipt, text)

if dt_match:
    date = dt_match.group(1)
    time = dt_match.group(2)
    print("Date:", date)
    print("Time:", time)

#5.Find payment method
payment_types = r"(Банковская карта|Наличные)"
payment_match = re.search(payment_types, text)

if payment_match:
    pm_method = payment_match.group(1)
    print("Payment method:", pm_method)

#6.Create a structured output (JSON or formatted text)
receipt_data = {
    "products": products,
    "prices": total_price,
    "total": total,
    "date": date,
    "time": time,
    "payment_method": pm_method
}

print("\nStructured receipt data:")

for key, value in receipt_data.items():
    print(f"\n{key}:")
    
    if isinstance(value, list):
        for v in value:
            print(v)
    else:
        print(value)