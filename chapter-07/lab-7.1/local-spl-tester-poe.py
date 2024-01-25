#!/usr/bin/env python3
import asyncio, os, argparse, warnings
import fastapi_poe as fp

api_key = os.getenv('POE_API')

#runtime arguments
parser = argparse.ArgumentParser()
parser.add_argument('-log', type=str, help='/path/to/testlog.log')
parser.add_argument('-spl', type=str, help='/path/to/detection.spl')
args = parser.parse_args()

if not args.log:
    print('Please add -log </path/to/logfile.log>')
    exit()
if not args.spl:
    print('Please add -spl </path/to/detection.spl>')

#need to use async because bot will have multi-line outputs that need to complete
#https://developer.poe.com/server-bots/accessing-other-bots-on-poe
async def get_responses(api_key, messages):
    response = ""
    async for partial in fp.get_bot_response(messages=messages,
                                             #bot_name="<YOUR-PUBLIC-BOT-NAME>",
                                             #bot_name="Claude-2-100k",
                                             bot_name="Claude-Instant",
                                             api_key=api_key,
                                             temperature=0.15):
        if isinstance(partial, fp.PartialResponse) and partial.text:
            response += partial.text

    return response

#pull details from files and construct message
log_path = args.log
spl_path = args.spl

#forgot about overloads :)
log_file = open(log_path, 'r').read()
spl_file = open(spl_path, 'r').read()
prompt_file = open('prompt.md', 'r').read()

#construct the prompt without fstrings 
prompt_text = prompt_file + '\n ## Sample Log \n' + log_file + '\n ## Correlation Search SPL \n' + spl_file
#print(prompt_text)

#good practice
log_file.close()
spl_file.close()
prompt_file.close()

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

