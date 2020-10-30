"""Globally Ban users from all the
Group Administrations bots where you are SUDO
Available Commands:
.gban REASON
.ungban REASON"""
import asyncio
import logging

from sample_config import Config
from uniborg.util import admin_cmd

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@borg.on(admin_cmd(pattern="fban ?(.*)"))
async def _(event):
    if Config.G_BAN_LOGGER_GROUP is None:
        await event.edit("ENV VAR is not set. This module will not work.")
        return
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        r_from_id = r.forward.sender_id or r.sender_id if r.forward else r.sender_id
        await event.client.send_message(
            Config.G_BAN_LOGGER_GROUP,
            "!fban {} {}".format(r_from_id, reason)
        )
    else:
        user_id = event.pattern_match.group(1)
        await event.client.send_message(
            Config.G_BAN_LOGGER_GROUP,
            "!fban {}".format(user_id)
        )
        await event.client.send_message(
            entity="PersonalBLBot",
            message="{}".format(user_id)
        )
    await event.delete()


@borg.on(admin_cmd(pattern="unfban ?(.*)"))
async def _(event):
    if Config.G_BAN_LOGGER_GROUP is None:
        await event.edit("ENV VAR is not set. This module will not work.")
        return
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        r_from_id = r.sender_id
        await event.client.send_message(
            Config.G_BAN_LOGGER_GROUP,
            "!unfban {} {}".format(r_from_id, reason)
        )
    else:
        user_id = event.pattern_match.group(1)
        await event.client.send_message(
            Config.G_BAN_LOGGER_GROUP,
            "!unfban {}".format(user_id)
        )
    await event.delete()
