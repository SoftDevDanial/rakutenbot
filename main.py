import botMethods as botmethods

bot = botmethods.bot()

# Fill this Eg. bot.login("username" , "password")
bot.login()
bot.search_symbol("JCY")
bot.check_status()
bot.off()