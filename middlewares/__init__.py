from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .check_subscription import SubscriptionMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SubscriptionMiddleware())
