# Gnomes Suggestions Bot
Suggestions bot allows users in your community to make a suggestion and the server owner or server admins can reject the suggestions with a reason.

Commands
--------------------------
/suggest

The bot requires several API keys to begin functioning.
--------------------------
Discord_token - https://discord.com/developers/docs/intro / https://discord.com/developers/applications <br />

Additional information the bot requires.
--------------------------
Application ID - This is the ID of the bot itself. https://discord.com/developers/applications <br />
suggestions_channel - Ensures the command is run in a specific channel.<br />
suggestions_response_channel - This is the channel the bot announces any new applications and creates threads for.<br />

How can I limit the command to specific roles/channels?
--------------------------
Go to server settings -> Integrations -> Select manage for this bot.<br />
Set @everyone to X and add roles.<br />
Set # All Channels to X and add channels.<br />

Under commands, specify settings.<br />
Note - Server owners/admins can still use the command globally.<br />
