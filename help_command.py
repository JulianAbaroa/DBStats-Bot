from discord.ext import commands
import discord

class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(width=200)

    async def send_bot_help(self, mapping):
        ctx = self.context
        embed = discord.Embed(
            title="Bot Commands",
            color=discord.Color.blue()
        )

        for cog, commands_list in mapping.items():
            if commands_list:
                name = cog.qualified_name if cog else "No Category"
                cmd_list = "\n".join(f"{cmd.name} -> {cmd.help}" for cmd in commands_list)
                embed.add_field(name=name, value=cmd_list, inline=False)

        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        ctx = self.context
        embed = discord.Embed(
            title=f"Help for {command.name}",
            description=command.help or "No description",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    async def send_cog_help(self, cog):
        ctx = self.context
        embed = discord.Embed(
            title=f"{cog.qualified_name} Commands",
            description=getattr(cog, "description", "No description"),
            color=discord.Color.green()
        )

        commands_list = []
        for cmd in cog.get_commands():
            if isinstance(cmd, commands.Group):
                subcmds = "\n".join(f"  {sub.name} -> {sub.help}" for sub in cmd.commands)
                commands_list.append(f"{cmd.name} -> {cmd.help or 'No description'}\n{subcmds}")
            else:
                commands_list.append(f"{cmd.name} -> {cmd.help or 'No description'}")

        embed.add_field(name="Commands", value="\n".join(commands_list), inline=False)
        await ctx.send(embed=embed)
