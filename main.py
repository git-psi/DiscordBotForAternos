import interactions
from interactions import Button, SelectMenu, SelectOption, spread_to_rows
from interactions.ext.wait_for import *
from interactions.ext import wait_for
import asyncio
import python_aternos
from python_aternos import Client


bot = interactions.Client(token="MTA3Mjg0MDg1NTA3MDcwNzcyMw.Glb5YJ.27Tq5jvhoM6JFZRLclAF6mWuKgqy0fKnxtPSLs")
setup(bot)

color = {
    "red": 0xae0e0e,
    "green": 0x45e400
}


def error(name, icon_url, description, title):
    embed = interactions.Embed(title=title, color=color["red"], description=description)
    embed.set_author(icon_url=icon_url, name=name)
    embed.set_thumbnail("https://cdn3.emoji.gg/emojis/3972-failed.png")
    return embed


@bot.command(
    name="servers",
    description="Lance n'importe lequel des mes serveurs Aternos !",
)
async def command(ctx):
    menu = SelectMenu(
        custom_id="s1",
        options=[
            SelectOption(label="multi_psi.aternos.me:25043", value="multi_psi", description="(Ancien serveur)"),
            SelectOption(label="adventure_psi.aternos.me:39269", value="adventure_psi", description="(Nouveau serveur)"),
        ],
        placeholder="Choisis un serveur..."
    )
    cancel_btn = Button(style=4, custom_id="cancel", label="Annuler")

    choice_msg = await ctx.send(components=spread_to_rows(menu, cancel_btn))

    try:
        choice = await bot.wait_for_component(components=(menu, cancel_btn), timeout=10)
        await choice_msg.delete()
        if choice.data.custom_id == "s1":
            server=False
            if choice.data.values[0] == "adventure_psi":
                server = ["adventure_psi.aternos.me:39269", "**Adventure Psi**", 0, "*La listes de tous les mods se trouve dans le salon dédiés !*", "https://cdn.discordapp.com/attachments/1053709927325114538/1073181519604105257/iu.png"]
            if choice.data.values[0] == "multi_psi":
                server = ["multi_psi.aternos.me:25043", "**Multi Psi**", 1, "*Pour avoir les mods de ce serveur tu peux demander à psi !*", "https://cdn.discordapp.com/attachments/1053709927325114538/1073181211159183441/2023-02-09_10.55.11.png"]

            if server:
                start_btn = Button(style=3, custom_id="start", label="Lancer")
                stop_btn = Button(style=4, custom_id="stop", label="Arreter")

                embed = interactions.Embed(title=server[1], color=color["green"], description=server[3])
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
                embed.add_field(name="Id du serveur:", value=server[0])
                embed.set_image(server[4])
                embed.set_footer(f"{ctx.author.name} a utilisé la commande /servers")
                message = await ctx.send(embeds=embed)
                ok = False
                while not ok:
                    try:
                        aternos = Client.from_credentials("alternos_psi", "alternos2007psi")
                        servers = aternos.list_servers()
                        server = servers[server[2]]
                        statut=server.status
                        embed.add_field(name="Statut du serveur:", value=statut)
                        await message.edit(embeds=embed, components=spread_to_rows(start_btn, stop_btn))
                        ok = True
                        try:
                            choice = await bot.wait_for_component(components=(start_btn, stop_btn), timeout=20)
                            if choice.data.custom_id == "start":
                                try:
                                    server.start()
                                    embed.description = "Ta demande a bien était prise en compte"
                                    await message.edit(embeds=embed)
                                except:
                                    await message.edit(embeds=error(name=ctx.author.name, icon_url=ctx.author.avatar_url, title="**Une erreur à eu lieu**", description="La commande n'a pas pu être éxécuté... Plusieurs raisons sont possibles, le serveur est peur-être déjà allumé ou le bot ne peut pas passer les sécurités misent en place par Aternos. En cas de persistance demander à psi :)"))
                            elif choice.data.custom_id == "stop":
                                try:
                                    server.stop()
                                    embed.description = "Ta demande a bien était prise en compte"
                                    await message.edit(embeds=embed)
                                except:
                                    await message.edit(embeds=error(name=ctx.author.name, icon_url=ctx.author.avatar_url, title="**Une erreur à eu lieu**", description="La commande n'a pas pu être éxécuté... Plusieurs raisons sont possibles, le serveur est peur-être déjà éteind ou le bot ne peut pas passer les sécurités misent en place par Aternos. En cas de persistance demander à psi :)"))

                        except asyncio.TimeoutError:
                            await message.edit(embeds=embed)
                    except:pass


    except asyncio.TimeoutError:
        await choice_msg.delete()
        return await ctx.send(embeds=error(title="*Tu a pris trop de temps*", description="Tu n'as pas répondu à la dernière commande que tu a effectué", name=ctx.author.name, icon_url=ctx.author.avatar_url))
    
    





bot.start()