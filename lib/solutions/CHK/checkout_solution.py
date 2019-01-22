from collections import Counter
import csv
import operator
import re


def load_prices():
    """
    Loads data from storage (prices.csv)
    Returns:
        item_prices (dict): price information for each item - {item: price}
        item_deals (set): all unique deals in the dataset
    """
    item_prices = {}
    item_deals = set([])
    with open('prices.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for (item, price, deals) in csv_reader:
            item_prices[item] = int(price)
            for deal in deals.split(', '):
                if deal:
                    item_deals.add(deal)

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
    Calculates cost of item based on quantity
    Args:
        prices (dict): {item_code: price}
        item (str): item_code
        quantity (int): quantity of item in basket
    """
    return quantity * prices[item]


def calculate_saving(deal, item_prices):
    """
    Parse the deal string and calculate how much money is saved
    when this deal gets applied. Also returns deal requirement.
    Args:
        deal (str): deal information
        item_prices (dict): {item: price}
    Returns:
        requirements (list(str)): shows what is needed to complete deal, eg. [2E, B]
        saving (int): total saving this deal gives
        cost (int): cost of deal
    """
    free_re = re.search(r'(\w+) get one ([^\n]+) free', deal)
    if free_re:
        # saving is value of free item
        saving = item_prices[free_re.group(2)]
        requirements = list(free_re.groups())
        quantity, item = parse_deal_code(free_re.group(1))
        cost = get_cost(item_prices, item, quantity)
    else:
        # assuming for now that all other deals are just x-for
        # saving is difference between deal price and quantity * base price
        [(deal_code_quantity, deal_price)] = re.findall(r'(\w+) for (\w+)', deal)
        deal_quantity, deal_item = parse_deal_code(deal_code_quantity)
        saving = (deal_quantity * item_prices[deal_item]) - int(deal_price)
        requirements = [deal_code_quantity]
        cost = int(deal_price)

    return requirements, saving, cost


def get_ordered_deals(item_prices, item_deals):
    """
    Returns a list of deals in order of saving, so we can 
    apply best deals first.
    Args:
        item_prices (dict): {item: price}
        item_deals (set): set([deal1, deal2, etc.])
    Returns:
        ordered_deals (list(tuple)): 
            [(deal_x, saving_x), (deal_y, saving_y), ..]
    """
    deal_savings = []
    for deal in item_deals:
        requirements, saving, cost = calculate_saving(deal, item_prices)
        deal_savings.append((deal, requirements, saving, cost))

    # sort by saving in descending order
    deal_savings.sort(key=operator.itemgetter(2), reverse=True)
    return deal_savings


def requirements_satisfied(items_counter, requirements):
    """
    Checks if items in requirements are present in basket (items_counter)
    Args:
        items_counter (collections.Counter): items in basket
            with number of occurrences
        requirements (list): list of requirements for this deal eg. ['2E', 'B']
    Returns:
        nullable(collections.Counter): Counter showing how many of each item
        this deal uses. Returns None if the deal requirements are not met.
    """
    c = Counter()
    for r in requirements:
        quantity, item = parse_deal_code(r)
        if (
            None in (quantity, item)
            or item not in items_counter
            or items_counter[item] < quantity
        ):
            # requirements for this deal not satisfied
            return None
            
        # if item is already in c then this will sum the values
        c.update({item: quantity})

    # if all requirements satisfied then return True
    return c


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
    print "skus", skus

    total_cost = 0
    item_prices, item_deals = load_prices()
    items_counter = Counter(skus)

    ordered_deals = get_ordered_deals(item_prices, item_deals)
    print "ordered_deals", ordered_deals

    for (deal, requirements, saving, deal_cost) in ordered_deals:
        print "deal: ", deal
        print "requirements", requirements
        print "items_counter", items_counter
        reqs_counter = requirements_satisfied(items_counter, requirements)
        print "reqs_counter", reqs_counter
        # sanity check to avoid infinite loop. Assuming someone can't
        # apply a deal more than ctr times
        ctr = 10
        # loop in order to apply deal as many times as is valid
        while reqs_counter is not None and ctr > 0:
            ctr -= 1
            total_cost += deal_cost
            # subtract items from basket
            items_counter -= reqs_counter
            reqs_counter = requirements_satisfied(items_counter, requirements)

    # for any remaining items, just add cost
    for item, quantity in items_counter.iteritems():
        if None in (item, quantity) or item not in item_prices:
            # invalid input
            return -1
        else:
            item_cost = get_cost(item_prices, item, quantity)
            if item_cost is None:
                # invalid input
                return -1
            else:
                total_cost += item_cost

    return total_cost









