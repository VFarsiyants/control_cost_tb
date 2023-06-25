from sqlalchemy import bindparam

from database.models import Category, Expense
from database.connection import Session
from bot.tools import ai_request


def categorize_ai():
    # Getting expenses without category
    with Session.begin() as session:
        expenses_without_category = session.query(Expense)\
            .filter(Expense.category_id==None).all()
        
        if expenses_without_category == list():
            #TODO logging: there are not expesnes with aren't set category
            return
        
        categories = session.query(Category).all()

        expenses_str = ', '.join([f'{expense.id}. {expense.name}' 
                                  for expense in expenses_without_category])
        categories_str = ', '.join([f'{cat.id}. {cat.name}' 
                                    for cat in categories])

    # Describing query for gpt-3
    query = f'''Here the list of expenses' names: {expenses_str}. And here 
    the list of categories' names of expense: {categories_str}. For each id of 
    expense should be selected appropriate id of category
    '''

    # To get determinated response from gpt-3, should be provided function
    func = {
        'name': 'set_category_to_expense',
        'description': 'Set category to each expense in the list',
        'parameters': {
            'type': 'object',
            'properties': {
                'result': {
                    'type': 'array',
                    'items':{
                        'type': 'object',
                        'properties': {
                            'expense_id': {
                                'type': 'number',
                                'description': 'id of expense'
                            },
                            'category_id': { 
                                'type': 'number',
                                'description': 'id of category'
                            },
                        },
                        'description': '''id of expense and id of 
                        category related to this expense'''
                    },
                    'description': '''List with objects which represent 
                    link beetwen expense and category'''
                },
            },
            'required': ['result'],
        },
    }

    try:
        expense_to_category: list[dict] = ai_request(query, func, 'result')
    except Exception:
        #TODO add loging, error on handling request to GPT
        return

    # updating category of expense in our table
    with Session.begin() as session:

        stmt = Expense.__table__.update().\
            where(Expense.id == bindparam('expense_id')).\
            values(category_id=bindparam('category_id'))
        session.execute(
            stmt, expense_to_category
        )
