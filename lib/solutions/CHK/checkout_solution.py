import csv



def load_prices():
    """
    Returns dict of information in prices.csv
    Format: {SKU : {"price": price, "deal": deal}}
    Where `deal` can be null
    """
    with open('prices.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        prices = {
            row[0]: {"price": row[1], "deal": row[2]}
            for row in csv_reader
        }

    return prices


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
    total_cost = 0
    prices = load_prices()
    for sku in skus.split(","):
        if sku not in prices:
            # invalid input
            return -1
        else:
            total_cost += prices[sku]["price"]

    return total_cost



