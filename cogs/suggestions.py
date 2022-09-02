import discord
from discord import app_commands
from discord.ext import commands
import json, traceback

class Suggestions(commands.Cog):
    
    def __init__(self, client):
        print("[Cog] Suggestions has been initiated")
        self.client = client
        with open("./json/config.json", "r") as f:
            config = json.load(f)
        self.config = config
        self.stalks = []
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.config['suggestions_channel']:
            if not message.author.bot:
                buttons = SuggestButtons()
                reply = await message.reply("Please use the slash command /suggest or click this button", view=buttons)
                await message.delete()
                await reply.delete(delay=300)
    
    @app_commands.command(name="suggest", description="Suggest something for the servers!")
    async def suggest(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SuggestionForm())
        
            
    @app_commands.command(name="rejectsuggestion", description="Reject a suggestion!")
    @app_commands.describe(suggestion_number='What suggestion number?')
    @app_commands.describe(response='Why did you reject it?')
    async def rejectsuggestion(self, interaction: discord.Interaction, suggestion_number:int, response:str):
        stored_suggestions = ''
        with open('./json/suggestions.json', 'r') as f:
            stored_suggestions = json.load(f)
        stored_suggestions[suggestion_number]['response'] = response
        stored_suggestions[suggestion_number]['status'] = 'rejected'
        
        responsechannel = interaction.guild.get_channel(self.config['suggestions_response_channel'])
        suggestionschannel = interaction.guild.get_channel(self.config['suggestions_channel'])
        suggester = interaction.guild.get_member(stored_suggestions[suggestion_number]['suggester_id'])
        message = await suggestionschannel.fetch_message(stored_suggestions[suggestion_number]['message_id'])
        await message.delete()
        
        embed = discord.Embed(title=f"Suggestion #{suggestion_number} from {stored_suggestions[suggestion_number]['suggester']}", color=int(self.config['color'], base=16))
        embed.add_field(name='The suggestion', value=f"```{stored_suggestions[suggestion_number]['suggestion']}```", inline=False)
        embed.add_field(name='Status', value=f"Rejected.", inline=False)
        embed.add_field(name='Response', value=f"```{response}```", inline=False)
        embed.set_footer(text="Developed by Gnomeslayer#5551")
        
        if self.config['send_response_to_channel']:
            await responsechannel.send(embed=embed)
        with open('./json/suggestions.json', 'w') as f:
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
        with open('./json/suggestions.json', 'r') as f:
            stored_suggestions = json.load(f)
        stored_suggestions[suggestion_number]['response'] = response
        stored_suggestions[suggestion_number]['status'] = 'approved'
        
        responsechannel = interaction.guild.get_channel(self.config['suggestions_response_channel'])
        suggestionschannel = interaction.guild.get_channel(self.config['suggestions_channel'])
        suggester = interaction.guild.get_member(stored_suggestions[suggestion_number]['suggester_id'])
        message = await suggestionschannel.fetch_message(stored_suggestions[suggestion_number]['message_id'])
        await message.delete()
        
        embed = discord.Embed(title=f"Suggestion #{suggestion_number} from {stored_suggestions[suggestion_number]['suggester']}", color=int(self.config['color'], base=16))
        embed.add_field(name='The suggestion', value=f"```{stored_suggestions[suggestion_number]['suggestion']}```", inline=False)
        embed.add_field(name='Status', value=f"Approved.", inline=False)
        embed.add_field(name='Response', value=f"```{response}```", inline=False)
        embed.set_footer(text="Developed by Gnomeslayer#5551")
        if self.config['send_response_to_channel']:
            await responsechannel.send(embed=embed)
        with open('./json/suggestions.json', 'w') as f:
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
class SuggestButtons(discord.ui.View):
    @discord.ui.button(label="Make a suggestion!", style=discord.ButtonStyle.green)
    async def admin(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SuggestionForm())
        
class SuggestionForm(discord.ui.Modal, title="Apply to become staff for this server!"):
    def __init__(self):
        super().__init__()
    
    suggestion = discord.ui.TextInput(
        label="What is your suggestion?",
        style=discord.TextStyle.long,
        placeholder="Your suggestion goes here",
        max_length=1000,
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        stored_suggestions = ''
        config = ''
        with open('./json/config.json', 'r') as f:
            config = json.load(f)
        with open('./json/suggestions.json', 'r') as f:
            stored_suggestions = json.load(f)
        suggestionschannel = interaction.guild.get_channel(config['suggestions_channel'])
        embed = discord.Embed(title=f'Suggestion #{len(stored_suggestions)} from {interaction.user}', color=int(config['color'], base=16))
        embed.add_field(name='The suggestion', value=f'```{self.suggestion.value}```', inline=False)
        icon_url=interaction.user.display_avatar
        embed.set_footer(text="Developed by Gnomeslayer#5551", icon_url=icon_url)
        suggestion_message = await suggestionschannel.send(embed=embed)
        message_id = suggestion_message.id
        await interaction.response.send_message("Thank you for making a suggestion!", ephemeral=True)
        current_suggestion = [{'message_id': message_id, 'suggester': str(interaction.user), 'suggester_id': int(interaction.user.id), 'suggestion': self.suggestion.value, 'status': 'Unreviewed', 'response': 'None'}]
        stored_suggestions += current_suggestion
        with open('./json/suggestions.json', 'w') as f:
            f.write(json.dumps(stored_suggestions, indent=4))
            
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)
        
async def setup(client):
    await client.add_cog(Suggestions(client))
