import discord
from discord import app_commands
from discord.ext import commands
import json

class Suggestions(commands.Cog):
    
    def __init__(self, client):
        print("[Cog] Suggestions has been initiated")
        self.client = client
        with open("config.json", "r") as f:
            config = json.load(f)
        self.config = config
        self.stalks = []
    
    @app_commands.command(name="suggest", description="Suggest something for the servers!")
    @app_commands.describe(suggestion='What is your suggestion?')
    async def suggest(self, interaction: discord.Interaction, suggestion:str):
        stored_suggestions = ''
        with open('suggestions.json', 'r') as f:
            stored_suggestions = json.load(f)
        suggestionschannel = interaction.guild.get_channel(self.config['suggestions_channel'])        
        embed = discord.Embed(title=f'Suggestion #{len(stored_suggestions)} from {interaction.user}', color=0x552E12)
        embed.add_field(name='The suggestion', value=f'```{suggestion}```', inline=False)
        icon_url=interaction.user.display_avatar
        embed.set_footer(text="Developed by Gnomeslayer#5551", icon_url=icon_url)
        await suggestionschannel.send(embed=embed)
        await interaction.response.send_message("Thank you for making a suggestion!", ephemeral=True)
        current_suggestion = [{'suggester': str(interaction.user), 'suggester_id': int(interaction.user.id), 'suggestion': suggestion, 'status': 'Unreviewed', 'response': 'None'}]
        stored_suggestions += current_suggestion
        with open('suggestions.json', 'w') as f:
            f.write(json.dumps(stored_suggestions, indent=4))
            
    @app_commands.command(name="rejectsuggestion", description="Reject a suggestion!")
    @app_commands.describe(suggestion_number='What suggestion number?')
    @app_commands.describe(response='Why did you reject it?')
    async def rejectsuggestion(self, interaction: discord.Interaction, suggestion_number:int, response:str):
        stored_suggestions = ''
        with open('suggestions.json', 'r') as f:
            stored_suggestions = json.load(f)
        stored_suggestions[suggestion_number]['response'] = response
        stored_suggestions[suggestion_number]['status'] = 'rejected'
        suggester = interaction.guild.get_member(stored_suggestions[suggestion_number]['suggester_id'])
        embed = discord.Embed(title=f"Suggestion #{suggestion_number} from {stored_suggestions[suggestion_number]['suggester']}", color=0x552E12)
        embed.add_field(name='The suggestion', value=f"```{stored_suggestions[suggestion_number]['suggestion']}```", inline=False)
        embed.add_field(name='Status', value=f"Rejected.", inline=False)
        embed.add_field(name='Response', value=f"```{response}```", inline=False)
        
        responsechannel = interaction.guild.get_channel(self.config['suggestions_response_channel'])
        if self.config['send_response_to_channel']:
            await responsechannel.send(embed=embed)
        with open('suggestions.json', 'w') as f:
            f.write(json.dumps(stored_suggestions, indent=4))
        if self.config['send_response_to_user']:
            try:
                await suggester.send(embed=embed)
            except:
                await interaction.response.send_message("Thank you for rejecting a suggestion!\nI was unable to contact the person who made the suggestion.", ephemeral=True)
                return
            await interaction.response.send_message("Thank you for rejecting a suggestion!\nI have contacted the person who made the suggestion.", ephemeral=True)
        else:
            await interaction.response.send_message("Thank you for rejecting this suggestion!", ephemeral=True)
        
    @app_commands.command(name="approvesuggestion", description="Approve a suggestion!")
    @app_commands.describe(suggestion_number='What suggestion number?')
    @app_commands.describe(response='Why did you approve it?')
    async def approvesuggestion(self, interaction: discord.Interaction, suggestion_number:int, response:str):
        stored_suggestions = ''
        with open('suggestions.json', 'r') as f:
            stored_suggestions = json.load(f)
        stored_suggestions[suggestion_number]['response'] = response
        stored_suggestions[suggestion_number]['status'] = 'approved'
        suggester = interaction.guild.get_member(stored_suggestions[suggestion_number]['suggester_id'])
        embed = discord.Embed(title=f"Suggestion #{suggestion_number} from {stored_suggestions[suggestion_number]['suggester']}", color=0x552E12)
        embed.add_field(name='The suggestion', value=f"```{stored_suggestions[suggestion_number]['suggestion']}```", inline=False)
        embed.add_field(name='Status', value=f"Approved.", inline=False)
        embed.add_field(name='Response', value=f"```{response}```", inline=False)
        
        responsechannel = interaction.guild.get_channel(self.config['suggestions_response_channel'])
        if self.config['send_response_to_channel']:
            await responsechannel.send(embed=embed)
        with open('suggestions.json', 'w') as f:
            f.write(json.dumps(stored_suggestions, indent=4))
        if self.config['send_response_to_user']:
            try:
                await suggester.send(embed=embed)
            except:
                await interaction.response.send_message("Thank you for approving a suggestion!\nI was unable to contact the person who made the suggestion.", ephemeral=True)
                return
            await interaction.response.send_message("Thank you for approving a suggestion!\nI have contacted the person who made the suggestion.", ephemeral=True)
        else:
            await interaction.response.send_message("Thank you for approving this suggestion!", ephemeral=True)
        
async def setup(client):
    await client.add_cog(Suggestions(client))