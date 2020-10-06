"""**Know Your UniBorg**
◇ list of all loaded plugins
◆ `.helpme`\n
◇ to know Data Center
◆ `.dc`\n
◇ powered by
◆ `.config`\n
◇ to know syntax
◆ `.syntax` <plugin name>
"""
import logging
import shutil
import sys
import time

from sample_config import Config
from telethon import __version__, events, functions


@borg.on(slitu.admin_cmd(pattern="helpme ?(.*)", allow_sudo=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    splugin_name = event.pattern_match.group(1)
    if splugin_name in borg._plugins:
        s_help_string = borg._plugins[splugin_name].__doc__
    else:
        s_help_string = ""
    _, check_sgnirts = check_data_base_heal_th()

    current_run_time = slitu.time_formatter((time.time() - BOT_START_TIME))
    total, used, free = shutil.disk_usage("/")
    total = slitu.humanbytes(total)
    used = slitu.humanbytes(used)
    free = slitu.humanbytes(free)

    help_string = "@UniBorg\n"
    help_string += f"✅ **UpTime** `{current_run_time}`\n"
    help_string += f"✅ **Python** `{sys.version}`\n"
    help_string += f"✅ **Telethon** `{__version__}`\n"
    help_string += f"{check_sgnirts} **Database**\n"
    help_string += f"**Total Disk Space**: `{total}`\n"
    help_string += f"**Used Disk Space**: `{used}`\n"
    help_string += f"**Free Disk Space**: `{free}`\n\n"
    help_string += f"UserBot Forked from https://github.com/muhammedfurkan/uniborg"
    borg._iiqsixfourstore[str(event.chat_id)] = {}
    borg._iiqsixfourstore[
        str(event.chat_id)
    ][
        str(event.id)
    ] = help_string + "\n\n" + s_help_string
    tgbotusername = Config.TG_BOT_USER_NAME_BF_HER  # pylint:disable=E0602
    if tgbotusername is not None:
        results = await borg.inline_query(
            tgbotusername,
            help_string + "\n\n" + s_help_string
        )
        await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
    else:
        await event.reply(
            help_string + "\n\n" + s_help_string,
            parse_mode="html"
        )

    await event.delete()


@borg.on(slitu.admin_cmd(pattern="dc"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(result.stringify())


@borg.on(slitu.admin_cmd(pattern="config"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await event.client(functions.help.GetConfigRequest())  # pylint:disable=E0602
    result = result.stringify()
    logger.info(result)
    await event.edit("""Telethon UserBot powered by @UniBorg""")


@borg.on(slitu.admin_cmd(pattern="syntax (.*)"))
async def _(event):
    if event.fwd_from:
        return
    plugin_name = event.pattern_match.group(1)
    if plugin_name in borg._plugins:
        help_string = borg._plugins[plugin_name].__doc__
        unload_string = f"Use `.unload {plugin_name}` to remove this plugin.\n           © @UniBorg"
        if help_string:
            plugin_syntax = f"Syntax for plugin **{plugin_name}**:\n\n{help_string}\n{unload_string}"
        else:
            plugin_syntax = f"No DOCSTRING has been setup for {plugin_name} plugin."
    else:
        plugin_syntax = "Enter valid **Plugin** name.\nDo `.exec ls stdplugins` or `.helpme` to get list of valid plugin names."
    await event.edit(plugin_syntax)


def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "❌"

    if not Config.DB_URI:
        return is_database_working, output

    from sql_helpers import SESSION

    try:
        # to check database we will execute raw query
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"❌ {str(e)}"
        is_database_working = False
    else:
        output = "✅"
        is_database_working = True

    return is_database_working, output
