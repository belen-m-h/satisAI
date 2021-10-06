import datetime
from datetime import timedelta
from itertools import compress, product
import Inventory.checkInventory as inv
import Cooking.Cooking as cook
import copy


def getDifference(then, now):
    """Obtains the difference between to dates

    Args:
        then: higher date
        now: lower date

    Returns:
        the difference in minutes
    """
    duration = now - then
    duration_in_s = duration.total_seconds()
    minute_ct = 60

    def mins():
        return divmod(duration_in_s, minute_ct)[0]
    return int(mins())


def updateTimes(burgersdict, orderDateTime, slots, slotTime, step):
    """

    Args:
        burgersdict: dictionary with the current state of the burgers on order
        slots: dictionary of the step(cook, assembly or packaging)
        slotTime: time to process each burger in each place
        step: COOK, ASSEMBLY or PACKAGE

    Returns:
         The dictionary of the burgers with the time in which they would finish
         the cooking process, and the dictionaries of the cooking step, with the time until
        the sites of each phase are occupied, when an order is processed.
    """
    numberOfBurgers = len(burgersdict.keys())
    orderDate = datetime.datetime.strptime(orderDateTime, '%Y-%m-%d %H:%M:%S')
    # print(burgersdict)
    for j in range(numberOfBurgers):
        # Take the slot with the minimum time to be free
        vmin = min(slots, key=slots.get)
        # If the burguer has not been procesed yet (burgersdict[j]["step_finish_time"] is None) take the min start tiem as the order time
        # otherwise take the minimum time to be processed as the time at which the previous step finished burgersdict[j]["step_finish_time"]
        start_time = orderDate
        if burgersdict[j]["step_finish_time"] is not None:
            start_time = burgersdict[j]["step_finish_time"]

        # take the time at which the burguer can be processed in this step (when the previous step is finished and when the slot is free)
        time = max(slots[vmin], start_time)

        #Update both burguer and slot times
        slots[vmin] = time + timedelta(minutes=int(slotTime))
        burgersdict[j]["step_finish_time"] = slots[vmin]
        burgersdict[j]["step"] = step

    return slots, burgersdict


def checkCookingAvailability(orderDateTime, cookingPlaces, assemblyPlaces, packagingPlaces, cookingTime, assemblyTime, packagingTime, burgersdict):
    """Check availability of places to  of an order

    Args:
        cookingPlaces:
        assemblyPlaces:
        packagingPlaces:
        cookingTime:
        assemblyTime:
        packagingTime:
        burgersdict:

    Retrun:
        If order can be cooked or not depending on the available products
    """


    cookingPlaces, burgersdict = updateTimes(burgersdict, orderDateTime, cookingPlaces, cookingTime, "COOKING")
    assemblyPlaces, burgersdict = updateTimes(burgersdict, orderDateTime, assemblyPlaces, assemblyTime, "ASSEMBLING")
    packagingPlaces, burgersdict = updateTimes(burgersdict, orderDateTime, packagingPlaces, packagingTime, "PACKAGING")

    numberOfBurgers = len(burgersdict.keys())
    orderDate = datetime.datetime.strptime(orderDateTime, '%Y-%m-%d %H:%M:%S')

    max_t = 0
    # todo check if we can obtain the max   min(slots, key=slots.get)
    for i in range(numberOfBurgers):
        diff = getDifference(orderDate, burgersdict[i]["step_finish_time"])
        max_t = max(max_t, diff)

    if max_t < 20:
        return True, [cookingPlaces,assemblyPlaces,packagingPlaces], burgersdict, max_t
    else:
        return False, [None,None,None], None, None


def combinations(items):
    """Insert in a list the possible combinations of orders

    Args:
        items: list of orders

    Return:
        List of possible combinations.
    """

    return (set(compress(items, mask)) for mask in product(*[[0, 1]] * len(items)))


def checkInventoryAndCooking(order_food, restaurant, orderDate, cookingPlaces, assemblyPlaces, packagePlaces, burgers):
    """Check availability of places to  of an order and inventory

    Retrun:
        True with the actual status of kitchen, and status of burgers
    """
    if inv.checkInventory(order_food, restaurant):
        onTime, [cookingPlaces_tmp, assemblyPlaces_tmp, packagingPlaces_tmp], burgersdict_tmp, max_t_tmp = \
            cook.checkCookingAvailability(
                orderDate, cookingPlaces, assemblyPlaces, packagePlaces,
                restaurant[2], restaurant[4], restaurant[6], burgers
            )

        return onTime, [cookingPlaces_tmp, assemblyPlaces_tmp, packagingPlaces_tmp], burgersdict_tmp, max_t_tmp
    else:
        return False, [None, None, None], None, None


def checkInventoryAndCookingBatches(batch_of_orders, restaurant, orders, cookingPlaces, assemblyPlaces, packagePlaces):

    cookingPlaces_window, assemblyPlaces_window, packagePlaces_window = cookingPlaces, assemblyPlaces, packagePlaces
    onTimeDict={}

    total_burguers=0
    penalization=0
    orders_finish_time = {}
    restaurant_tmp = copy.deepcopy(restaurant)

    # For every order in waiting_orders_till_kitchen_available
    # (which contains a subset of the orders in queue) we analise if we have inventOry for all of them
    # and if we can process all of them on time
    for j in batch_of_orders:
        order_id = int(list(j.keys())[0])
        burguers_v = list(j.values())[0]
        n_burguers = len(burguers_v.keys())
        order_food = inv.totalFood(orders['Food'][order_id])
        if inv.checkInventory(order_food, restaurant_tmp):
            onTime, [cookingPlaces_tmp, assemblyPlaces_tmp,packagingPlaces_tmp], burgersdict, max_t_tmp = \
                cook.checkCookingAvailability(
                    orders['Time'][order_id],cookingPlaces_window.copy(),
                    assemblyPlaces_window.copy(), packagePlaces_window.copy(),
                    restaurant_tmp[2], restaurant_tmp[4],restaurant_tmp[6], burguers_v
                )

            onTimeDict[order_id] = {"onTime": onTime, "burgers":burgersdict, "nBurguers":n_burguers}
            orders_finish_time[order_id] = max_t_tmp
            # For every single order in the set of orders if we have inventory and can do it on time we
            # update temporarily slots status or the next order in the iteration or return what woudl be
            # the configuration if we take that full order
            if onTime:
                cookingPlaces_window, assemblyPlaces_window, packagePlaces_window= cookingPlaces_tmp, assemblyPlaces_tmp, packagingPlaces_tmp
                penalization += inv.calculate_penalization(order_food, restaurant_tmp, n_burguers)
                inv.updateInventory(order_food, restaurant_tmp)
                total_burguers += n_burguers
            # If we run out of time we can not process this combination of orders
            else:
                return None, [None, None, None], None, None, None, None
        # If we run out of inventory we can not process this combination of orders
        else:
            return None, [None, None, None], None, None, None, None

    return onTimeDict, [cookingPlaces_window, assemblyPlaces_window, packagePlaces_window], restaurant_tmp, total_burguers, penalization, orders_finish_time


def findBestCombination(waiting_orders_till_kitchen_available, restaurant, orders, cookingPlaces, assemblyPlaces, packagePlaces):

    n_orders = len(waiting_orders_till_kitchen_available)
    # We create a list with all the possible combinations of the pending orders
    all_order_combinations = list(combinations(range(n_orders)))

    # Params of the best order combination found
    best_score = 0
    best_order = 0
    best_cookingPlaces = None
    best_assemblyPlaces = None
    best_packagePlaces = None
    best_orders_finish_time = None
    best_comb = None
    restaurant_best = None
    # For every order combination we check if we have inventory for it + if we can serve all in less than 20 minutes and we take the best one
    # in accordance to our optimization function
    for order_combination in all_order_combinations:
        order_subset = []
        order_combination = list(order_combination)
        for order in order_combination:
            order_subset.append(copy.deepcopy(waiting_orders_till_kitchen_available[order]))

        onTimeDict, [cookingPlaces_tmp, assemblyPlaces_tmp, packagePlaces_tmp], restaurant_tmp, total_burguers, penalization, orders_finish_time = \
            checkInventoryAndCookingBatches(order_subset.copy(), restaurant.copy(), orders.copy(), cookingPlaces.copy(),assemblyPlaces.copy(), packagePlaces.copy())

        # If the score of the combination is better than the current best option we override it
        if onTimeDict:
            total_score = total_burguers-penalization
            if best_score<total_score:
                best_score=total_score
                best_order=order_subset
                best_orders_finish_time = orders_finish_time
                best_comb= order_combination
                best_cookingPlaces = cookingPlaces_tmp
                best_assemblyPlaces = assemblyPlaces_tmp
                best_packagePlaces = packagePlaces_tmp
                restaurant_best = restaurant_tmp

    # MTODO MAKE TEST THAT CHECK THE INVENTARY AND ONE CASE SCENARIO
    return best_order, best_cookingPlaces, best_assemblyPlaces,best_packagePlaces, best_orders_finish_time, best_comb, restaurant_best

