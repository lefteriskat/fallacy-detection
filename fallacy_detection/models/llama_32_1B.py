from transformers import pipeline
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, AutoTokenizer, LlamaModel

from accelerate import Accelerator

print(torch.cuda.is_available())  # Should return True
print(torch.cuda.current_device())  # Should output 0 if using the first GPU

accelerator = Accelerator()
device = accelerator.device
print(device)
# messages = [
#     {"role": "user", "content": "Who are you?"},
#     {
#         "role": "you are an expert in Logic and a critical thinker.",
#         "content": "Can you explain what is a logical fallacy and give me some exmaples and categories?",
#     },
# ]
# pipe = pipeline(
#     "text-generation",
#     model="meta-llama/Llama-3.2-3B-Instruct",
#     max_length=2048,
#     device=0,
#     token="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",
# )


# out = pipe(messages)


model = LlamaForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B-Instruct",
    token="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",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Llama-3.2-3B-Instruct",
    token="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",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
prompt = "What is a logical fallacy?"
inputs = tokenizer(prompt, return_tensors="pt")
input_ids = inputs.input_ids.to(device)
attention_mask = inputs.attention_mask.to(device)

model.eval()
# Generate
with torch.no_grad():
    generate_ids = model.generate(input_ids, attention_mask=attention_mask, max_new_tokens=1024)
out = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)

print(out)
