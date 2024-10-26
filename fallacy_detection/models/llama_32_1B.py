from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
    {"role": "you are an expert in Logic and a critical thinker.",
     "content": "Can you explain what is a logical fallacy and give me some exmaples and categories?"},
]
pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-3B-Instruct", max_length=2048, device=0)
out = pipe(messages)
print(out)


# from transformers import AutoTokenizer, AutoModelForCausalLM

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")