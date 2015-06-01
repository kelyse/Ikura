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

def organization(user_card_dict_py):
	"""This is rearranging my data to display on html page and for D3"""


	# print "What is this user_card_dict_py?", user_card_dict_py
	values = user_card_dict_py.values()
	# print "All of values", type(values)
	# print "First index within values", type(values[0])
	# print "First index within idex within values", type(values[0][0])
	# print "What is this? The first card dict?", values[0][0]

	min_debt_list = []
	min_int_list = []
	min_payment_list = []

	sugg_debt_list = []
	sugg_int_list = []
	sugg_payment_list = []

	# print "What is", values[0]

	for i in range(len(values[0])):
		print "*" * 100
		card = values[0][i]
		# print  "Here is a card!", card
		dict_of_payments_per_card = card.values()[0]
		sugg_payment_info = dict_of_payments_per_card["Suggested"]
		min_payment_info = dict_of_payments_per_card["Minimum"]
		# print "This is min payment info", min_payment_info

	# *************************************
		# Minimum Payment Data #
	# *************************************

		min_debt = min_payment_info[0]
		# print "This is minimum debt on my card as it decreases:", min_debt
		min_debt_list.append(min_debt)


		min_int = min_payment_info[1]
		# print "This is the minimum interest accruing for each payment:", min_int
		min_int_list.append(min_int)


		min_payment = min_payment_info[2]
		# print "This is the minimum payments for card until debt is gone:", min_payment
		min_payment_list.append(min_payment)

	# *************************************
		# Suggested Payment Data # 
	# *************************************

		sugg_debt = sugg_payment_info[0]
		# print "This is suggested debt on my card as it decreases:", sugg_debt
		sugg_debt_list.append(sugg_debt)

		sugg_int = sugg_payment_info[1]
		# print "This is the suggested interest accruing for each payment:", sugg_int
		sugg_int_list.append(sugg_int)

		sugg_payment = sugg_payment_info[2]
		# print "This is the suggested payments for card until debt is gone:", sugg_payment
		sugg_payment_list.append(sugg_payment)



	total_min_debt = zip(*min_debt_list)
	# print "This is my min debt zipped list", total_min_debt
	total_min_int = zip(*min_int_list)
	# print "This is my min int zipped list", total_min_int
	total_min_payment = zip(*min_payment_list)
	# print "This is my min payment zipped list", total_min_payment

	total_sugg_debt = zip(*sugg_debt_list)
	# print "This is my sugg debt zipped list", total_sugg_debt
	total_sugg_int = zip(*sugg_int_list)
	# print "This is my sugg int zipped list", total_sugg_int
	total_sugg_payment = zip(*sugg_payment_list)
	# print "This is my sugg payment zipped list", total_sugg_payment

# Maybe making the choice here NOT to round out numbers. Will round in Jinja on HTML.

	now = datetime.now()
	dt_min_month = pd.date_range(datetime.strftime(now, '%Y-%m-%d'), periods=len(total_min_debt), freq='M')	
	dt_sugg_month = pd.date_range(datetime.strftime(now, '%Y-%m-%d'), periods=len(total_sugg_debt), freq='M')


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

	# print "total_calc_sugg_payment", total_calc_sugg_payment

	total_min = zip(*[dt_min_month, total_calc_min_debt, total_calc_min_int, total_calc_min_payment])
	total_sugg = zip(*[dt_sugg_month, total_calc_sugg_debt, total_calc_sugg_int, total_calc_sugg_payment])
	# print "This is total sugg - (date, debt, int, payment )", total_sugg

#I don't think I need to have the same values for both min and sugg so we shall see...
	# print "M:", len(total_min)
	# print "S:", len(total_sugg)
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
	df_min = pd.DataFrame(data = total_min, columns=['Month', 'Debt', 'Interest', 'Payments'])
	# print "This is my Min panda", df_min
	df_sugg = pd.DataFrame(data = total_sugg, columns=['Month', 'Debt', 'Interest', 'Payments'])



# 	#**************# A debugger tool from Rachael: #**************#
# 	# import pdb; pdb.set_trace()




# #********** This is the list of my data points (date: ##, Min: ##, Sugg: ##) that will be JSONified and passed to D3 **********#
	new_data_points = zip(*[dt_min_month.date, total_calc_min_debt, total_calc_sugg_debt])

	new_data_point_list = []
	for i in range(len(new_data_points)):
		point_dict = {"date":str(new_data_points[i][0]), "Minimum":new_data_points[i][1], "Suggested": new_data_points[i][2]}
		new_data_point_list.append(point_dict)


	df_total = [df_min, df_sugg, new_data_point_list]


	return df_total



# TODO:
# create points for use in multiple d3 graphs? use toggle feature?: 
# 	(debt_decr, time)
# 	(intr_decr, time)
# 	(payment_decr, time)		
# TODOD:
#  Dates get messed up in graph if they are not the same length


