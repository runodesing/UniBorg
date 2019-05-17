#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy
import os
from PIL import Image
import time

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from sample_config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)




@borg.on_message(pyrogram.Filters.command(["generatecustomthumbnail"]))
def generate_custom_thumbnail(bot, update):
    if update.reply_to_message is not None:
        reply_message = update.reply_to_message
        if reply_message.media_group_id is not None:
            download_location = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/" + str(reply_message.media_group_id) + "/"
            save_final_image = download_location + str(round(time.time())) + ".jpg"
            list_im = os.listdir(download_location)
            if len(list_im) == 2:
                imgs = [ Image.open(download_location + i) for i in list_im ]
                inm_aesph = sorted([(numpy.sum(i.size), i.size) for i in imgs])
                min_shape = inm_aesph[1][1]
                imgs_comb = numpy.hstack(numpy.asarray(i.resize(min_shape)) for i in imgs)
                imgs_comb = Image.fromarray(imgs_comb)
                # combine: https://stackoverflow.com/a/30228789/4723940
                imgs_comb.save(save_final_image)
                # send
                bot.send_photo(
                    chat_id=update.chat.id,
                    photo=save_final_image,
                    caption=Translation.CUSTOM_CAPTION_UL_FILE,
                    reply_to_message_id=update.message_id
                )
            else:
                bot.send_message(
                    chat_id=update.chat.id,
                    text=Translation.ERR_ONLY_TWO_MEDIA_IN_ALBUM,
                    reply_to_message_id=update.message_id
                )
            try:
                [os.remove(download_location + i) for i in list_im ]
                os.remove(download_location)
            except:
                pass
        else:
            bot.send_message(
                chat_id=update.chat.id,
                text=Translation.REPLY_TO_MEDIA_ALBUM_TO_GEN_THUMB,
                reply_to_message_id=update.message_id
            )
    else:
        bot.send_message(
            chat_id=update.chat.id,
            text=Translation.REPLY_TO_MEDIA_ALBUM_TO_GEN_THUMB,
            reply_to_message_id=update.message_id
        )


@borg.on_message(pyrogram.Filters.photo)
def save_photo(bot, update):
        # album is sent
        download_location = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/" + str(update.media_group_id) + "/"
        # create download directory, if not exist
if not os.path.isdir(download_location):
        os.makedirs(download_location)
        bot.download_media(
            message=update,
            file_name=download_location
        )
    else:
        # received single photo
        download_location = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
        bot.download_media(
            message=update,
            file_name=download_location
        )
        bot.send_message(
            chat_id=update.chat.id,
            text=Translation.SAVED_CUSTOM_THUMB_NAIL,
            reply_to_message_id=update.message_id
        )


@borg.on_message(pyrogram.Filters.command(["deletethumbnail"]))
def delete_thumbnail(bot, update):
    download_location = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
    try:
        os.remove(download_location + ".jpg")
        # os.remove(download_location + ".json")
    except:
        pass
    bot.send_message(
        chat_id=update.chat.id,
        text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id
    )
