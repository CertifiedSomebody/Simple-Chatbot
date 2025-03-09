import google.generativeai as genai

genai.configure(api_key="AIzaSyA1pvhkv7CkiXM-3WeKEDwY0T0_-gGmx38")

models = genai.list_models()
for model in models:
    print(model.name)
