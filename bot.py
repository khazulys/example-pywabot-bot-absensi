import asyncio
from pywabot import PyWaBot
from handlers import handlers

async def main():
    apikey = "API_KEY"
    session = "my_whatsapp_session"
    bot = PyWaBot(session_name=session, api_key=apikey)

    handlers.register_handlers(bot)

    try:
        if await bot.connect():
            print("Bot is ready for incoming messages ...")
            await bot.start_listening()
        else:
            try:
                phone_number = int(input("Enter your phone number (e.g., 628): "))
                code = await bot.request_pairing_code(phone_number)
                if code:
                    print(f"Your pairing code: {code}")
                    print("Waiting for connection after pairing...")
                    if await bot.wait_for_connection(timeout=120):
                        print("Bot connected successfully!")
                        await bot.start_listening()
                    else:
                        print("Connection timeout after pairing.")
                else:
                    print("Failed to request pairing code.")
            except ValueError:
                print("Invalid phone number.")
            except Exception as e:
                print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print("Bot stopped by user.")

if __name__ == "__main__":
    asyncio.run(main())
