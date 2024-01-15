#!/usr/bin/env python3
import asyncio, os, argparse
import fastapi_poe as fp

api_key = os.getenv('POE_API')

#runtime arguments
parser = argparse.ArgumentParser()
parser.add_argument('-url', type=str, help='Provide parsable URL of IOAs or IOCs e.g. STIX JSON format or CSV')
args = parser.parse_args()

if not args.url:
    print('Please provide a URL using the -url argument.')
    # e.g. https://www.cisa.gov/sites/default/files/2023-12/AA23-352A-StopRansomware-Play-Ransomware.stix_.json
    exit()

#need to use async because bot will have multi-line outputs that need to complete
#https://developer.poe.com/server-bots/accessing-other-bots-on-poe
async def get_responses(api_key, messages):
    response = ""
    async for partial in fp.get_bot_response(messages=messages,
                                             bot_name="Claude-Instant",
                                             #bot_name="LinkAwareBot",
                                             api_key=api_key,
                                             temperature=0.25):
        if isinstance(partial, fp.PartialResponse) and partial.text:
            response += partial.text

    return response

#using f-strings allows positioning token replacements
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
    f"- The attached contents are from {args.url}. Parse accordingly.\n"
    f"- Analyze the parsed contents to find indicators of compromise patterns. \n"
    f"- Create a list of file hashes and process syntaxes to look for. \n"
    f"- From the the output, generate a useful Splunk SPL correlation search using Splunk Enteprise Securitys standard data models and CIM compliant"
))

#wrap create a message with an attachment
#https://developer.poe.com/server-bots/enabling-file-upload-for-your-bot
attachment_url = args.url #our input
attachment_name = "attachment.txt"  #any name is fine because its referenced in prompt
attachment_content_type = "text/plain"  #use mime format
attachment_message = fp.ProtocolMessage(
    role="user",
    content=f"Attachment: {attachment_url}",
    attachments=[fp.Attachment(url=attachment_url, name=attachment_name, content_type=attachment_content_type)]
)

#main driver
if __name__ == "__main__":
    #event loop response
    bot_response = asyncio.run(get_responses(api_key, [message, attachment_message]))

    print('### BOT ORIGINAL RESPONSE ###')
    print(bot_response)