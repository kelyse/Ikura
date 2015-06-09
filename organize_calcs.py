from model import connect_to_db, db, User, Card, Value
from pandas import Series, DataFrame
import pandas as pd
from datetime import datetime
# import json

# Keeping this here for now so I can play with file to make sure organizaiton works.
# Will eventually send this stuff to server.py so that this stuff shows on dashboard.html
# from server import app
# connect_to_db(app)


#  This should be a dict with key of card name, each value is a dictionary key value pair of min and sugg
def to_be_sorted_by_date(i):
    return i[2]

def organization(user_card_dict_py):
    """This is rearranging my data to display on html page and for D3"""

    values = user_card_dict_py.values()

    min_debt_list = []
    min_int_list = []
    min_payment_list = []

    sugg_debt_list = []
    sugg_int_list = []
    sugg_payment_list = []


    for i in range(len(values[0])):
        card = values[0][i]
        dict_of_payments_per_card = card.values()[0]
        sugg_payment_info = dict_of_payments_per_card["Suggested"]
        min_payment_info = dict_of_payments_per_card["Minimum"]

    # *************************************
        # Minimum Payment Data #
    # *************************************

        min_debt = min_payment_info[0]
        min_debt_list.append(min_debt)


        min_int = min_payment_info[1]
        min_int_list.append(min_int)


        min_payment = min_payment_info[2]
        min_payment_list.append(min_payment)

    # *************************************
        # Suggested Payment Data # 
    # *************************************

        sugg_debt = sugg_payment_info[0]
        sugg_debt_list.append(sugg_debt)

        sugg_int = sugg_payment_info[1]
        sugg_int_list.append(sugg_int)

        sugg_payment = sugg_payment_info[2]
        sugg_payment_list.append(sugg_payment)



    total_min_debt = zip(*min_debt_list)
    total_min_int = zip(*min_int_list)
    total_min_payment = zip(*min_payment_list)

    total_sugg_debt = zip(*sugg_debt_list)
    total_sugg_int = zip(*sugg_int_list)
    total_sugg_payment = zip(*sugg_payment_list)

    # Maybe making the choice here NOT to round out numbers. Will round in Jinja on HTML.

    now = datetime.now()
    dt_min_month = pd.date_range(datetime.strftime(now, '%Y-%m-%d'), periods=(len(total_min_debt)-1), freq='M') 
    dt_sugg_month = pd.date_range(datetime.strftime(now, '%Y-%m-%d'), periods=(len(total_sugg_debt)-1), freq='M')


    total_calc_min_debt = [] 
    for i in total_min_debt:
        sum_of = 0
        for x in i:
            sum_of = sum_of + x
        total_calc_min_debt.append(sum_of)


    total_calc_min_int = []
    for i in total_min_int:
        sum_of = 0
        for x in i:
            sum_of = sum_of + x
        total_calc_min_int.append(sum_of)

    total_calc_min_payment = []
    for i in total_min_payment:
        sum_of = 0
        for x in i:
            sum_of = sum_of + x
        total_calc_min_payment.append(sum_of)


    total_calc_sugg_debt = []
    for i in total_sugg_debt:
        sum_of = 0
        for x in i:
            sum_of = sum_of + x
        total_calc_sugg_debt.append(sum_of)


    total_calc_sugg_int = []
    for i in total_sugg_int:
        sum_of = 0
        for x in i:
            sum_of = sum_of + x
        total_calc_sugg_int.append(sum_of)


    total_calc_sugg_payment = []
    for i in total_sugg_payment:
        sum_of = 0
        for x in i:
            sum_of = sum_of + x
        total_calc_sugg_payment.append(sum_of)


    total_min = zip(*[total_calc_min_debt, total_calc_min_int, total_calc_min_payment])
    total_sugg = zip(*[total_calc_sugg_debt, total_calc_sugg_int, total_calc_sugg_payment])

    # I don't think I need to have the same values for both min and sugg so we shall see...
    #   print "M:", len(total_min)
    #   print "S:", len(total_sugg)
    # I think I do...


    while len(total_sugg_debt) < len(total_min_debt):
        total_sugg_debt.append((0, 0, 0))


    total_calc_sugg_debt = []
    for i in total_sugg_debt:
        sum_of = 0
        for x in i:
            sum_of = sum_of + x
        total_calc_sugg_debt.append(sum_of)


    all_totals = [total_min, total_sugg]

    # I think these are right......
    df_min = pd.DataFrame(data = total_min, index=dt_min_month, columns=['Debt', 'Interest', 'Payments'])
    # print "This is my Min panda", df_min
    df_sugg = pd.DataFrame(data = total_sugg, index=dt_sugg_month, columns=['Debt', 'Interest', 'Payments'])



    #   #**************# A debugger tool from Rachael: #**************#
    #   # import pdb; pdb.set_trace()




    # #********** This is the list of my data points (date: ##, Min: ##, Sugg: ##) that will be JSONified and passed to D3 **********#
    new_data_points = zip(*[dt_min_month.date, total_calc_min_debt, total_calc_sugg_debt])

    new_data_point_list = []
    for i in range(len(new_data_points)):
        point_dict = {"date":str(new_data_points[i][0]), "Minimum":new_data_points[i][1], "Suggested": new_data_points[i][2]}
        new_data_point_list.append(point_dict)


    df_total = [df_min, df_sugg, new_data_point_list]


    return df_total


def organization_int(user_dict_int):
    """organizing this dict into correct format to display on webpage"""

    card_names = user_dict_int[0].keys()
    print "am i here?", card_names

    now = datetime.now()
    point_lists = user_dict_int[1]
    point_list = []

    points = len(point_lists[0])
    dt = pd.date_range(datetime.strftime(now, '%Y-%m-%d'), periods=points, freq='M')
    print "date not time?", dt

    card_counter = 0
    all_cards_points = []
    for card in point_lists:
        card_points = []
        # print '*' * 10
        # print "this is my card", card
        counter = 0
        
        for point in card:
                point = list(point)
                date = dt[counter]
                counter += 1 
                point.append(date)
                name = str(card_names[card_counter])
                point.append(name)
                card_points.append(point)
        card_counter = card_counter + 1
      

        all_cards_points.append(card_points)


    print "This is all_cards_points", all_cards_points

    #give me a list of all my points per card
    # print "all_cards_points - index 0", all_cards_points[0]
    # print len(all_cards_points[0])

    # df_all = []
    # for item in all_cards_points:
    #     df_item = pd.DataFrame(data = item, columns=['Debt', 'Payments', 'Month'])
    #     df_all.append(df_item)

    # # print "is this all"
    

    all_together_cards_points = []
    for card in all_cards_points:
        for point in card:
            all_together_cards_points.append(point)

    sorted_points =sorted(all_together_cards_points, key=to_be_sorted_by_date)

  
    return sorted_points


# TODO:
# create points for use in multiple d3 graphs? use toggle feature?: 
#   (debt_decr, time)
#   (intr_decr, time)
#   (payment_decr, time)        
# TODOD:
#  Dates get messed up in graph if they are not the same length


