from sqlalchemy import select, cast, func, DECIMAL, asc

from database.models import Expense, User, Category
from database.connection import Session

def _get_total_stmt(username: str, period: tuple):
    total_q =select(func.sum(Expense.cost).label('total'))\
        .where(User.tg_username == username,
               Expense.created_at >= period[0],
               Expense.created_at <= period[1])\
        .join(User)
    return total_q


def get_expenses_by_categories(username: str, period: tuple):
    total_stmt = _get_total_stmt(username, period)

    sub_q =total_stmt.scalar_subquery()

    percent_field = cast(func.sum(Expense.cost) * 100 / sub_q,
                         DECIMAL(5, 2))

    stmt = (
        select(Category.name, func.sum(Expense.cost), percent_field)
        .where(User.tg_username == username,
               Expense.created_at >= period[0],
               Expense.created_at <= period[1])
        .select_from(User).join(Expense)
        .join(Category)
        .group_by(Category.name)
    )
    with Session.begin() as session:
        result = session.execute(stmt)
        total = session.scalar(total_stmt)
        return [
            {'category_name': item[0],
             'expenses_sum': item[1],
             'fraction': item[2]} for item in result
        ], total
    

def get_expenses_list(username: str, period: tuple):
    total_stmt = _get_total_stmt(username, period)

    stmt = (
        select(Expense.name, Expense.cost, Expense.created_at)
        .where(User.tg_username == username,
               Expense.created_at >= period[0],
               Expense.created_at <= period[1])
        .join(User).order_by(asc(Expense.created_at))
    )
    with Session.begin() as session:
        result = session.execute(stmt)
        total = session.scalar(total_stmt)
        return [
            {'name': item[0],
             'cost': item[1],
             'date': item[2].date().strftime('%d.%m.%Y')} for item in result
        ], total