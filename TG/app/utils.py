import telebot
from jira import JIRA
from redminelib import Redmine

bot = telebot.TeleBot('5444414945:AAE8X9rNiQl7avGoRoknkBxgI-jtAU3nUEo')

jira_options = {'server': 'https://finch1.atlassian.net'}
jira = JIRA(options=jira_options, basic_auth=('kirill200118@gmail.com', 'aeGqCvb2DyzmUA79yxpNDD0C'))


redmine = Redmine('https://task.finch.fm', username='finch-jira-bot', password='LPWmYe2kbB')
