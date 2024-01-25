#!/usr/bin/env python3
import asyncio, os, argparse, warnings, csv
import fastapi_poe as fp

api_key = os.getenv('POE_API')

#need to use async because bot will have multi-line outputs that need to complete
#https://developer.poe.com/server-bots/accessing-other-bots-on-poe
async def get_responses(api_key, messages):
    response = ""
    async for partial in fp.get_bot_response(messages=messages,
                                             #bot_name="<YOUR-PUBLIC-BOT-NAME>",
                                             bot_name="Claude-2-100k",
                                             #bot_name="Claude-Instant",
                                             api_key=api_key,
                                             temperature=0.15):
        if isinstance(partial, fp.PartialResponse) and partial.text:
            response += partial.text

    return response

#parse buildspec file
buildspec_handle = open('buildspec.csv', 'r')
buildspec_file = csv.reader(buildspec_handle, delimiter=',')
for i in buildspec_file: #csv.reader requires iteration
    log_path = str(i[0]) #get first column
    spl_path = str(i[1]) #get second column

#forgot about overloads :)
log_file = open(log_path, 'r').read()
spl_file = open(spl_path, 'r').read()
prompt_file = open('prompt.md', 'r').read()

#construct the prompt without fstrings 
prompt_text = prompt_file + '\n ## Sample Log \n' + log_file + '\n ## Correlation Search SPL \n' + spl_file
#print(prompt_text)

message = fp.ProtocolMessage(role="user", content=(prompt_text))

#main driver
if __name__ == "__main__":
    #event loop response
    bot_response = asyncio.run(get_responses(api_key, [message]))
    print(bot_response)
    if '[HIGH]' in bot_response:
        print('PASS: AI Evaluation - HIGH')
        exit()
    elif '[MEDIUM]' in bot_response:
        print('CAUTION: AI Evaluation - MEDIUM')
        warnings.warn('CAUTION: AI Evaluation - MEDIUM')
    elif '[LOW]' in bot_response:
        print('FAIL: AI Evaluation - LOW')
        raise ValueError('TEST FAIL: AI Low probability Rating. Please check test log and SPL.')
        exit(1)
    elif '[UNKNOWN]' in bot_response:
        print('FAIL: AI Evaluation - UNKNOWN')
        raise ValueError('TEST FAIL: AI cannot determine detection. Please check test log and SPL.')
        exit(1)