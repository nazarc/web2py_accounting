from gluon import (TABLE, TR, THEAD, TD, B)
import logging
logger = logging.getLogger("web2py.app.accounting")
logger.setLevel(logging.DEBUG)


class Accounting:
    def __init__(self):
        pass


class Account(Accounting):

    def __init__(self, account_id=None, account_name=None, category_id=None,
                 category=None, creation_date=None, amount=None,
                 total_balance=None, comment=None):

        self._account_id = account_id
        self._account_name = account_name
        self._category_id = category_id
        self._category = category
        self._creation_date = creation_date
        self._amount = amount
        self._amounts = None
        self._total_balance = total_balance
        self._balance_per_category = []
        self._comment = comment
        self._accounts_data = list()
        self._categories = Category()
        self._incoming_data = None
        self._outgoing_data = None

    @property
    def incoming_data(self):
        return self._incoming_data

    @incoming_data.setter
    def incoming_data(self, incoming_data):
        self._incoming_data = incoming_data

    @property
    def outgoing_data(self):
        return self._outgoing_data

    @outgoing_data.setter
    def outgoing_data(self, outgoing_data):
        self._outgoing_data = outgoing_data

    @property
    def balance_per_category(self):
        return self._balance_per_category

    @balance_per_category.setter
    def balance_per_category(self, balance_per_category):
        self._balance_per_category = balance_per_category

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        if not account_id:
            raise Exception('Error! account_id ')
        self._account_id = account_id

    @property
    def account_name(self):
        return self._account_name

    @account_name.setter
    def account_name(self, account_name):
        if not account_name:
            raise Exception('Error! account_name ')
        self._account_name = account_name

    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        if not category_id:
            raise Exception('Error! category_id')
        self._category_id = category_id

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if not category:
            raise Exception('Error! category')
        self._category = category

    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        if not creation_date:
            raise Exception('Error! creation_date')
        self._creation_date = creation_date

    @property
    def amount(self):
        return float('%.2f' % self._amount)

    @amount.setter
    def amount(self, amount):
        if not amount:
            raise Exception('Error! amount')
        self._amount = amount

    @property
    def amounts(self):
        return self._amounts

    @amounts.setter
    def amounts(self, amounts):
        if not amounts:
            raise Exception('Error! amounts')
        self._amounts = amounts

    @property
    def total_balance(self):
        return float('%.2f' % self._total_balance)

    @total_balance.setter
    def total_balance(self, total_balance):
        if not total_balance:
            raise Exception('Error! total_amount', total_balance)
        self._total_balance = total_balance

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = comment

    @property
    def accounts_data(self):
        return self._accounts_data

    @accounts_data.setter
    def accounts_data(self, accounts_data):
        if isinstance(accounts_data, list):
            logger.debug('Setting {} account data {}'
                         .format(self.__class__.__name__, accounts_data))
            self._accounts_data = accounts_data
        else:
            raise Exception(
                'Error {} account data'.format(self.__class__.__name__))

    @staticmethod
    def extract_amounts(values, key):
        return [value[key] for value in values]

    def sum_up_amounts(self):
        totalized_amount = 0.0
        for amount in self.amounts:
            totalized_amount += amount
        return float('%.2f' % totalized_amount)

    def _sum_up_catergory_amount(self):
        for account_data in self.accounts_data:
            for category_amount in self._categories.categories_lst:
                if account_data['category'] == category_amount['category']:
                    category_amount['amount'] += account_data['amount']
        logger.debug('[sum_up_catergory_amount]: {}'.format(category_amount))

    def _update_category_amount(self):
        for category in self._categories.categories_lst:
            category_amount = dict.fromkeys([category['category']],
                                             category['amount'])
            self._categories.amount_per_category.update(category_amount)

    def get_account_amounts(self, acc_type, values):
        self.amounts = self.extract_amounts(values=values, key='amount')
        total_amounts = self.sum_up_amounts()
        logger.debug('balance > total {} amount: {}'.
                     format(acc_type, total_amounts))
        return dict(acc_type=acc_type, total_amounts=total_amounts)

    def get_amount_sum_per_category(self):
        self.determine_categories_of_account_data()

        for category in self._categories.category_set:
            self._categories.categories_lst.append(dict(category=category,
                                                        amount=0.0))
        logger.debug('Created Category / Amount list: {}'.format(
            self._categories.categories_lst))

        self._sum_up_catergory_amount()
        logger.debug('Sum upped amount per category: {}'.format(
                     self._categories.categories_lst))

        self._update_category_amount()
        logger.debug('Created amount per category {}'
                     .format(self._categories.amount_per_category))

        return self._categories.amount_per_category

    def determine_categories_of_account_data(self):
        for category in self.accounts_data:
            self._categories.category_set.add(category['category'])
        logger.debug('Determined categories of account data: {}'
                     .format(self._categories.category_set))


class Category:
    def __init__(self):
        self._categories_lst = list()
        self._amount_per_category = dict()
        self._category_set = set()

    @property
    def categories_lst(self):
        return self._categories_lst

    @categories_lst.setter
    def categories_lst(self, categories_lst):
        if isinstance(categories_lst, list) or not categories_lst:
            raise Exception('Class: {} Error Categories List '
                            .format(self.__class__.__name__))
        self._categories_lst = categories_lst

    @property
    def amount_per_category(self):
        return self._amount_per_category

    @amount_per_category.setter
    def amount_per_category(self, amount_per_category):
        if isinstance(amount_per_category, dict) or not amount_per_category:
            raise Exception('Class: {} Error Amount Per Category '
                            .format(self.__class__.__name__))
        self._amount_per_category = amount_per_category

    @property
    def category_set(self):
        return self._category_set

    @category_set.setter
    def category_set(self, category_set):
        if isinstance(category_set, set) or not category_set:
            raise Exception('Class: {} Error Category Set'
                            .format(self.__class__.__name__))
        self._category_set = category_set


class AccountOutgoing(Account):
    def __init__(self):
        super(AccountOutgoing, self).__init__(self)


class AccountIncoming(Account):
    def __init__(self):
        super(AccountIncoming, self).__init__(self)


class AccountBalance(Account):
    def __init__(self):
        super(AccountBalance, self).__init__(self)

        self._balance_table_columns = None

        self._equal_categories = None

    @property
    def equal_categories(self):
        return  self._equal_categories

    @equal_categories.setter
    def equal_categories(self, equal_categories):
        self._equal_categories = equal_categories

    @property
    def balance_table_columns(self):
        return self._balance_table_columns

    @balance_table_columns.setter
    def balance_table_columns(self, balance_table_columns):
        self._balance_table_columns = balance_table_columns

    def create_balance_table(self):
        table_keys = THEAD(TR(*[TD(B(k)) for k in self.balance_table_columns]))
        table_rows = [TR(*[TD(v) for k, v in row.items()])
                      for row in self.balance_per_category]
        balance_table = TABLE(table_keys, table_rows, _class='web2py_grid')
        return balance_table

    def _get_in_out_difference(self):
        equal_categories = []
        for inc in self.incoming_data:
            for out in self.outgoing_data:
                if inc['category'] == out['category']:
                    equal_categories.append(inc['category'])
                    in_out_diff = inc['amount'] - out['amount']
                    self.balance_per_category.append(dict(
                        incoming_amt=inc['amount'],
                        outgoing_amt=out['amount'],
                        in_out_diff=in_out_diff,
                        category_in=inc['category'],
                        category_out=out['category']))
        self.equal_categories = equal_categories

    def _get_incoming_dat_if_category_not_equal(self):
        for inc in self.incoming_data:
            if not inc['category'] in self.equal_categories:
                self.balance_per_category.append(dict(
                    incoming_amt=inc['amount'],
                    outgoing_amt='',
                    in_out_diff='',
                    category_in=inc['category'],
                    category_out=''))

    def _get_outgoing_dat_if_category_not_equal(self):
        for out in self.outgoing_data:
            if not out['category'] in self.equal_categories:
                self.balance_per_category.append(dict(
                    incoming_amt='',
                    outgoing_amt=out['amount'],
                    in_out_diff='',
                    category_in='',
                    category_out=out['category']))

    def get_balance_table_data(self):
        self._get_in_out_difference()
        self._get_incoming_dat_if_category_not_equal()
        self._get_outgoing_dat_if_category_not_equal()

