#
import requests
from pyrogram import filters

from megumin import megux


@megux.on_message(filters.command("github"))
async def github_(client, message):
    username = " ".join(message.text.split()[1:])
    if not username:
        await message.reply("`Pesquisar o vento?`")
        return
    url = "https://api.github.com/users/{}".format(username)
    res = requests.get(url)
    if res.status_code == 200:
        msg = await message.reply("`Buscando informaΓ§Γ΅es no gitgub...`")
        data = res.json()
        photo = data["avatar_url"]
        if data["bio"]:
            data["bio"] = data["bio"].strip()
        repos = []
        sec_res = requests.get(data["repos_url"])
        if sec_res.status_code == 200:
            limit = int(5)
            for repo in sec_res.json():
                repos.append(f"[{repo['name']}]({repo['html_url']})")
                limit -= 1
                if limit == 0:
                    break
        template = """
\bπ€ **Name** : [{name}]({html_url})
π§ **Type** : `{type}`
π’ **Company** : `{company}`
π­ **Blog** : {blog}
π **Location** : `{location}`
π **Bio** : __{bio}__
β€οΈ **Followers** : `{followers}`
π **Following** : `{following}`
π **Public Repos** : `{public_repos}`
π **Public Gists** : `{public_gists}`
π **Profile Created** : `{created_at}`
βοΈ **Profile Updated** : `{updated_at}`\n""".format(
            **data
        )
        if repos:
            template += "π **Some Repos** : " + " | ".join(repos)
        await message.reply_photo(
            caption=template,
            photo=photo,
            disable_notification=True,
        )
        await msg.delete()
    else:
        await message.edit("__No user found with__ `{}` username!".format(username))
