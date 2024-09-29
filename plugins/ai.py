
Get Answers from Chat GPT

> No need of any API key.
> You can whitelist IP: @aknuserbot
> Bots > Start > Add IP whitelist > Now send your public IP address

• Examples: 
> {i}askold How to send message in telethon

from io import BytesIO

from . import async_searcher, LOGS, ultroid_cmd

@ultroid_cmd(pattern="askold( ([\s\S]*)|$)")
async def chatgpt_old(e):
    query = e.pattern_match.group(2)
    reply = await e.get_reply_message()
    if not query:
        if reply and reply.text:
            query = reply.message
    if not query:
        return await e.eor("Give a Question to ask from ChatGPT")
    not_pro = await e.eor("Generating answer...")
    payloads = {"query": query}
    try:
        response = await async_searcher(
            "https://private-akeno.randydev.my.id/ryuzaki/chatgpt-old",
            post=True,
            json=payloads,
            re_json=True,
            headers = {"Content-Type": "application/json"},
        )
        response = response["randydev"].get("message")
        if len(response + query) < 4080:
            to_edit = (
                f"Query:\n~ {query}\n\nChatGPT:\n~ {response}"
            )
            return await not_pro.edit(to_edit, parse_mode="html")
        with BytesIO(response.encode()) as file:
            file.name = "gpt_response.txt"
            await e.client.send_file(
                e.chat_id,
                file,
                caption=f"{query[:1020]}",
                reply_to=e.reply_to_msg_id
            )
        await not_pro.try_delete()
    except Exception as exc:
        LOGS.exception(exc)
        await not_pro.edit(f"Ran into an Error: \n{exc}" )
        
