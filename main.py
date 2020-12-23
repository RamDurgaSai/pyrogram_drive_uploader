from pyrogram import Client, filters
import os, threading
from pyrogram.handlers import MessageHandler
from upload_drive import Upload


class Pyrogram_Application():
    # A Group which has files to upload
    zipvy = "ftsihsydi"

    def __init__(self):
        self.uploader = Upload(call_back=self.reply)
        self.uploader.auth()
        api_id = 1681659
        api_hash = "52206d87f2f7574e070ed39a17af6b2d"
        self.app = Client("my_account", api_id=api_id, api_hash=api_hash)
        self.app.add_handler(MessageHandler(self.main, filters=filters.chat(self.zipvy) & filters.document))
        # uploader = Upload(app, message, upload_to, drive, chat_id='upload_to_drive')
        self.app.run()

    def main(self, client, message):
        self.message = message
        self.reply_message = self.message.reply_text(text='Downloading Started...Plz Wait')
        self.message_id = self.reply_message.message_id
        # Download zip Now
        self.zip_path = self.download_media(message=message)

        if not os.path.isfile(self.zip_path):
            self.reply("Zip is not downloaded May be  Message does not contain any downloadable media")
            return
        else:
            self.reply("Download finished uploading Now please wait")
            self.uploader.set_zip_location(self.zip_path)
        try:
            self.uploader.upload()
            self.clear()
        except Exception as e :
            self.reply(str(e))




    def download_media(self, message):

        try:
            zip_location = self.app.download_media(message, block=True, )
            return zip_location
        except:
            return None

    def reply(self, text):
        self.app.edit_message_text(chat_id=self.zipvy, text=text,
                                   message_id=self.message_id)

    def clear(self):

        try:
            if os.path.isfile(self.zip_path):
                os.remove(self.zip_path)
                self.reply("Uploaded to Google drive  .... Now U can send new Task")

        except:
            self.reply("Unable to delete uploaded files ")


if __name__ == '__main__':
    pyrogram_application = Pyrogram_Application()
