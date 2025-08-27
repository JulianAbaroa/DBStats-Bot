from discord.ext import commands
import discord

MAX_FIELD = 1024
MAX_CMD_HELP = 200
MAX_DESC = 4096

def safe_truncate(s: str, limit: int):
    if s is None:
        return "No description"
    s = str(s).strip()
    return s if len(s) <= limit else s[:limit-1] + "…"

class HelpCommand(commands.Cog):
    """Custom help command (use: !help, !help <cog|command>)"""

    def __init__(self, bot):
        self.bot = bot

    def _short_help(self, cmd: commands.Command):
        return cmd.help or cmd.short_doc or "No description"

    def _command_signature(self, ctx, cmd: commands.Command):
        sig = cmd.signature or ""
        return f"**!{cmd.qualified_name} {sig}**".strip()

    @commands.command(name="help")
    async def help_command(self, ctx, *, query: str = None):
        """
         - !help player
         - !help match
        """
        if not query:
            embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())

            for cog_name, cog in self.bot.cogs.items():
                cmds = [c for c in cog.get_commands() if not c.hidden]
                if not cmds:
                    continue
                lines = []
                for cmd in cmds:
                    lines.append(f"{safe_truncate(self._short_help(cmd), MAX_CMD_HELP)}")
                embed.add_field(name=cog_name, value=safe_truncate("\n".join(lines), MAX_FIELD), inline=False)

            others = [c for c in self.bot.walk_commands() if not c.cog_name and not c.hidden]
            if others:
                lines = []
                listed = set()
                for cmd in others:
                    if cmd.name in listed:
                        continue
                    lines.append(f"{safe_truncate(self._short_help(cmd), MAX_CMD_HELP)}")
                    listed.add(cmd.name)
                embed.add_field(name="No Category", value=safe_truncate("\n".join(lines), MAX_FIELD), inline=False)

            await ctx.send(embed=embed)
            return

        q = query.strip()
        parts = q.split()

        maybe_cmd_name = " ".join(parts) if len(parts) > 1 else parts[0]

        cmd = self.bot.get_command(maybe_cmd_name)
        if cmd is None and len(parts) >= 2:
            joined = f"{parts[0]} {parts[1]}"
            cmd = self.bot.get_command(joined)

        if cmd:
            desc_lines = []
            desc_lines.append(safe_truncate(cmd.help or cmd.short_doc or "No description", MAX_CMD_HELP))
            desc_text = "\n\n".join(desc_lines)
            embed = discord.Embed(description=safe_truncate(desc_text, MAX_DESC), color=discord.Color.green())

            embed.add_field(name="Usage", value=f"**!{cmd.qualified_name} {cmd.signature or ''}**".strip(), inline=False)

            if isinstance(cmd, commands.Group):
                if cmd.commands:
                    sub_lines = []
                    for sub in cmd.commands:
                        if sub.hidden:
                            continue
                        help_text = safe_truncate(sub.help or sub.short_doc or "No description", MAX_CMD_HELP)
                        sub_lines.append(f"**!{sub.qualified_name} {sub.signature or ''}**\n{help_text}")
                    embed.add_field(name="Subcommands", value=safe_truncate("\n\n".join(sub_lines), MAX_FIELD), inline=False)
                else:
                    embed.add_field(name="Subcommands", value="This command group has no subcommands.", inline=False)

            await ctx.send(embed=embed)
            return

        cog = None
        cog_name = None
        for name, c in self.bot.cogs.items():
            if name.lower() == q.lower() or (c.__doc__ and c.__doc__.strip().lower().startswith(q.lower())):
                cog = c
                cog_name = name
                break

        if cog:
            lines = []
            header = safe_truncate(cog.__doc__ or "No description", MAX_CMD_HELP)
            if header:
                lines.append(header)
                lines.append("")

            for cmd in cog.get_commands():
                if cmd.hidden:
                    continue
                if isinstance(cmd, commands.Group):
                    group_help = safe_truncate(cmd.help or cmd.short_doc or "No description", MAX_CMD_HELP)
                    sub_entries = []
                    for sub in cmd.commands:
                        if sub.hidden:
                            continue
                        sub_help = safe_truncate(sub.help or sub.short_doc or "No description", MAX_CMD_HELP)
                        sub_entries.append(f"  • **!{sub.qualified_name} {sub.signature or ''}**: {sub_help}")
                    block = f"**!{cmd.qualified_name} {cmd.signature or ''}**: {group_help}\n" + "\n".join(sub_entries)
                    lines.append(block)
                else:
                    help_text = safe_truncate(cmd.help or cmd.short_doc or "No description", MAX_CMD_HELP)
                    lines.append(f"**!{cmd.qualified_name} {cmd.signature or ''}**: {help_text}")

            full_desc = "\n\n".join(lines)
            embed = discord.Embed(description=safe_truncate(full_desc, MAX_DESC), color=discord.Color.blue())
            await ctx.send(embed=embed)
            return

        await ctx.send(f"No help found for `{q}`. Try `!help` to list commands.")

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))