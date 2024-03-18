from telegram.ext import ContextTypes, CommandHandler, ConversationHandler
from telegram import Update

import Model

import logging
import BotSetup

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

START, CREATE_LIST, EDIT_LIST, DELETE_LIST, NAME_LIST, ADD_LINE, DEL_LINE, FINISH_LINE, CLAIM_KEY = range(9)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if "user" not in context.user_data:
        context.user_data["user"] = Model.User()
        await update.message.reply_text("Добро пожаловать в менеджер листов!")
    await update.message.reply_text("Что вы хотите сделать с вашими листами?")
    return START


async def create_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    list_name = context.args[0] if context.args else "UndefinedList"
    data_list = Model.DataList(list_name)
    context.user_data["user"].lists.append(data_list.id)

    await update.message.reply_text(f"Новый лист {list_name} был создан!")
    await start(update, context)

    return START


async def del_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    found_lists = []
    matches = []
    if not context.args:
        found_lists = [Model.DataList.lists[list_index].name for list_index in context.user_data["user"].lists]
    else:
        for list_index in context.user_data["user"].lists:
            list_name = Model.DataList.lists[list_index].name
            if list_name.lower().startswith(context.args[0].lower()):
                found_lists.append(list_name)
            if list_name.lower().startswith == context.args[0].lower():
                matches.append(list_name)

    await update.message.reply_text(f"Найдены совпадения: {found_lists}")
    await update.message.reply_text(f"Найдены похожие: {matches}")

    await start(update, context)

    return START


async def view_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    names = []
    for list_index in context.user_data["user"].lists:
        list_name = Model.DataList.lists[list_index].name
        names.append(list_name)

    print(", ".join(i.name for i in Model.DataList.lists.values()))

    await update.message.reply_text(f"Найдены листы: {names}")

    await start(update, context)

    return START


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Работа с листами закончена")
    return ConversationHandler.END


if __name__ == "__main__":
    app = BotSetup.setup_app()

    start_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [
                CommandHandler("create_list", create_list),
                CommandHandler("delete_list", del_list),
                CommandHandler("view_list", view_list)
            ]
        },
        fallbacks=[CommandHandler("done", done)]
    )

    app.add_handler(start_conversation_handler)

    app.run_polling()
