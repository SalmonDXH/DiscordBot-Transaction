from app.discord.bot import discord_bot,give_role_to_user
from dotenv import load_dotenv
import os, asyncio
from flask import Flask, request, jsonify
from app.discord.bot import Logs
import hashlib
import json
import hmac

app_server= Flask(__name__)
@app_server.route("/casso-webhook", methods=["POST"])
def recieve_payment_vietqr():
    try:
        load_dotenv()
        secret_api = os.getenv('secret_webhook_casso')
        
        h = request.headers
        data = request.json
        if not verify_webhook_signature(h,data,secret_api):
            return jsonify({"error": "Invalid key"}), 401
        
        data_detail = data['data']
        userid = 0
        try:
            userid = int(data_detail['description'].split('Start')[1].split('End')[0])
            asyncio.run_coroutine_threadsafe(Logs('[VN PAYMENT]', f'Recieve **{format(data_detail['amount'],',')} VND** from <@{userid}>', 'yellow'), discord_bot.loop)
        except Exception as e:
            print(e)
        
        if data_detail['amount'] >= 100000 and 'Orca' in data_detail['description']:
            
            main_guild = int(os.getenv('main_guild').strip())
            role_id = int(os.getenv('donate_role_vn').strip())
            channel_id = int(os.getenv('donate_vn_channel').strip())
            asyncio.run_coroutine_threadsafe(give_role_to_user(main_guild, userid, role_id,channel_id),discord_bot.loop)
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
    


def sort_obj_data_by_key(data):
    sorted_obj = {}
    for key in sorted(data.keys()):
        if isinstance(data[key], dict):
            sorted_obj[key] = sort_obj_data_by_key(data[key])
        else:
            sorted_obj[key] = data[key]
    return sorted_obj

def verify_webhook_signature(headers, data, checksum_key):
    received_signature = headers["X-Casso-Signature"]
    timestamp_str, signature = received_signature.split(",")[0][2:], received_signature.split(",")[1][3:]
    timestamp = int(timestamp_str)

    sorted_data_by_key = sort_obj_data_by_key(data)
    message_to_sign = f"{timestamp}.{json.dumps(sorted_data_by_key, separators=(',', ':'))}"

    generated_signature = hmac.new(
        checksum_key.encode('utf-8'),
        message_to_sign.encode('utf-8'),
        hashlib.sha512
    ).hexdigest()
    return signature == generated_signature