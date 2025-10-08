from app.discord.bot import discord_bot,give_role_to_user
from dotenv import load_dotenv
import os, asyncio
from flask import Flask, request, jsonify
from app.discord.bot import Logs

app_server= Flask(__name__)
@app_server.route("/casso-webhook", methods=["POST"])
def recieve_payment_vietqr():
    try:
        data = request.json
        data_detail = data['data']
        userid = int(data_detail['description'].split('Start')[1].split('End')[0])
        try:
            asyncio.run_coroutine_threadsafe(Logs('[VN PAYMENT]', f'Recieve **{format(data_detail['amount'],',')} VND** from <@{userid}>', 'yellow'), discord_bot.loop)
        except Exception as e:
            print(e)
        if data_detail['amount'] >= 100000 and 'Orca' in data_detail['description']:
            load_dotenv()
            main_guild = int(os.getenv('main_guild').strip())
            role_id = int(os.getenv('donate_role').strip())
            asyncio.run_coroutine_threadsafe(give_role_to_user(main_guild, userid, role_id),discord_bot.loop)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid data"}), 400

@app_server.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "ok"}), 200

@app_server.route("/paypal-webhook", methods=["POST"])
def recieve_payment_paypal():
    try:
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid data"}), 400

def run_flask():
    app_server.run(host="0.0.0.0", port=5000)