from discord.ui import View, button, Button
import discord

class MatchPaginatorView(View):
    def __init__(self, pages: list[discord.Embed]):
        super().__init__(timeout=180) # El carrusel se elimina después de 3 minutos de inactividad
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

class RecentMatchesPaginatorView(MatchPaginatorView):
    def __init__(self, pages: list[discord.Embed], all_matches_data: list):
        super().__init__(pages)
        self.all_matches_data = all_matches_data
        self.page_size = 5 
        self.add_item(self.copy_ids_button) 

    def get_current_page_ids(self) -> list[str]:
        start = self.current_page * self.page_size
        end = start + self.page_size
        current_page_data = self.all_matches_data[start:end]
        return [str(dict(row).get('match_id')) for row in current_page_data]

    @button(label="Copy IDs", style=discord.ButtonStyle.blurple)
    async def copy_ids_button(self, interaction: discord.Interaction, button: Button):
        current_ids = self.get_current_page_ids()
        ids_message = "Here are the match IDs for this page:\n" + "\n".join(f"`{mid}`" for mid in current_ids)
        await interaction.response.send_message(ids_message, ephemeral=True)