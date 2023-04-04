llm_settings = {
    "bloom":"http://172.16.33.2:8080/bloom",
    "chatglm":"http://172.16.23.85:30592/chatglm/ask",
}

def set_llm_settings(llm_name:str, url:str):
    global llm_settings
    llm_settings[llm_name] = url