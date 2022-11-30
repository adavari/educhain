# Handle unknown transactions in payment gateway
import logging

from utils.zarinpal import verify_new_transaction
from model.transaction_model import TransactionModel
from model.course_model import CourseModel

transactions = TransactionModel().get_unvalidated_transactions()

for transaction in transactions:
    logging.log(transaction['transaction_code'])
    response = verify_new_transaction(transaction['transaction_code'], transaction['price'])
    if not response:
        status = 2
    else:
        status = 1
        CourseModel().insert_user_course_sync(transaction['course_id'], transaction['user_id'])

    TransactionModel().update_transaction_status_sync(transaction['id'], status)


suc_transactions = TransactionModel().get_transactions_by_status_sync(1)
for t in suc_transactions:
    CourseModel().insert_user_course_sync(t['course_id'], t['user_id'])