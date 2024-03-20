import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands
from bot import ColoBot
from datetime import datetime
from cogs.base_cog import BaseCog
import random

colobot = ColoBot

async def setup(bot: ColoBot):
    await bot.add_cog(Tasks(bot), guilds=[discord.Object(id=1218298385480683630)])
    

class Tasks(BaseCog):
    def __init__(self, bot: ColoBot):
        self.bot = colobot
        self.shop = [["-10% au bouchon lyonnais de Place Pi sur le menu Tradition", 300], ["Une place de ciné offerte au Pathé", 200], ["Un mois d'abonnement Amazon prime", 1000]]
        self.tasks_list = ["Aspirateur + Serpilllère", "Laver SdB", "Laver WC", "Vaisselle", "Laver vitres + miroirs"]
        self.mates = ["Pierre", "Paul", "Jacques", "Martine", "Françoise"]
        self.tasks_pebibility_score = [["Aspirateur + Serpilllère", 3], ["Laver SdB", 2], ["Laver WC", 5], ["Vaisselle", 4], ["Laver vitres + miroirs", 2]]
        self.balances = [["Pierre", 0], ["Paul", 0], ["Jacques", 0], ["Martine", 0], ["Françoise", 0]]
        self.tasks_attribution = []
     
    def set_tasks(self):
            numbers = []
            _tasks_attribution = []
            random.shuffle(self.mates)
            for mate in self.mates:
                i = 0
                if i != 4:
                    while True:
                        number = random.randint(0, len(self.tasks_list)-1)
                        if number not in numbers:
                            numbers.append(number)
                            _tasks_attribution.append([mate, number])
                            i += 1
                            break
                        elif len(numbers) == len(self.tasks_list):
                            break
                            
            return _tasks_attribution
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.tasks_attribution = self.set_tasks()

    @app_commands.command(name="passer_un_jour", description="Passe un jour")
    async def passer_un_jour(self, interaction: discord.Interaction):
        self.tasks_attribution = self.set_tasks()
        await interaction.response.send_message("Jour passé!", ephemeral=True)

    @app_commands.command(name="liste_des_tâches", description="Afficher la liste des tâches")
    async def tasks_list(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Tâches et prix:", color=0x00f987)
        for task in self.tasks_pebibility_score:
            task_index = task[1]
            if task_index is not None and 0 <= task_index < len(self.tasks_pebibility_score):
                embed.add_field(name=task[0], value=task[1], inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)
  
    @app_commands.command(name="tâches_du_jour", description="Connaitre les tâches du jour")
    async def daily_tasks(self, interaction: discord.Interaction):
        if interaction is None or interaction.response is None: return

        if len(self.tasks_attribution) != 0:
            date = datetime.today().strftime('%A %d %B')
            embed = discord.Embed(  
                title=f"Liste des tâches du {date.title()}:", color=0x00f987)
            for task in self.tasks_attribution:
                task_index = task[1]
                if task_index is not None and 0 <= task_index < len(self.tasks_list):
                    task_description = self.tasks_list[task_index]
                    if task_description is not None:
                        embed.add_field(name=task[0], value=str(task_description), inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="valider_une_tâche", description="`/valider_une_tâche <tâche>` -> valide la tâche")
    async def confirm_a_task(self, interaction: discord.Interaction, task_name: str):
        if interaction is None or interaction.response is None: return

        for task in self.tasks_attribution:
            task_n = self.tasks_list[task[1]]
            if task_n.lower() == task_name.lower():
                self.tasks_attribution.remove(task)
                for balance in self.balances:
                        if balance[0].lower() == task[0].lower():
                            for penibility_score in self.tasks_pebibility_score:
                                if penibility_score[0].lower() == task_name.lower():
                                    print(balance[0], balance[1])
                                    print(penibility_score[1])
                                    result = int(balance[1]) + int(penibility_score[1])
                                    print(result)
                                    balance[1] == result
                                    print(balance[1])
                break


        await interaction.response.send_message(f"Tâche \"{task_n}\" validée !", ephemeral=True)

    @app_commands.command(name="porte-feuille", description="`/porte-feuille <nom_de_la_personne>` -> affiche le compte")
    async def balance(self, interaction: discord.Interaction, mate_name: str):
        if interaction is None or interaction.response is None: return

        embed = discord.Embed(
            title=f"Compte en banque de {mate_name}:", color=0x00f987)

        for balance in self.balances:
            if balance[0].lower() == mate_name.lower():
                embed.add_field(name="Compte courant", value=f"{balance[1]} :coin:", inline=False)
                
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    @app_commands.command(name="boutique", description="Voir les objets en boutique")
    async def shop(self, interaction: discord.Interaction):
        if interaction is None or interaction.response is None: return
        
        embed = discord.Embed(
            title=f"Boutique", color=0x00f987)
        for product in self.shop:
            embed.add_field(name=product[0], value=f"Prix: {product[1]} :coin:", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    class Add_a_task(discord.ui.Modal, title='Ajouter une tâche'):
        def __init__(self, tasks_cog):
            super().__init__(timeout=None)
            self.tasks_cog = tasks_cog
            self.custom_id = "add_task_modal"

        name = discord.ui.TextInput(
            label='Tâche',
            placeholder='Entrez la nouvelle tâche ici...',
        )
        i = 0
        while True:  
            penibility_score = discord.ui.TextInput(
                label="Score de pénibilité de la tâche",
                placeholder="Notez la tâche de 1 à 5. | 5 étant une tâche très pénible"
            )
            
            try:
                penibility_score = int(penibility_score.value)
                if penibility_score >= 1 and penibility_score <= 5:
                    break
            except: i += 1
            if i == 10:
                break

        async def on_submit(self, interaction: discord.Interaction):
            self.tasks_cog.tasks_list.append(self.name.value)
            print([self.name.value, self.penibility_score])
            self.tasks_cog.tasks_pebibility_score.append([self.name.value, int(self.penibility_score.value)])
            await interaction.response.send_message("Tâche prochainement ajoutée à la liste.", ephemeral=True)

    @app_commands.command(name="ajouter_une_tache", description="Ajoute une tâche à la liste")
    async def add_a_task_into_the_list(self, interaction: discord.Interaction):
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
    async def add_a_mate_into_the_list(self, interaction: discord.Interaction):
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
