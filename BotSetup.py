from telegram.ext import ApplicationBuilder, PicklePersistence
from secrets import TOKEN
import Model


def setup_app():
    per = PicklePersistence(filepath="data")

    app_b = ApplicationBuilder()
    app_b.token(TOKEN)
    app_b.persistence(per)
    app = app_b.build()
    return app

