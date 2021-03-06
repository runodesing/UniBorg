"""Count Number of Files in a Chat
Original Module Credits: https://t.me/UniBorg/127"""
from uniborg.util import admin_cmd, humanbytes, parse_pre, yaml_format


@borg.on(admin_cmd(pattern="filecount ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    entity = event.chat_id
    input_str = event.pattern_match.group(1)
    if input_str:
        entity = input_str
    status_message = await event.reply(
        "... this might take some time "
        "depending on the number of messages "
        "in the chat ..."
    )
    mus = 0
    hmm = {}
    async for message in event.client.iter_messages(
        entity=entity,
        limit=None
    ):
        if message and message.file:
            if message.file.mime_type not in hmm:
                hmm[message.file.mime_type] = 0
            hmm[message.file.mime_type] += message.file.size
    hnm = {key: humanbytes(hmm[key]) for key in hmm}
    await status_message.edit(
        yaml_format(hnm),
        parse_mode=parse_pre
    )
