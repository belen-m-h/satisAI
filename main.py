import datetime

import Inventory.checkInventory as inv
import processData.processData as processData
import Cooking.Cooking as cook

if __name__ == '__main__':

    # PROCESSING THE DATA
    # We process the restaurant information
    restaurant = processData.processBranch()
    # We process into a dataframe the orders of the restaurant
    orders = processData.processOrders()
    # We define the places for cook, assembly and package
    cookingPlaces, assemblyPlaces, packagePlaces = processData.definePlaces(restaurant)
    # We define a list to place the orders we do not know how to process
    waiting_orders_till_kitchen_available = []

    # PROCESSING THE ORDERS
    i = 0
    while i < len(orders):
        # Time in which the order is received
        orderDate = datetime.datetime.strptime(orders['Time'][i], '%Y-%m-%d %H:%M:%S')

        # We take the minimum time we can cook a burger
        min_cooking=min(cookingPlaces.values())
        # if not pending orders and can take the next order we take it if it can be processed in les than 20 mins
        order_food = inv.totalFood(orders['Food'][i])
        burgers = processData.defineBurguers(order_food["nBurgers"] + order_food["nVeggie"])
        # If the kitchen is free we start processign the order
        if (min_cooking < orderDate):
            # if there are no orders in the queue (
            # and we simply receive one order when our kitchen is free) we process it
            if waiting_orders_till_kitchen_available == []:
                onTime, [cookingPlaces_tmp, assemblyPlaces_tmp, packagePlaces_tmp], burgersdict_tmp, max_t_tmp = cook.checkInventoryAndCooking(order_food, restaurant.copy(), orders['Time'][i], cookingPlaces.copy(), assemblyPlaces.copy(),
                                         packagePlaces.copy(), burgers.copy())

                # if we can cook in in less than 20 mins then we take it and update the slots time + the restaurant stock
                if onTime:
                    cookingPlaces, assemblyPlaces, packagePlaces, burgersdict = (
                        cookingPlaces_tmp, assemblyPlaces_tmp, packagePlaces_tmp, burgersdict_tmp)
                    inv.updateInventory(order_food, restaurant)

                    print(orders["RestaurantID"][i]+","+orders["OrderID"][i]+",ACCEPTED "+str(max_t_tmp))
                else:
                    print(orders["RestaurantID"][i]+","+orders["OrderID"][i]+",REJECTED")


            # if there are pending orders in the queue to be accepted or rejected
            # we analise from all the orders in the queue which ones we prefer to take:
            # in accordance to our optimization function
            else:
                import copy
                # We count all the pending orders we have
                total_orders_queue = len(waiting_orders_till_kitchen_available)
                # We find the best combination of the orders to be processed.
                best_order, cookingPlaces_tmp, assemblyPlaces_tmp, packagePlaces_tmp, best_max_tmp, best_order_combination, restaurant_tmp = \
                    cook.findBestCombination(copy.deepcopy(waiting_orders_till_kitchen_available), restaurant.copy(), orders.copy(), cookingPlaces.copy(), assemblyPlaces.copy(), packagePlaces.copy())

                min_ord=list(waiting_orders_till_kitchen_available[0].keys())[0]
                
                for j in range(total_orders_queue):
                    if j in best_order_combination:
                        print(orders["RestaurantID"][min_ord+j] + "," + orders["OrderID"][min_ord+j] + ",ACCEPTED " + str(best_max_tmp[j+min_ord]))
                    else:
                        print(orders["RestaurantID"][min_ord+j] + "," + orders["OrderID"][min_ord+j] + ",REJECTED")

                # If we took at least one order we update the slots times + the restaurant stock
                if len(best_order_combination)>0:
                    cookingPlaces, assemblyPlaces, packagePlaces = (
                        cookingPlaces_tmp, assemblyPlaces_tmp, packagePlaces_tmp)
                    restaurant = copy.deepcopy(restaurant_tmp)

                # we reset the queue
                waiting_orders_till_kitchen_available = []
                i-=1
        # If the kitchen is not free we wait until it is free and save the order in the queue to decide later
        # (when the kitchen is free with orders we want to accept/cancel)
        else:
            waiting_orders_till_kitchen_available.append({i:burgers})
        i+=1
    t_max = max(packagePlaces,key=packagePlaces.get)
    total_t =cook.getDifference(datetime.datetime.strptime(orders['Time'][0], '%Y-%m-%d %H:%M:%S'),packagePlaces[t_max] )
    print(restaurant[0]+',TOTAL,'+str(total_t))
    print(str(restaurant[0])+',Inventory,'+str(restaurant[7])+','+str(restaurant[8])+','+str(restaurant[9])+
          ','+str(restaurant[10])+','+str(restaurant[11]))

