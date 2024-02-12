# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# from transformers import pipeline


# # Initialize the summarizer
# summarizer = pipeline("summarization", model="lidiya/bart-large-xsum-samsum")

# # Create a ThreadPoolExecutor
# executor = ThreadPoolExecutor(max_workers=1)


# async def async_summarize_chat(chat_log):
#     loop = asyncio.get_event_loop()
#     # Run the summarizer in a background thread
#     processed = await loop.run_in_executor(executor, lambda: summarizer(chat_log))
#     return processed[0]["summary_text"]
