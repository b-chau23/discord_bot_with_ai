import os
import gpt
import claude_antrhopic
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
# load discord bot token
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot Connected Succesfully")

@bot.command()
async def test(ctx):
    claude_antrhopic.write_claude_log("TEST MESSAGE")
    gpt.write_gpt_log("TEST MESSAGE")
    await ctx.send("test good")
    print("test good")

@bot.command()
async def gpt3(ctx, *args):
    args = ' '.join(args)
    output = gpt.get_text("gpt-3.5-turbo-1106", args)
    await send_msg(ctx, output)

@bot.command()
async def gpt4(ctx, *args):
    args = ' '.join(args)
    output = gpt.get_text("gpt-4-1106-preview", args)
    await send_msg(ctx, output)

@bot.command()
async def image(ctx, *args):
    args = ' '.join(args)
    pic = ctx.message.attachments[0].url
    output = gpt.get_image(pic, args)
    await send_msg(ctx, output)
    
@bot.command()
async def create(ctx, *args):
    args = ' '.join(args)
    img_url = gpt.create(args)
    e = discord.Embed(
            url=img_url,
    )
    e.set_thumbnail(url=img_url)
    await ctx.send("Please note image URLs expire after 1 Hour", embed=e)

@bot.command()
async def opus(ctx, *args):
    args = ' '.join(args)
    output = claude_antrhopic.get_text("claude-3-opus-20240229", args)
    await send_msg(ctx, output)

@bot.command()
async def sonnet(ctx, *args):
    output = claude_antrhopic.get_text("claude-3-sonnet-20240229", ' '.join(args))
    await send_msg(ctx, output)

@bot.command()
async def opus_image(ctx, *args):
    pic = ctx.message.attachments[0].url
    output = claude_antrhopic.get_image("claude-3-opus-20240229", ' '.join(args), pic)
    await send_msg(ctx, output)

@bot.command()
async def sonnet_image(ctx, *args):
    pic = ctx.message.attachments[0].url
    output = claude_antrhopic.get_image("claude-3-sonnet-20240229", ' '.join(args), pic)
    await send_msg(ctx, output)

async def send_msg(ctx, message):
    if len(message) > 2000:
        write_temp(message)
        await ctx.send("Output was too long for a Discord message. I've attached a file containing the text:", file=discord.File("temp.txt"))
    else:
        await ctx.send(message)

def write_temp(message):
    with open("discord_bot/temp.txt", "w") as f:
        f.write(message)

if __name__ == "__main__":
    bot.run(TOKEN)