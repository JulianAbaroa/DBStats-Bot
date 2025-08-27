from discord.ext import commands
import discord

MAX_FIELD_LEN = 1024

def safe_truncate(s: str, limit: int = MAX_FIELD_LEN) -> str:
    if s is None:
        return "No description"
    s = str(s).strip()
    if len(s) <= limit:
        return s
    return s[: limit - 1] + "…"

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
            if not commands_list:
                continue
            name = cog.qualified_name if cog else "No Category"
            lines = []
            for cmd in commands_list:
                lines.append(f"**{cmd.name}** — {safe_truncate(cmd.help or cmd.short_doc or 'No description', 200)}")
            value = "\n".join(lines)
            embed.add_field(name=name, value=safe_truncate(value), inline=False)

        await ctx.send(embed=embed)

    async def send_cog_help(self, cog):
        ctx = self.context
        title = f"{cog.qualified_name} Commands"
        description = cog.__doc__ or "No description"
        embed = discord.Embed(title=title, description=safe_truncate(description), color=discord.Color.green())

        lines = []
        for cmd in cog.get_commands():
            if isinstance(cmd, commands.Group):
                sublines = []
                for sub in cmd.commands:
                    sublines.append(f"  • **{sub.name}** — {safe_truncate(sub.help or 'No description', 150)}")
                group_block = f"**{cmd.name}** — {safe_truncate(cmd.help or 'No description', 150)}\n" + "\n".join(sublines)
                lines.append(group_block)
            else:
                lines.append(f"**{cmd.name}** — {safe_truncate(cmd.help or 'No description', 200)}")

        if lines:
            value = "\n\n".join(lines)
            embed.add_field(name="Commands", value=safe_truncate(value), inline=False)
        else:
            embed.add_field(name="Commands", value="No commands found.", inline=False)

        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        """
        If command is a Group, display its subcommands and their helps.
        Otherwise display normal help.
        """
        ctx = self.context
        title = f"Help: {command.qualified_name}"
        description = command.help or command.description or command.short_doc or "No description"
        embed = discord.Embed(title=title, description=safe_truncate(description), color=discord.Color.green())

        if isinstance(command, commands.Group):
            if command.commands:
                lines = []
                for sub in command.commands:
                    sig = self.get_command_signature(sub)
                    lines.append(f"**{sig}**\n{sub.help or 'No description'}")
                embed.add_field(name="Subcommands", value=safe_truncate("\n\n".join(lines)), inline=False)
            else:
                embed.add_field(name="Subcommands", value="This command group has no subcommands.", inline=False)
        else:
            embed.add_field(name="Usage", value=self.get_command_signature(command), inline=False)

        await ctx.send(embed=embed)