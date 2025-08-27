from discord.ext import commands
import discord

MAX_FIELD = 1024
MAX_CMD_HELP = 200

def safe_truncate(s: str, limit: int):
    if s is None:
        return "No description"
    s = str(s).strip()
    return s if len(s) <= limit else s[:limit-1] + "…"

class HelpCog(commands.Cog):
    """Custom help command (use: !help, !help <cog|command>)"""

    def __init__(self, bot):
        self.bot = bot

    def _short_help(self, cmd: commands.Command):
        return cmd.help or cmd.short_doc or "No description"

    def _command_signature(self, ctx, cmd: commands.Command):
        prefix = ctx.prefix or "!"
        sig = cmd.signature or ""
        return f"`{prefix}{cmd.qualified_name} {sig}`".strip()

    @commands.command(name="help")
    async def help_command(self, ctx, *, query: str = None):
        """
        Usage:
         - !help
         - !help player
         - !help player avg
        """
        if not query:
            embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())
            for cog_name, cog in self.bot.cogs.items():
                cmds = [c for c in cog.get_commands() if not c.hidden]
                if not cmds:
                    continue
                lines = []
                for cmd in cmds:
                    lines.append(f"**{cmd.name}** — {safe_truncate(self._short_help(cmd), MAX_CMD_HELP)}")
                value = "\n".join(lines)
                embed.add_field(name=cog_name, value=safe_truncate(value, MAX_FIELD), inline=False)
            others = [c for c in self.bot.walk_commands() if not c.cog_name and not c.hidden]
            if others:
                lines = []
                listed = set()
                for cmd in others:
                    if cmd.name in listed:
                        continue
                    lines.append(f"**{cmd.name}** — {safe_truncate(self._short_help(cmd), MAX_CMD_HELP)}")
                    listed.add(cmd.name)
                embed.add_field(name="No Category", value=safe_truncate("\n".join(lines), MAX_FIELD), inline=False)

            await ctx.send(embed=embed)
            return

        q = query.strip()
        parts = q.split()
        if len(parts) > 1:
            maybe_cmd_name = " ".join(parts)
        else:
            maybe_cmd_name = parts[0]

        cmd = self.bot.get_command(maybe_cmd_name)
        if cmd is None:
            if len(parts) >= 2:
                joined = f"{parts[0]} {parts[1]}"
                cmd = self.bot.get_command(joined)
        if cmd:
            embed = discord.Embed(title=f"Help: {cmd.qualified_name}", description=safe_truncate(cmd.help or cmd.short_doc or "No description", MAX_FIELD), color=discord.Color.green())
            embed.add_field(name="Usage", value=self._command_signature(ctx, cmd), inline=False)

            if isinstance(cmd, commands.Group):
                if cmd.commands:
                    lines = []
                    for sub in cmd.commands:
                        if sub.hidden:
                            continue
                        sig = self._command_signature(ctx, sub)
                        lines.append(f"**{sig}**\n{safe_truncate(sub.help or sub.short_doc or 'No description', MAX_CMD_HELP)}")
                    embed.add_field(name="Subcommands", value=safe_truncate("\n\n".join(lines), MAX_FIELD), inline=False)
                else:
                    embed.add_field(name="Subcommands", value="This command group has no subcommands.", inline=False)

            await ctx.send(embed=embed)
            return

        cog = None
        for name, c in self.bot.cogs.items():
            if name.lower() == q.lower() or getattr(c, "__doc__", "").strip().lower().startswith(q.lower()):
                cog = c
                cog_name = name
                break

        if cog:
            embed = discord.Embed(title=f"{cog_name} Commands", description=safe_truncate(cog.__doc__ or "No description", MAX_FIELD), color=discord.Color.blue())
            lines = []
            for cmd in cog.get_commands():
                if cmd.hidden:
                    continue
                if isinstance(cmd, commands.Group):
                    sublines = []
                    for sub in cmd.commands:
                        if sub.hidden:
                            continue
                        sublines.append(f"  • **{sub.name}** — {safe_truncate(sub.help or sub.short_doc or 'No description', MAX_CMD_HELP)}")
                    group_block = f"**{cmd.name}** — {safe_truncate(cmd.help or cmd.short_doc or 'No description', MAX_CMD_HELP)}\n" + "\n".join(sublines)
                    lines.append(group_block)
                else:
                    lines.append(f"**{cmd.name}** — {safe_truncate(cmd.help or cmd.short_doc or 'No description', MAX_CMD_HELP)}")

            embed.add_field(name="Commands", value=safe_truncate("\n\n".join(lines), MAX_FIELD), inline=False)
            await ctx.send(embed=embed)
            return

        await ctx.send(f"No help found for `{q}`. Try `!help` to list commands.")

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
