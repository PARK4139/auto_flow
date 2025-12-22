def move_f_via_telegram_bot_v2(f):
    from telegram import Bot
    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN
    from pk_internal_tools.pk_functions.get_token_from_f_token import get_token_from_f_token

    token_telegram = get_token_from_f_token(f_token=rf'{D_PK_RECYCLE_BIN}\token_telegram.txt', initial_str="")
    token_telegram_chat_id = get_token_from_f_token(f_token=rf'{D_PK_RECYCLE_BIN}\token_telegram_chat_id.txt', initial_str="")
    bot = Bot(token=token_telegram)

    async def move_f_to_telegram_bot_chat_room():
        try:
            with open(f, "rb") as f_obj:
                await bot.send_document(chat_id=token_telegram_chat_id, document=f_obj, timeout=60)  # 기본 20초에서 60초로 증가
            print("_f_ 전송 성공!")
        except Exception as e:
            print(f" 오류 발생: {e}")

    import asyncio
    asyncio.run(move_f_to_telegram_bot_chat_room())
