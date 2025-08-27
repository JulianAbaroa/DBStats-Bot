from discord.ui import View, button, Button, Select
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

class RecentMatchesPaginatorView(View):
    def __init__(self, pages: list[discord.Embed], all_matches_data: list):
        super().__init__(timeout=180)
        self.pages = pages
        self.all_matches_data = all_matches_data
        self.current_page = 0
        self.page_size = 5
        
        self.add_item(self.create_select_menu())
        
        self.update_buttons()

    def update_buttons(self):
        self.children[0].disabled = (self.current_page == 0)
        self.children[1].disabled = (self.current_page == len(self.pages) - 1)

    def get_current_page_data(self) -> list:
        start = self.current_page * self.page_size
        end = start + self.page_size
        return self.all_matches_data[start:end]

    def create_select_menu(self) -> Select:
        options = []
        current_page_data = self.get_current_page_data()
        
        if not current_page_data:
            return Select(placeholder="No data available", options=[])

        for i, row in enumerate(current_page_data):
            match = dict(row)
            match_id = str(match.get('match_id'))
            gametype = match.get('gametype_name')
            rating = int(match.get('rating'))
            
            options.append(
                discord.SelectOption(
                    label=f"Match {self.current_page * self.page_size + i + 1}: {gametype}",
                    description=f"Rating: {rating} | ID: {match_id}",
                    value=match_id
                )
            )
        
        select = Select(
            placeholder="Select a match ID to copy...",
            options=options,
            min_values=1,
            max_values=1,
            custom_id="match_select_menu"
        )
        select.callback = self.select_callback
        return select

    async def select_callback(self, interaction: discord.Interaction):
        selected_id = interaction.data['values'][0]
        await interaction.response.send_message(f"{selected_id}", ephemeral=True)
    
    @button(label="Previous", style=discord.ButtonStyle.secondary, custom_id="previous_button")
    async def previous_page_button(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            self.children[-1] = self.create_select_menu()
            await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)
        else:
            await interaction.response.defer()

    @button(label="Next", style=discord.ButtonStyle.secondary, custom_id="next_button")
    async def next_page_button(self, interaction: discord.Interaction, button: Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.update_buttons()
            self.children[-1] = self.create_select_menu()
            await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)
        else:
            await interaction.response.defer()