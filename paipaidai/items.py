# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PaipaidaiItemList(scrapy.Item):
    itemid = scrapy.Field()


class PaipaidaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    userName = scrapy.Field()
    userRate = scrapy.Field()
    amount =scrapy.Field()
    year_rate =scrapy.Field()
    timeLimit =scrapy.Field()
    progressBar =scrapy.Field()
    bidders = scrapy.Field()
    end_time = scrapy.Field()
    #borrow_balance =scrapy.Field()
    male =scrapy.Field()
    age =scrapy.Field()
    registerTime =scrapy.Field()
    degree_education =scrapy.Field()
    college =scrapy.Field()
    learn_form =scrapy.Field()
    authentication_information =scrapy.Field()
    succeed_borrow =scrapy.Field()
    first_borrow_time =scrapy.Field()
    borrow_history =scrapy.Field()
    succeed_repay =scrapy.Field()
    normal_repay =scrapy.Field()
    overtime_less_15 =scrapy.Field()
    overtime_more_15 =scrapy.Field()
    #future_six_month_repay =scrapy.Field()
    #last_six_month_delay =scrapy.Field()
    cumulative_amount_of_borrowing =scrapy.Field()
    to_be_repay =scrapy.Field()
    to_be_gather =scrapy.Field()
    max_borrow_amount =scrapy.Field()
    max_liabilities =scrapy.Field()
    #times =scrapy.Field()
    avg_rate = scrapy.Field()
    avg_data = scrapy.Field()
    avg_amount=scrapy.Field()
    sum_of_to_pay =scrapy.Field()
    max_overtime = scrapy.Field()
    last_fuzhai = scrapy.Field()
    update_time =scrapy.Field()
    state = scrapy.Field()
    id = scrapy.Field()
    userId = scrapy.Field()








