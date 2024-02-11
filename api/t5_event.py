# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# from transformers import T5ForConditionalGeneration, T5Tokenizer

# model_path = "path/to/your/saved/model"
# model = T5ForConditionalGeneration.from_pretrained(model_path)
# tokenizer = T5Tokenizer.from_pretrained(model_path)


# def run_event_model_sync(input_text):
#     inputs = tokenizer.encode(
#         input_text, return_tensors="pt", max_length=512, truncation=True)
#     outputs = model.generate(inputs, max_length=80, min_length=20,
#                              length_penalty=2.0, num_beams=4, early_stopping=True)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)


# executor = ThreadPoolExecutor(max_workers=1)


# async def run_event_model_async(input_text):
#     loop = asyncio.get_event_loop()
#     result = await loop.run_in_executor(executor, run_event_model_sync, input_text)
#     return result

# #     summary = await run_model_async(input_text)
