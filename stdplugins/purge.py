"""Purge your messages without the admins seeing it in Recent Actions"""
import asyncio
import logging
from uniborg.util import admin_cmd, is_read
from telethon import events
import telethon.utils


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)

level = logging.INFO
print(level)


@borg.on(admin_cmd(pattern="purge ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        i = 1
        msgs = []
        from_user = None
        input_str = event.pattern_match.group(1)
        if input_str:
            from_user = await event.client.get_entity(input_str)
            logger.info(from_user)
        async for message in event.client.iter_messages(
            event.chat_id,
            min_id=event.reply_to_msg_id,
            from_user=from_user
        ):
            i += 1
            msgs.append(message)
            if len(msgs) == 100:
                await event.client.delete_messages(event.chat_id, msgs, revoke=True)
                msgs = []
        if len(msgs) <= 100:
            await event.client.delete_messages(event.chat_id, msgs, revoke=True)
            msgs = []
            await event.delete()
        else:
            await event.edit("**PURGE** Failed!")


@borg.on(admin_cmd(pattern="purgme ?(.*)"))
async def purgeme(delme):
    """ For .purgeme, delete x count of your latest message."""
    message = delme.text
    count = int(message[8:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id, from_user='me'):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "`Purge complete!` Purged " + str(count) + " messages.",
    )
    await asyncio.sleep(5)
    await smsg.delete()
    await asyncio.sleep(5)


@borg.on(admin_cmd(pattern="selfd ?(.*) + ?(.*)", outgoing=True))
async def selfdestruct(destroy):
    if not destroy.text[0].isalpha() and destroy.text[0] not in ("/", "#", "@", "!"):
        await destroy.delete()
        message = destroy.pattern_match.group(2)
        counter = destroy.pattern_match.group(1)
        text = message + "\n\n`Bu mesaj " + \
            str(counter) + " saniye sonunda silinecektir.`"

        smsg = await destroy.client.send_message(destroy.chat_id, text)
        await asyncio.sleep(int(counter))
        await smsg.delete()




async def get_target_message(event):
    if event.is_reply and (await event.get_reply_message()).from_id == borg.uid:
        return await event.get_reply_message()
    async for message in borg.iter_messages(
            await event.get_input_chat(), limit=20):
        if message.out:
            return message


async def await_read(chat, message):
    chat = telethon.utils.get_peer_id(chat)

    async def read_filter(read_event):
        return (read_event.chat_id == chat
                and read_event.is_read(message))
    fut = borg.await_event(events.MessageRead(inbox=False), read_filter)

    if await is_read(borg, chat, message):
        fut.cancel()
        return

    await fut


@borg.on(admin_cmd(pattern="(del)(?:ete)?$"))
@borg.on(admin_cmd(pattern="(edit)(?:\s+(.*))?$"))
async def delete(event):
    await event.delete()
    command = event.pattern_match.group(1)
    if command == 'edit':
        text = event.pattern_match.group(2)
        if not text:
            return
    target = await get_target_message(event)
    if target:
        chat = await event.get_input_chat()
        await await_read(chat, target)
        await asyncio.sleep(.5)
        if command == 'edit':
            await borg.edit_message(chat, target, text)
        else:
            await borg.delete_messages(chat, target, revoke=True)
