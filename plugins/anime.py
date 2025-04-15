import json
from calendar import month_name
import aiohttp
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_readable_time(seconds: int) -> str:
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    time_parts = []
    if hours > 0:
        time_parts.append(f"{hours}h")
    if minutes > 0:
        time_parts.append(f"{minutes}m")
    if sec > 0:
        time_parts.append(f"{sec}s")
    return " ".join(time_parts)

media_query = """
query ($id: Int, $idMal: Int, $search: String, $type: MediaType) {
  Media(id: $id, idMal: $idMal, type: $type, search: $search) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    type
    format
    status(version: 2)
    description(asHtml: true)
    startDate {
      year
      month
      day
    }
    endDate {
      year
      month
      day
    }
    season
    seasonYear
    episodes
    duration
    chapters
    volumes
    countryOfOrigin
    source
    hashtag
    trailer {
      id
      site
      thumbnail
    }
    updatedAt
    coverImage {
      large
    }
    bannerImage
    genres
    synonyms
    averageScore
    meanScore
    popularity
    trending
    favourites
    tags {
      name
      description
      rank
    }
    relations {
      edges {
        node {
          id
          title {
            romaji
            english
            native
          }
          format
          status
          source
          averageScore
          siteUrl
        }
        relationType
      }
    }
    characters {
      edges {
        role
        node {
          name {
            full
            native
          }
          siteUrl
        }
      }
    }
    studios {
      nodes {
         name
         siteUrl
      }
    }
    isAdult
    nextAiringEpisode {
      airingAt
      timeUntilAiring
      episode
    }
    airingSchedule {
      edges {
        node {
          airingAt
          timeUntilAiring
          episode
        }
      }
    }
    externalLinks {
      url
      site
    }
    rankings {
      rank
      year
      context
    }
    reviews {
      nodes {
        summary
        rating
        score
        siteUrl
        user {
          name
        }
      }
    }
    siteUrl
  }
}
"""

async def get_media(variables):
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            "https://graphql.anilist.co",
            json={"query": media_query, "variables": variables}
        )
        return await response.read()

def shorten(description, info="anilist.co"):
    ms_g = ""
    if len(description) > 700:
        description = f"{description[:500]}...."
        ms_g += f'\n<strong><blockquote>𝗗𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 :</blockquote></strong> <em><blockquote expandable>{description}</em></blockquote><a href="{info}"><blockquote>Mᴏʀᴇ ɪɴғᴏ</blockquote></a>'
    else:
        ms_g += f"\n<strong><blockquote>𝗗𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 :</blockquote></strong> <em></blockquote expandable>{description}</blockquote></em>"
    return (
        ms_g.replace("<br>", "")
        .replace("</br>", "")
        .replace("<i>", "")
        .replace("</i>", "")
    )

async def handle_media(mesg, media_type):
    search = mesg.text.split(None, 1)
    reply = await mesg.reply("<blockquote>⏳ <i>Pʟᴇᴀsᴇ ᴡᴀɪᴛ ...</i></blockquote>", quote=True)
    if len(search) == 1:
        return await reply.edit(f"<blockquote>⚠️ <b>Gɪᴠᴇ {media_type.capitalize()} Nᴀᴍᴇ ᴘʟᴇᴀsᴇ...</blockquote></b>")
    search = search[1]
    variables = {"search": search, "type": media_type.upper()}
    data = json.loads(await get_media(variables))["data"]
    res = data.get("Media", None)
    if not res:
        return await reply.edit("<blockquote>💢 Nᴏ ʀᴇsᴏᴜʀᴄᴇ ғᴏᴜɴᴅ! [404]</blockquote>")

    msg = f"<b><blockquote>{res['title']['romaji']}</b>(<code>{res['title']['native']}</code>)</blockquote>\n\n<b>Type</b>: {res['format']}\n<b>Status</b>: {res['status']}\n"
    
    if media_type == "anime":
        durasi = get_readable_time(int(res.get("duration", 0) * 60))
        msg += f"<b>Episodes</b>: {res.get('episodes', 'N/A')}\n<b>Duration </b>: {durasi} Per Eps.\n"
    else:
        msg += f"<b>Chapters</b>: {res.get('chapters', 'N/A')}\n<b>Volumes</b>: {res.get('volumes', 'N/A')}\n"

    msg += f"<b>Score</b>: {res.get('averageScore', 'N/A')}%\n<b>Category</b>: <code>"
    for genre in res.get("genres", []):
        msg += f"{genre}, "
    msg = msg.rstrip(", ") + "</code>\n"

    try:
        sd = res["startDate"]
        startdate = f"{month_name[sd['month']]} {sd['day']}, {sd['year']}"
    except:
        startdate = "-"
    msg += f"<b>Start date</b>: <code>{startdate}</code>\n"

    try:
        ed = res["endDate"]
        enddate = f"{month_name[ed['month']]} {ed['day']}, {ed['year']}"
    except:
        enddate = "-"
    msg += f"<b>End date</b>: <code>{enddate}</code>\n"

    msg += "<b>Studios</b>: <code>"
    for studio in res.get("studios", {}).get("nodes", []):
        msg += f"{studio['name']}, "
    msg = msg.rstrip(", ") + "</code>\n"

    info = res.get("siteUrl")
    trailer = res.get("trailer")
    trailer_url = None
    if trailer and trailer.get("site") == "youtube":
        trailer_url = f"https://youtu.be/{trailer['id']}"

    description = res.get("description", "N/A")
    msg += shorten(description, info)

    image = res.get("bannerImage") or res["coverImage"]["large"]
    btn = [[InlineKeyboardButton("Mᴏʀᴇ ɪɴғᴏ ⚡", url=info)]]
    if trailer_url:
        btn[0].append(InlineKeyboardButton("Tʀᴀɪʟᴇʀ 🎬", url=trailer_url))

    try:
        await mesg.reply_photo(image, caption=msg, reply_markup=InlineKeyboardMarkup(btn))
        await reply.delete()
    except:
        msg += f"\n[Image]({image})"
        await reply.edit(msg)

@Client.on_message(filters.command("anime", "/"))
async def anime_handler(client, message):
    await handle_media(message, "anime")

@Client.on_message(filters.command("manga", "/"))
async def manga_handler(client, message):
    await handle_media(message, "manga")

# Main bot runner
if __name__ == "__main__":
    app = Client(
        "anilist_bot",
        api_id=123456,  # Replace with your API ID
        api_hash="your_api_hash_here",  # Replace with your API hash
        bot_token="your_bot_token_here"  # Replace with your Bot token
    )

    app.add_handler(filters.command("anime", "/")(anime_handler))
    app.add_handler(filters.command("manga", "/")(manga_handler))

    app.run()
