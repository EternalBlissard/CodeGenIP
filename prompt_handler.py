from prompts.reasoner_prompt import getReasonerSystemPrompt
from prompts.test_case_generator_prompt import getTestCaseGeneratorSystemPrompt
from prompts.test_case_validator_prompt import getTestValidatorGeneratorSystemPrompt
from prompts.code_generator_prompt import getCodeGeneratorSystemPrompt
from prompts.get_reply_from_qwen import qwen_reply

def handle_reasoner_prompt(user_prompt,temperature=0.5,max_tokens=1024, top_p=0.7):
    messages = [
    { "role":"system", "content":getReasonerSystemPrompt()},
	{ "role": "user", "content": user_prompt}
    ]
    return qwen_reply(temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    messages=messages)

def handle_code_generator_prompt(user_prompt,temperature=0.5,max_tokens=1024, top_p=0.7):
    messages = [
    { "role":"system", "content":getCodeGeneratorSystemPrompt()},
	{ "role": "user", "content": user_prompt}
    ]
    return qwen_reply(temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    messages=messages)

def handle_test_case_generator_prompt(user_prompt,temperature=0.5,max_tokens=1024, top_p=0.7):
    messages = [
    { "role":"system", "content": getTestCaseGeneratorSystemPrompt()},
	{ "role": "user", "content": user_prompt}
    ]
    return qwen_reply(temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    messages=messages)

def handle_test_validator_prompt(user_prompt,temperature=0.5,max_tokens=1024, top_p=0.7):
    messages = [
    { "role":"system", "content": getTestValidatorGeneratorSystemPrompt()},
	{ "role": "user", "content": user_prompt}
    ]
    return qwen_reply(temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    messages=messages)



