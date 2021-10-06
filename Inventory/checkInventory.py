
K = 1

def totalFood(foodOrder):
    """Counts the number of each product in an order

    Args:
        foodOrder: list with all the burgers in the order

    Return:
        Dictionary with the number of each product
    """
    nVeggie = foodOrder.count('V')
    nBurgers = foodOrder.count(',') + 1 - nVeggie
    nLettuce = foodOrder.count('L')
    nTomato = foodOrder.count('T')
    nBacon = foodOrder.count('B')

    return {
        "nBurgers": nBurgers,
        "nLettuce": nLettuce,
        "nTomato": nTomato,
        "nVeggie": nVeggie,
        "nBacon": nBacon
     }


def proportion(amount, inventory, max):
    return (1-inventory/max)*amount


def calculate_penalization(order_food, stock, n_burguers, k = K):
    """Caclculates the penalization of an order

    Args:
        order_food: obtain the food in the order
        stock: of the products in the restuarant
        n_burguers: number of burgers in the restaurant
        K= 1

    Return:
        The penalization of the order
    """
    max_value = max(stock[7:11])
    p_burg = proportion(order_food["nBurgers"], stock[7], max_value)
    p_let = proportion(order_food["nLettuce"], stock[8], max_value)
    p_tom = proportion(order_food["nTomato"], stock[9], max_value)
    p_veg = proportion(order_food["nVeggie"], stock[10], max_value)
    p_bac = proportion(order_food["nBacon"], stock[11], max_value)

    return (p_burg + p_let + p_tom + p_veg + p_bac)/n_burguers * k


def checkInventory(order_food, stock):
    """Check availability of the products of an orther

    Args:
        order_food: Dictionary with the number of each product
        stock: Dictionary with the stock of each product

    Returns:
        If order can be cooked or not depending on the available products
    """

    if int(stock[7])-order_food["nBurgers"] < 0:
        return False
    elif int(stock[8])-order_food["nLettuce"] < 0:
        return False
    elif int(stock[9])-order_food["nTomato"] < 0:
        return False
    elif int(stock[10])-order_food["nVeggie"] < 0:
        return False
    elif int(stock[11])-order_food["nBacon"] < 0:
        return False
    else:
        return True

def updateInventory(order_food, stock):
    """Updates inventory by subtracting products from the order to be processed

    Args:
        order_food: Dictionary with the number of each product
        stock: Dictionary with the stock of each product

    Return:
        It only updates the dictionary of stock
    """
    stock[7]=int(stock[7])-order_food["nBurgers"]
    stock[8]=int(stock[8])-order_food["nLettuce"]
    stock[9]=int(stock[9])-order_food["nTomato"]
    stock[10]=int(stock[10])-order_food["nVeggie"]
    stock[11]=int(stock[11])-order_food["nBacon"]
