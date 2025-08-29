from discord.ui import View
import discord

class PaginatorView(View):
    def __init__(self, pages: list[discord.Embed]):
        super().__init__()
        self.pages = pages
        self.current_page = 0
        self.update_buttons()
    
    def update_buttons(self):
        self.children[0].disabled = (self.current_page == 0)
        self.children[1].disabled = (self.current_page == len(self.pages) - 1)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary, custom_id="previous")
    async def previous_page_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary, custom_id="next")
    async def next_page_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)
        else:
            await interaction.response.defer()