from discord import Interaction, TextChannel


class Player:

    def __init__(self):
        self.channel: TextChannel | None = None
        self.interaction: Interaction | None = None

    @classmethod
    def from_channel(cls, channel: TextChannel):
        player = Player()
        player.channel = channel
        return player

    @classmethod
    def from_interaction(cls, interaction: Interaction):
        player = Player()
        player.channel = interaction.channel
        player.interaction = interaction
        return player

    async def notify(self, content: str):
        if self.channel is None:
            return
        await self.channel.send(content)

    async def reply(self, message: str):
        if self.interaction is None:
            return
        await self.interaction.response.send_message(message)
