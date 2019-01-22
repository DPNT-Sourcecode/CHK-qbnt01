from collections import Counter
import csv
import operator
import re


def load_prices():
    """
    Loads data from storage (prices.csv)
    Returns:
        item_prices (dict): price information for each item - {item: price}
        item_deals (dict): all deals that contain the item  - {item: [deal1, deal2, etc.]}
    """
    item_prices = {}
    item_deals = {}
    with open('prices.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for (item, price, deals) in csv_reader:
            item_prices[item] = int(price)
            if deals:
                item_deals[item] = deals

    return item_prices, item_deals


def parse_deal_code(deal_code):
    """
    Converts an sku and it's quantity into separate parts.
    eg.
    A -> 1, A
    3A -> 3, A
    Args:
        deal_code (string) - contains sku item and an optional quantity
                        (defaults to 1)
    Returns:
        int - quantity of item
        str - item sku code
    """
    # separate numbers and letters
    result = re.findall('\d+|\D+', deal_code)
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





def get_deal_info(deal, item):
    """
    Returns quantity and price of deal from description
    Args:
        deal (str): description of deal, eg. "2B for 45"
        item (str): sku code for item we are expecting deal for
    """
    deal_code_quantity, deal_price = deal.split(' for ')
    deal_quantity, deal_item = parse_deal_code(deal_code_quantity)
    if (
        not deal_price.isdigit() or
        None in (deal_quantity, deal_item) or
        item != deal_item
    ):
        # invalid format for deal
        return None, None

    return int(deal_quantity), int(deal_price)


def get_cost(prices, item, quantity):
    """
    Calculates cost of item based on quantity, including any deals
    Args:
        prices (dict): {item_code: {"price": price, "deals": deal}}
        item (str): item_code
        quantity (int): quantity of item in basket
    """
    item_price = prices[item]
    if item_price["deals"]:
        
        deal_quantity, deal_price = get_deal_info(item_price["deals"], item)
        if None in (deal_quantity, deal_price):
            # invalid deal format
            return None

        # apply deal as many times as possible
        num_deals, remainder = divmod(quantity, deal_quantity)
        cost = (num_deals * deal_price) + (remainder * item_price["price"])
    else:
        cost = quantity * item_price["price"]

    return cost


def calculate_saving(deal, item_prices):
    """
    Parse the deal string and calculate how much money is saved
    when this deal gets applied.
    """
    return 0


def get_ordered_deals(item_prices, item_deals):
    """
    Returns a list of deals in order of saving, so we can 
    apply best deals first.
    Args:
        item_prices (dict): {item: price}
        
    """
    deals_seen = set([])
    deal_savings = []
    for _, deal in item_deals.iteritems():
        if deal in deals_seen:
            continue

        saving = calculate_saving(deal, item_prices)
        deal_savings.append((deal, saving))

    # sort by saving
    ordered_deals = deal_savings.sort(key=operator.itemgetter(1))
    return ordered_deals


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
    if not skus:
        return 0

    total_cost = 0
    item_prices, item_deals = load_prices()
    items_counter = Counter(skus)
    
    ordered_deals = get_ordered_deals(item_prices, item_deals)
    
    for item, quantity in items.iteritems():
        if None in (item, quantity) or item not in prices:
            # invalid input
            return -1
        else:
            item_cost = get_cost(prices, item, quantity)
            if item_cost is None:
                # invalid input
                return -1
            else:
                total_cost += item_cost

    return total_cost

