import pyjokes
import re
from pywabot import types
from utils import utils
from utils import data_manager

user_absen_data = {}

def register_handlers(bot):
    @bot.on_message
    async def welcome_message(message):
        if message.text and not message.text.startswith('.'):
            teks = f"Hai *{message.sender_name}*, kamu mau ngapain?\n\n- ketik *.list* untuk melihat daftar perintah"
            await bot.mark_chat_as_read(message)
            await bot.typing(message.chat, duration=1)
            await bot.send_message(message.chat, teks, reply_chat=message)

    @bot.handle_msg(".list")
    async def show_menu(message):
        teks = "Berikut adalah perintah dari bot ini:\n\n- (*.kata*) Hasilkan kata-kata mutiara\n- (*.absen*) untuk melakukan absensi"
        await bot.mark_chat_as_read(message)
        await bot.typing(message.chat, duration=1)
        await bot.send_message(
            message.chat, 
            teks, 
            reply_chat=message
        )

    @bot.handle_msg(".kata")
    async def word_generator(message):
        joke = pyjokes.get_joke()
        teks = f"Kata-kata motivasi lucu:\n\n{joke}"
        await bot.mark_chat_as_read(message)
        await bot.typing(message.chat, duration=1)
        await bot.send_message(
            message.chat, 
            teks, 
            reply_chat=message
        )

    @bot.handle_msg(".absen")
    async def absensi(message: types.WaMessage):
        bot.set_user_state(message.chat, "awaiting_absen_location")
        await bot.mark_chat_as_read(message)
        await bot.typing(message.chat, duration=1)
        await bot.send_message(
            message.chat, 
            "Silakan kirim lokasi kamu untuk melanjutkan absen", 
            reply_chat=message
        )

    @bot.on_location(user_state="awaiting_absen_location")
    async def process_absen_location(message: types.WaMessage):
        bot.clear_user_state(message.chat)
        config = utils.load_config()

        maps_url = config.get("gmaps_url")
        radius_m = int(re.findall(r"\d+", str(config.get("radius", "100")))[0])

        target_lat, target_lon = await utils.get_coordinate(maps_url)
        if target_lat is None or target_lon is None:
            await bot.send_message(message.chat, "Gagal mengambil koordinat target.", reply_chat=message)
            return

        loc = message.get_location()
        lat, lon = loc.get("latitude"), loc.get("longitude")
        if lat is None or lon is None:
            await bot.send_message(message.chat, "Lokasi tidak valid.", reply_chat=message)
            return

        distance = utils.haversine(lat, lon, target_lat, target_lon)
        
        lokasi = f"{lat}, {lon}"
        nama = message.sender_name

        if distance <= radius_m:
            absen_data = {
                "nama": nama,
                "lokasi": lokasi,
                "distance": distance,
                "status": "Hadir"
            }
            user_absen_data[message.chat] = absen_data
            bot.set_user_state(message.chat, "awaiting_absen_image")
            status = "Hadir"
            reply_text = (
                f"Lokasi berhasil di verifikasi!\nLokasi kamu berada dalam radius *{radius_m}* meter.\n"
                f"Jarak ke titik: *{distance:.2f}* meter.\n\n"
                f"Silakan kirim foto kamu untuk melanjutkan proses absensi."
            )
        else:
            selisih = distance - radius_m
            status = "Di Luar Jangkauan"
            reply_text = (
                f"Lokasi di luar radius *{radius_m}* meter.\n"
                f"Jarak dari batas: *{selisih:.2f}* meter."
            )
        
        data_manager.save_absensi(nama, lokasi, distance, status)
        await bot.mark_chat_as_read(message)
        await bot.typing(message.chat, duration=1)
        await bot.send_message(message.chat, reply_text, reply_chat=message)

    @bot.on_image(user_state="awaiting_absen_image")
    async def get_absen_image(message):
        bot.clear_user_state(message.chat)
        
        if message.image and message.chat in user_absen_data:
            absen_data = user_absen_data.pop(message.chat)
            nama = absen_data.get('nama')
            lokasi = absen_data.get('lokasi')
            distance = absen_data.get('distance')
            status = absen_data.get('status')

            file_path = await bot.download_media(message, path="downloads/")
            
            reply_text = (
                f"Absensi berhasil disimpan!\n\n"
                f"Nama: *{nama}*\n"
                f"Lokasi: *{lokasi}*\n"
                f"Jarak: *{distance:.2f}* meter\n"
                f"Status: *{status}*\n"
            )

            await bot.mark_chat_as_read(message)
            await bot.typing(message.chat, duration=1)
            await bot.send_message(message.chat, reply_text, reply_chat=message)

    @bot.handle_msg(".cancel")
    async def cancel_process(message):
        current_state = bot.get_user_state(message.chat)
        if current_state:
            bot.clear_user_state(message.chat)
            if message.chat in user_absen_data:
                del user_absen_data[message.chat]
            await bot.send_message(message.chat, "Proses dibatalkan.", reply_chat=message)
        else:
            await bot.send_message(message.chat, "Tidak ada proses yang sedang berjalan.", reply_chat=message)

