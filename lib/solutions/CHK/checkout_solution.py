import csv
import re


def load_prices():
    """
    Returns dict of information in prices.csv
    Format: {SKU : {"price": price, "deal": deal}}
    Where `deal` can be null
    """
    with open('prices.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        prices = {
            row[0]: {"price": int(row[1]), "deal": row[2]}
            for row in csv_reader
        }
    return prices


def parse_sku(sku):
    """
    Converts an sku and it's quantity into separate parts.
    eg.
    A -> 1, A
    3A -> 3, A
    Args:
        sku (string) - contains sku item and an optional quantity
                        (defaults to 1)
    Returns:
        int - quantity of item
        str - item sku code
    """
    # separate numbers and letters
    result = re.findall('\d+|\D+', sku)
    if len(result) == 1:
        # if quantity not specified, default to 1
        quantity = 1
        item = result[0]
    elif len(result) != 2:
        # something has gone wrong with the format
        return None, None
    else:
        quantity = int(result[0])
        item = result[1]

    return quantity, item


def get_cost(prices, item, quantity):
    """
    Calculates cost of item based on quantity, including any deals
    Args:
        prices (dict): {item_code: {"price": price, "deal": deal}}
        item (str): item_code
        quantity (int): quantity of item in basket
    """
    item_price = prices[item]
    if item_price["deal"] and quantity >= get_deal_quantity(item_price["deal"]):

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
        quantity, item = parse_sku(sku)
        if None in (item, quantity) or item not in prices:
            # invalid input
            return -1
        else:
            total_cost += get_cost(prices, item, quantity)
#            total_cost += prices[item]["price"]

    return total_cost




