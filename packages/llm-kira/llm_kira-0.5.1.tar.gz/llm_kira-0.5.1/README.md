# llm-kira

A refactored version of the `openai-kira` specification. Use redis or a file database.

Building ChatBot with LLMs.Using `async` requests.

> Contributors welcomed.

## Features

* safely cut context
* usage
* async request api / curl
* multi-Api Key load
* self-design callback

## Basic Use

`pip install -U llm-kira`

**Init**

```python
import llm_kira

llm_kira.setting.redisSetting = llm_kira.setting.RedisConfig(host="localhost",
                                                             port=6379,
                                                             db=0,
                                                             password=None)
llm_kira.setting.dbFile = "client_memory.db"
llm_kira.setting.proxyUrl = None  # "127.0.0.1"

# Plugin
llm_kira.setting.webServerUrlFilter = False
llm_kira.setting.webServerStopSentence = ["广告", "营销号"]  # 有默认值
```

## Demo

**More examples of use in `test/test.py`.**

Take `openai` as an example

```python
import asyncio
import random
import llm_kira
from llm_kira.client import Optimizer
from llm_kira.client.types import PromptItem
from llm_kira.client.llms.openai import OpenAiParam
from typing import List

openaiApiKey = ["key1", "key2"]
openaiApiKey: List[str]

receiver = llm_kira.client
conversation = receiver.Conversation(
    start_name="Human:",
    restart_name="AI:",
    conversation_id=10093,  # random.randint(1, 10000000),
)

llm = llm_kira.client.llms.OpenAi(
    profile=conversation,
    api_key=openaiApiKey,
    token_limit=3700,
    auto_penalty=False,
    call_func=None,
)

mem = receiver.MemoryManager(profile=conversation)
chat_client = receiver.ChatBot(profile=conversation,
                               llm_model=llm
                               )

async def chat():
    promptManager = llm_kira.creator.PromptEngine(profile=conversation,
                                                  connect_words="\n",
                                                  memory_manger=mem,
                                                  llm_model=llm,
                                                  description="这是一段对话",
                                                  reference_ratio=0.5,
                                                  forget_words=["忘掉对话"],
                                                  optimizer=Optimizer.SinglePoint,
                                                  )
    promptManager.insert_prompt(prompt=PromptItem(start=conversation.start_name, text=input("TestPrompt:")))
    response = await chat_client.predict(
        prompt=promptManager,
        llm_param=OpenAiParam(model_name="text-davinci-003", temperature=0.8, presence_penalty=0.1, n=1, best_of=1),
        predict_tokens=1000,
    )
    print(f"id {response.conversation_id}")
    print(f"ask {response.ask}")
    print(f"reply {response.reply}")
    print(f"usage:{response.llm.usage}")
    print(f"usage:{response.llm.raw}")
    print(f"---{response.llm.time}---")

    promptManager.clean(clean_prompt=True,clean_knowledge=False,clean_memory=False)
    promptManager.insert_prompt(prompt=PromptItem(start=conversation.start_name, text='今天天气怎么样'))
    response = await chat_client.predict(llm_param=OpenAiParam(model_name="text-davinci-003"),
                                         prompt=promptManager,
                                         predict_tokens=500,
                                         # parse_reply=None
                                         )
    _info = "parse_reply 函数回调会处理 llm 的回复字段，比如 list 等，传入list，传出 str 的回复。必须是 str。"
    _info2 = "The parse_reply function callback handles the reply fields of llm, such as list, etc. Pass in list and pass out str for the reply."
    print(f"id {response.conversation_id}")
    print(f"ask {response.ask}")
    print(f"reply {response.reply}")
    print(f"usage:{response.llm.usage}")
    print(f"usage:{response.llm.raw}")
    print(f"---{response.llm.time}---")


asyncio.run(chat())
```

## Frame

```
├── client
│      ├── agent.py  //profile class
│      ├── anchor.py // client etc.
│      ├── enhance.py // web search etc.
│      ├── __init__.py
│      ├── llm.py // llm func.
│      ├── module  // plugin for enhance
│      ├── Optimizer.py // memory Optimizer (cutter
│      ├── pot.py // test cache
│      ├── test_module.py // test plugin
│      ├── text_analysis_tools // nlp support
│      ├── types.py // data class
│      └── vocab.json // cache?
├── __init__.py
├── openai  // func
│      ├── api // data
│      ├── __init__.py
│      └── resouce  // func
├── requirements.txt
└── utils  // utils... tools...
    ├── chat.py
    ├── data.py
    ├── fatlangdetect //lang detect
    ├── langdetect
    ├── network.py
    └── setting.py

```
