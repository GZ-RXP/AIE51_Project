from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

model_name = "Qwen2.5-0.5B-Instruct-train2"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def get_sentiment(text):
    """
        调用大模型根据输入的文本生成诊断报告
    """
    sys_prompt = """
    你是一个医生问诊助手，请根据医生与患者的对话，总结生成一个简短的医疗报告！
    生成诊断报告的例子如下：
    主   诉: 稀便，便中有粘液。
    现 病 史: 患儿出现稀便，每天大便次数为四五次。
    辅助检查: 暂缺。
    既 往 史: 不详。
    诊    断: 消化不良。
    建    议: 思密达，妈咪爱，粪便常规检查。
    """
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": text}
    ]
    # 将对话转化为模型可处理的格式
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response