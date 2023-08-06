# -*- coding: utf-8 -*-

# 参考：
# https://www.bilibili.com/read/cv21728710
# https://blog.csdn.net/hekaiyou/article/details/128303729


import os
import openai
from dramkit.iotools import load_yml
from dramkit.gentools import isnull, try_repeat_run


# API_KEY = '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'
API_KEY = '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'


QUIT_WORDS = ['quit', 'bye', 'good bye', 'goodbye', '拜拜', '再见']


def get_api_key():
    fcfg = os.path.join(os.path.dirname(__file__), 'config.yml')
    if os.path.exists(fcfg):
        cfg = load_yml(fcfg)
    else:
        cfg = {}
    if 'api_key' in cfg:
        return cfg['api_key']
    else:
        return API_KEY
    
    
API_KEY_DEFAULT = get_api_key()


@try_repeat_run(2)
def chat(prompt, api_key=None):
    '''
    单句对话
    返回(True/False, 回答内容/错误信息)
    '''
    if isnull(api_key):
        api_key = API_KEY_DEFAULT
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.7,
            max_tokens=2500,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']
            )
        answer = response['choices'][0]['text'].strip()
        return True, answer
    except Exception as exc:
        return False, exc.error.to_dict()


def chat_con(api_key=None):
    '''连续对话'''
    print('Yon can input `quit` to stop the conversation.')
    text = '' # 保存上文环境
    turns = [] # 保存连续对话记录
    while True: # 能够连续提问
        question = input('Please input your question:\n')
        if len(question.strip()) == 0:
            # 如果输入为空，提醒输入问题
            print('Please input your question:')
        # 如果输入为'quit'，程序终止
        elif question.lower() in QUIT_WORDS:
            print('\nAI: See you next time!')
            return turns, None
        else:
            prompt = text + '\nHuman: ' + question
            suscess, result = chat(prompt, api_key=api_key)
            if not suscess:
                return turns, result
            turns += [question] + [result] # 只有这样迭代才能连续提问理解上下文
            print('\nAI answer:\n' + result)
            # 为了防止超过字数限制程序会爆掉，限制保留的对话次数
            if len(turns) <= 10:
                text = '\n'.join(turns)
            else:
                text = '\n'.join(turns[-10:])
                
                
class OpenAIChat(object):
    
    def __init__(self, api_key=None):
        self.api_key = api_key if not isnull(api_key) else API_KEY_DEFAULT
        self.text = ''
        self.turns = []
        
    def chat(self, question, api_key=None):
        # 如果输入为空或'quit'，直接返回
        if len(question.strip()) == 0:
            print('AI: No correct question detected!')
            return 'No correct question detected!', {'error_info': 'No correct question detected!'}
        elif question.lower() in QUIT_WORDS:
            print('AI: See you next time!')
            return 'See you next time!', None
        else:
            prompt = self.text + '\nHuman: ' + question
            api_key_ = self.api_key if isnull(api_key) else api_key
            suscess, result = chat(prompt, api_key=api_key_)
            if not suscess:
                return '', result
            self.turns += [question] + [result]
            if len(self.turns) <= 10:
                self.text = '\n'.join(self.turns)
            else:
                self.text = '\n'.join(self.turns[-10:])
            return result, None
                
                
if __name__ == '__main__':
    # turns, e = chat_con()
    chater = OpenAIChat()
    
    
    
    
    
    
    
    
    
    
    