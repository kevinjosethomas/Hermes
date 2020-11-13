import os
import pytz
import pickle
import discord
from pathlib import Path
from datetime import datetime
from discord.ext import commands, tasks
from googleapiclient.discovery import build


class Email(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            print("Please provide a valid token.pickle with LOGIN CREDENTIALS!")

        self.service = build('gmail', 'v1', credentials=creds)

        self.check_mail.start()

    @tasks.loop(minutes=10)
    async def check_mail(self):
        """Checks for new email every 10 minutes"""

        try:
            try:
                last_email = open(Path("data/last_email.txt"), "r")
                last_email_id = last_email.read()
            except FileNotFoundError:
                last_email_id = None

            results = self.service.users().messages().list(userId='me').execute()
            emails = results.get('messages', [])

            # Latest email is not recorded
            if not last_email_id:
                update_email = open(Path("data/last_email.txt"), "w")
                update_email.write(emails[0]["id"])
                return

            if emails:
                latest_email = self.service.users().messages().get(userId='me', id=emails[0]["id"]).execute()

                # No new emails
                if latest_email["id"] == last_email_id:
                    return

                new_emails = []

                for email in emails[:10]:
                    email_content = self.service.users().messages().get(userId='me', id=email["id"]).execute()

                    if email_content["id"] == last_email_id:
                        break

                    new_emails.append(email_content)

                for email in new_emails[::-1]:

                    headers = email["payload"]["headers"]

                    for header in headers:
                        if header["name"].lower() == "subject":
                            SUBJECT = header["value"]
                        elif header["name"].lower() == "from":
                            FROM = header["value"].replace("<", "``<").replace(">", ">``")

                    description = f"📨 **{SUBJECT}**\n" \
                                f"**From:** {FROM}\n" \
                                f"```{email['snippet'][:924]}```"

                    email_date = datetime.fromtimestamp((int(email["internalDate"]) / 1000), tz=pytz.timezone("America/Toronto"))

                    embed = discord.Embed(
                        description=description,
                        timestamp=email_date,
                        color=self.bot.c.color
                    )

                    await self.bot.me.send(embed=embed)

                    update_email = open(Path("data/last_email.txt"), "w")
                    update_email.write(email["id"])

        except Exception as e:
            print(e)

    @check_mail.before_loop
    async def before_checking_mail(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(Email(bot))
