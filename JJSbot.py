import os
import discord
from discord.ext import commands
from discord.ui import Button, View

# --------------------
# BOT SETUP
# --------------------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Needed to manage roles

bot = commands.Bot(command_prefix="!", intents=intents)
TOKEN = os.getenv("TOKEN")

# --------------------
# ROLE IDS (replace with your server role IDs)
# --------------------
ROLE_1_ID = 1481860625133994137  # Replace with your first role ID
ROLE_2_ID = 1481858489889587283 # Replace with your second role ID
ROLE_3_ID = 1481858442066006128  # Replace with your third role ID

# --------------------
# EVENTS
# --------------------
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# --------------------
# COMMAND TO SEND BUTTONS EMBED
# --------------------
@bot.command()
async def roles(ctx):
    # --- CREATE BUTTONS ---
    button1 = Button(label="Role 1", style=discord.ButtonStyle.primary)
    button2 = Button(label="Role 2", style=discord.ButtonStyle.success)
    button3 = Button(label="Role 3", style=discord.ButtonStyle.danger)

    # --- ROLE ASSIGN FUNCTION ---
   async def assign_role(interaction, role_id):
    try:
        guild = interaction.guild
        member = interaction.user
        roles = [
            guild.get_role(ROLE_1_ID),
            guild.get_role(ROLE_2_ID),
            guild.get_role(ROLE_3_ID)
        ]
        for r in roles:
            if r.id != role_id and r in member.roles:
                await member.remove_roles(r)
        selected_role = guild.get_role(role_id)
        if selected_role not in member.roles:
            await member.add_roles(selected_role)
            await interaction.response.send_message(
                f"You now have the role: **{selected_role.name}**", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You already have the role: **{selected_role.name}**", ephemeral=True
            )
    except Exception as e:
        print(f"[ERROR] Failed to assign role: {e}")
        await interaction.response.send_message(
            "Something went wrong! Check bot permissions and role hierarchy.", ephemeral=True
        )

    # --- ASSIGN CALLBACKS PROPERLY ---
    async def button1_callback(interaction):
        await assign_role(interaction, ROLE_1_ID)

    async def button2_callback(interaction):
        await assign_role(interaction, ROLE_2_ID)

    async def button3_callback(interaction):
        await assign_role(interaction, ROLE_3_ID)

    button1.callback = button1_callback
    button2.callback = button2_callback
    button3.callback = button3_callback

    # --- ADD BUTTONS TO VIEW ---
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    # --- CREATE EMBED ---
    embed = discord.Embed(
        title="Choose Your Role",
        description="Click a button to assign yourself **one role** from this set. "
                    "Other roles will be removed automatically.",
        color=discord.Color.blue()
    )

    await ctx.send(embed=embed, view=view)

# --------------------
# RUN BOT
# --------------------
bot.run(TOKEN)
