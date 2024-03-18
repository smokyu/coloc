import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands
from bot import ColoBot
from datetime import datetime
from cogs.base_cog import BaseCog
import random
from translate import Translator
translator= Translator(from_lang="english",to_lang="french")

colobot = ColoBot

async def setup(bot: ColoBot):
    await bot.add_cog(Tasks(bot), guilds=[discord.Object(id=1218298385480683630)])
    

class Tasks(BaseCog):
    def __init__(self, bot: ColoBot):
        self.bot = colobot
        self.tasks_list = ["Aspirateur + Serpilllère", "Laver SdB", "Laver WC", "Vaisselle", "Laver vitres + miroirs"]
        self.mates = ["Pierre", "Paul", "Jacques", "Martine", "Françoise"]
        self.tasks_attribution = []
            
    def set_tasks(self):
            numbers = []
            _tasks_attribution = []
            random.shuffle(self.mates)
            print(self.mates, type(self.mates))
            print(random.shuffle(self.mates), type(random.shuffle(self.mates)))
            for mate in self.mates:
                i = 0
                if i != 4:
                    print("here")
                    while True:
                        number = random.randint(0, len(self.tasks_list)-1)
                        if number not in numbers:
                            numbers.append(number)
                            _tasks_attribution.append([mate, number])
                            i += 1
                            break
            return _tasks_attribution

    @commands.Cog.listener()
    async def on_ready(self):
        self.tasks_attribution = self.set_tasks()

    @app_commands.command(name="passer_un_jour", description="Passe un jour")
    async def passer_un_jour(self, interaction: discord.Interaction):
        self.tasks_attribution = self.set_tasks()
        await interaction.response.send_message("Jour passé!", ephemeral=True)
                
    @app_commands.command(name="liste_des_tâches", description="Connaitre les tâches du jour")
    async def liste_des_taches(self, interaction: discord.Interaction):
        if interaction is None or interaction.response is None:
            # L'interaction n'est plus valide
            return

        if len(self.tasks_attribution) != 0:
            date = translator.translate(datetime.today().strftime('%A %d %B'))
            embed = discord.Embed(
                title=f"Liste des tâches du {date.title()}:", color=0x00f987)
            for task in self.tasks_attribution:
                task_index = task[1]
                if task_index is not None and 0 <= task_index < len(self.tasks_list):
                    task_description = self.tasks_list[task_index]
                    if task_description is not None:
                        embed.add_field(name=task[0], value=str(task_description), inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

                
    class Add_a_task(discord.ui.Modal, title='Ajouter une tâche'):
        def __init__(self, tasks_cog):
            super().__init__(timeout=None)  # Définissez timeout à None pour éviter une erreur
            self.tasks_cog = tasks_cog
            self.custom_id = "add_task_modal"  # Ajoutez un custom_id

        name = discord.ui.TextInput(
            label='Tâche',
            placeholder='Entrez la nouvelle tâche ici...',
        )

        async def on_submit(self, interaction: discord.Interaction):
            self.tasks_cog.tasks_list.append(self.name.value)
            await interaction.response.send_message("Tâche prochainement ajoutée à la liste.", ephemeral=True)

    @app_commands.command(name="ajouter_une_tache", description="Ajoute une tâche à la liste")
    async def ajouter_une_tache(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.Add_a_task(self))
            
    class Add_a_mate(discord.ui.Modal, title='Ajouter une tâche'):
        def __init__(self, tasks_cog):
            super().__init__(timeout=None)  # Définissez timeout à None pour éviter une erreur
            self.tasks_cog = tasks_cog
            self.custom_id = "add_mate_modal"  # Ajoutez un custom_id

        name = discord.ui.TextInput(
            label='Prénom du colocataire',
            placeholder='Entrez le nom du coloc\' ici...',
        )

        async def on_submit(self, interaction: discord.Interaction):
            self.tasks_cog.mates.append(self.name.value)
            await interaction.response.send_message("Coloctaire prochainement ajoutée à la coloc'.", ephemeral=True)

    @app_commands.command(name="ajouter_un_colocataire", description="Ajoute un colocataire à la coloc'")
    async def ajouter_un_colocataire(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.Add_a_mate(self))

    class Feedback(discord.ui.Modal, title='Faire un retour'):
        name = discord.ui.TextInput(
            label='Votre pseudo',
            placeholder='Entrez votre pseudo ici...',
        )

        feedback = discord.ui.TextInput(
            label='Que pensez-vous de l\'appli ?',
            style=discord.TextStyle.long,
            placeholder='Écrivez votre avis ici...',
            max_length=300,
        )

        async def on_submit(self, interaction: discord.Interaction):
            try:
                staff_member = interaction.guild.get_member(667045884332343308)
                await staff_member.send(f"**__Avis de {self.name.value}__**:  \"*{self.feedback.value}\"*")
            except:
                pass
            await interaction.response.send_message(f'Merci pour votre retour, {self.name.value} !', ephemeral=True)

    @app_commands.command(name="feedback", description="Ouvre un modal pour nous donner votre avis sur notre app !")
    async def feedback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.Feedback())
