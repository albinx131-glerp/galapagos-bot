import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("activo en casa papaa")

@bot.tree.command(name="verificar", description="Te da el rol Verificado")
async def verificar(interaction: discord.Interaction):
    rol = discord.utils.get(interaction.guild.roles, name="☕🥞 | Miembros del Servidor.")
    if rol:
        await interaction.user.add_roles(rol)
        await interaction.response.send_message("Ya estás verificado 🔓", ephemeral=True)
    else:
        await interaction.response.send_message("No existe el rol", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    print("Mensaje detectado:", message.content)

    if "hola" in message.content.lower():
        await message.channel.send("Qué fue ñaño 😎")

    if "hijo de tu mami" in message.content.lower():
        await message.channel.send("la tuya por ciacaso")

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    canal = discord.utils.get(member.guild.text_channels, name="》︱🍻・bienvenidas")

    if canal is None:
        print("No se encontró el canal de bienvenida")
        return

    embed = discord.Embed(
        title="🏝️ | ¡BIENVENIDO A GALÁPAGOS RP!",
        description=(
            f"¡Hola {member.mention}!\n\n"
            "Gracias por unirte a nuestra comunidad.\n"
            "Para acceder a la ciudad y recibir tu **Bono de Ciudadanía ($500)**, es obligatorio verificarte.\n\n"
            "**Pasos a seguir:**\n"
            "1️⃣ Ve al canal de verificación\n"
            "2️⃣ Escribe `/verificar`\n"
            "3️⃣ Recibe tu rol de **Ciudadano**\n\n"
            "¡Disfruta tu estadía! 🌴"
        ),
        color=0x00c8ff
    )

    embed.set_image(url="https://media.discordapp.net/attachments/1449763992913444865/1453393835492376577/Gemini_Generated_Image_z5lct2z5lct2z5lc.png")
    embed.set_footer(text=f"🏝️ | GALÁPAGOS RP, {member.name}")

    await canal.send(embed=embed)

# ---------- TICKETS ----------

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Abrir ticket", style=discord.ButtonStyle.green)
    async def abrir(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        categoria = discord.utils.get(guild.categories, name="tickets pendientes staff")

        if categoria is None:
            await interaction.response.send_message(
                "No existe la categoría **tickets pendientes staff**",
                ephemeral=True
            )
            return

        canal = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            category=categoria
        )

        # 🔒 CERRAMOS TODO
        await canal.set_permissions(guild.default_role, read_messages=False)

        # 👤 SOLO EL USUARIO
        await canal.set_permissions(user, read_messages=True, send_messages=True)

        # 🛡️ STAFF (opcional)
        staff = discord.utils.get(guild.roles, name="║╾╼╾║ɢᴀʟᴀᴘᴀɢᴏꜱ ᴇʀᴘ [ꜱᴛᴀꜰꜰ]║╼╼╼║")
        if staff:
            await canal.set_permissions(staff, read_messages=True, send_messages=True)

        await canal.send(
            f"🎫 {user.mention} este es tu ticket privado.\nExplica tu problema."
        )

        await interaction.response.send_message(
            f"Ticket creado: {canal.mention}",
            ephemeral=True
        )


@bot.command()
async def ticket(ctx):
    embed = discord.Embed(
        title="🎫 | Sistema de Soporte",
        description=(
            "¿Necesitas ayuda del staff?\n\n"
            "Presiona el botón de abajo para abrir un ticket privado.\n"
            "Un miembro del staff te atenderá lo antes posible."
        ),
        color=0x00ff99
    )

    await ctx.send(embed=embed, view=TicketView())


import os
bot.run(os.getenv("TOKEN"))
