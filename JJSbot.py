import os
import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Needed to manage roles

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("TOKEN")

# Replace with your actual Discord role IDs
ROLE_1_ID = 1481860625133994137 # Role for Button 1
ROLE_2_ID = 1481858489889587283 # Role for Button 2
ROLE_3_ID = 1481858442066006128  # Role for Button 3

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def roles(ctx):
    # Create buttons
    button1 = Button(label="Role 1", style=discord.ButtonStyle.primary)
    button2 = Button(label="Role 2", style=discord.ButtonStyle.success)
    button3 = Button(label="Role 3", style=discord.ButtonStyle.danger)

    # Button callback helper
    async def assign_role(interaction, role_id):
        guild = interaction.guild
        member = interaction.user
        roles = [
            guild.get_role(ROLE_1_ID),
            guild.get_role(ROLE_2_ID),
            guild.get_role(ROLE_3_ID)
        ]
        # Remove other roles
        for r in roles:
            if r.id != role_id and r in member.roles:
                await member.remove_roles(r)
        # Add selected role
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

    # Assign callbacks
    button1.callback = lambda i: assign_role(i, ROLE_1_ID)
    button2.callback = lambda i: assign_role(i, ROLE_2_ID)
    button3.callback = lambda i: assign_role(i, ROLE_3_ID)

    # Add buttons to a view
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    # Create an embed
    embed = discord.Embed(
        title="Choose Your Skill Level.",
        description="Pick a role based on your skill level."
                    "You may only have one role.",
        color=discord.Color.yellow()
    )

    # Send the embed with buttons
    await ctx.send(embed=embed, view=view)

bot.run(TOKEN)
