import csv



def load_prices():
    """
    Returns list of tuples of information in prices.csv
    Format: [(SKU, price, deal)]
    Where `deal` can be null
    """
    with open('prices.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
    

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    """
    Returns total cost of all items listed in `skus`
    Args:
        skus (string) - the SKUs of all the products in the basket
    Returns:
        Integer representing the total checkout value of the items 
    """
    



