import pandas as pd
import csv
import datetime

INITIAL_TIME = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)


def processBranch(file="data/branch.csv"):
    """Process branch capacity of cooking and inventory

    Args:
        file= branch information

    Prints:
        Process the branch data and return a dictionary with the info
    """
    array = []

    with open(file) as csvfile:
        csvReader = csv.reader(csvfile)
        for row in csvReader:
            for i in range(12):
                array.append(row[i])

    return array


def processOrders(file="data/orders.csv"):
    """Process orders into a dataframe

    Args:
        file= orders information

    Prints:
        Process the branch data and show it
    """
    colnames = ['RestaurantID', 'Time', 'OrderID', 'Food']
    orders_data = pd.read_csv(file, delimiter=';')
    df_orders = pd.DataFrame(orders_data).sort_values(by=['Time'], ascending=True).reset_index()
    return df_orders


def definePlaces(array):
    """We define the places we have in the restaurant to cook, assembly or package the burgers

    Args:
        file= dictionary of the restaurant

    Prints:
        Returns 3 dictionaries with the available places defined for each task,
        with the available time equal to INITIAL_TIME
    """
    cookDict = dict()
    assemblyDict = dict()
    packageDict = dict()
    for i in range(int(array[1][0:1])):
        cookDict[i] = INITIAL_TIME
    for i in range(int(array[3][0:1])):
        assemblyDict[i] = INITIAL_TIME
    for i in range(int(array[5][0:1])):
        packageDict[i] = INITIAL_TIME

    return cookDict, assemblyDict, packageDict


def defineBurguers(burgernumber):
    """We define the a dictionary with all the burgers of the order

    Args:
        file= dictionary for the burgers

    Prints:
        Returns a dictionaries with the available places defined for each task,
        with the available time equal to INITIAL_TIME
    """
    burgers = dict()
    for i in range(burgernumber):
        #todo remove order_time or remove datetime as argument
        burgers[i] = {"order_time": None, "step_finish_time": None, "step": None}
    # print(burgers)
    return burgers