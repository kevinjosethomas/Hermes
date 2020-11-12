from __future__ import print_function

import pickle
import os.path
import discord
from discord.ext import commands
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


class Email(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                
        if not creds or not creds.valid:
            print("Please provide a valid token.pickle with LOGIN CREDENTIALS!")
            exit()

        self.service = build('gmail', 'v1', credentials=creds)


def setup(bot):
    bot.add_cog(Email(bot))
