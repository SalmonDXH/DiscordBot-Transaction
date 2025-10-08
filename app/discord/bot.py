import discord
import os
from discord.ext import commands
from discord import app_commands
from app.transaction.vietqr import VietQR
from app.utils.color_config import CommandEmbedColor
from dotenv import load_dotenv


def embed_builder(title,desc,color):
    return discord.Embed(title=title, description=desc, color=CommandEmbedColor[color])


class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        load_dotenv()
        self.logs_channel = int(os.getenv('logs_channel').strip())
        
        super().__init__(
            command_prefix='!!!!!!!',
            intents=intents,
            help_command=None
        )
        
    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Slash commands synced successfully!")
    
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")


discord_bot = DiscordBot()


@discord_bot.tree.command(name='ping', description='Check bot latency')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! {round(discord_bot.latency*1000)}ms')

@discord_bot.tree.command(name='donate_vn',description='Donate bằng ngân hàng hoặc momo để nhận role Orca')
async def donate_vn(interaction: discord.Interaction):
    content = f'OrcaStart{interaction.user.id}End'
    image = VietQR(100000, content).apiqr
    description = f'Người donate: <@{interaction.user.id}>\nGiá: **100k vnd**\nNội dung: `{content}`'
    embed = embed_builder('VietQR',description,'pink')
    embed.set_image(url=image)
    await interaction.response.send_message(embed=embed)



async def give_role_to_user(guild_id, user_id, role_id, channel_id):
    guild = discord_bot.get_guild(guild_id)
    if guild is None:
        print("❌ Guild not found!")
        await Logs('[ROLE] FAIL', f'Guild not found!', 'red', channel_id)
        return

    member = guild.get_member(user_id)
    if member is None:
        try:
            member = await guild.fetch_member(user_id)
        except:
            print("❌ Member not found in guild!")
            await Logs('[ROLE] FAIL', f'Member not in guild', 'red', channel_id)
            return

    role = guild.get_role(role_id)
    if role is None:
        print("❌ Role not found!")
        await Logs('[ROLE] FAIL', f'Role not found', 'red', channel_id)
        return

    try:
        await member.add_roles(role)
        print(f"✅ Gave role '{role.name}' to {member.display_name}")
        await Logs('[ROLE] SUCCESS', f'Successfully give <@&{role_id}> to <@{member.id}>', 'green',channel_id)
    except Exception as e:
        await Logs('[ROLE] FAIL', f'Error during giving <@&{role_id}> to <@{member.id}>', 'red',channel_id)
        print(f"❌ Failed to give role: {e}")
    

async def Logs(title:str,logs:str,color:str, channel_id=0):
    try:
        logs_channel = discord_bot.get_channel(discord_bot.logs_channel)
        if channel_id != 0:
            logs_channel = discord_bot.get_channel(channel_id)
        if not logs_channel:
            print('Channel not found')
            return
        embed = embed_builder(title,logs,color)
        await logs_channel.send(embed=embed)
    except Exception as e:
        print(e)
    pass