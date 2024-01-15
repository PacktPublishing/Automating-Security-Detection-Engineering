#!/usr/bin/env python3
import asyncio, os, feedparser
import fastapi_poe as fp
from datetime import datetime, timedelta

api_key = os.getenv('POE_API')

async def get_responses(api_key, url):
    response = ""
    # Using f-strings allows positioning token replacements
    message = fp.ProtocolMessage(role="user", content=(
        f"### Context\n"
        f"You are a detection engineer bot that analyzes cybersecurty inputs that creates code, parsed outputs, and signatures for tools like SIEM, EDR, NIDS, CNAPP.\n"
        f"You are also a bot that ensures that the requirements section is never skipped or missed.\n"
        f"## Requirements\n"
        f"- Do not include unnecessary statements in your response, only code.\n"
        f"- Do not include any explanations in your responses.\n"
        f"- Never fabricate or provide untrue details that impact functionality.\n"
        f"- Do not make mistakes. Always validate your response to work.\n"
        f"- Seek example logs and official documentations on the web to use in your validation.\n"
        f"## Request\n"
        f"Provide a response with the following requirements:\n"
        f"- The attached contents are from {url}. Parse accordingly.\n"
        f"- Analyze the parsed contents to find indicators of compromise patterns. \n"
        f"- Create a list of file hashes and process syntaxes to look for. \n"
        f"- From the the output, generate a useful Splunk SPL correlation search using Splunk Enteprise Securitys standard data models and CIM compliant"
    ))

    #wrap create a message with an attachment
    #https://developer.poe.com/server-bots/enabling-file-upload-for-your-bot
    attachment_url = url #our input
    attachment_name = "attachment.txt"  #any name is fine because its referenced in prompt
    attachment_content_type = "text/plain"  #use mime format
    attachment_message = fp.ProtocolMessage(
        role="user",
        content=f"Attachment: {attachment_url}",
        attachments=[fp.Attachment(url=attachment_url, name=attachment_name, content_type=attachment_content_type)]
        )
    async for partial in fp.get_bot_response(messages=[message, attachment_message],
                                             bot_name="Claude-Instant",
                                             #bot_name="LinkAwareBot",
                                             api_key=api_key,
                                             temperature=0.25):
        if isinstance(partial, fp.PartialResponse) and partial.text:
            response += partial.text
    return response

def get_urls(rssfeed):
    #e.g. https://allinfosecnews.com/feed/" 
    feed = feedparser.parse(rssfeed)
    links = []

    now = datetime.now()
    time_range = timedelta(days=1)

    for entry in feed.entries:
        #have to remove the offset because of striptimes parameters
        entry_date_str = entry.published[:-6]
        entry_date = datetime.strptime(entry_date_str, "%a, %d %b %Y %H:%M:%S")

    if now - entry_date <= time_range:
        links.append(entry.link)
        return links #returns a list to iterate on in main driver

#main driver
if __name__ == "__main__":
    #get fresh -24h urls returns as list type
    fresh_urls = get_urls('https://allinfosecnews.com/feed/')

    #write std out to file too messy in console
    file_handle = open("ai-recommended-spl.txt", "w")

    for url in fresh_urls:
        bot_response = asyncio.run(get_responses(api_key, url))
        print("Writing responses for: " + url)
        file_handle.write(bot_response + "\n")
    
    file_handle.close()
    exit()
