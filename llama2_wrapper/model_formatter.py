from abc import ABC, abstractmethod

class Formatter(ABC):
    DESCRIPTION = ""
    stop_words = []
    @abstractmethod
    def format_texts(self, system_prompt, chat_history, message):
        pass

class LlamaFormatter(Formatter):
    DESCRIPTION = """
    # llama2-webui
    """
    stop_words = []
    def format_texts(self, system_prompt, chat_history, message):
        texts = [f"[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n"]
        for user_input, response in chat_history:
            texts.append(f"{user_input.strip()} [/INST] {response.strip()} </s><s> [INST] ")
        texts.append(f"{message.strip()} [/INST]")
        return texts


class QwenFormatter(Formatter):
    DESCRIPTION = """
    # qwen-webui
    """
    stop_words = ["<|im_start|>assistant","<|im_end|>","\n't"]

    def format_texts(self, system_prompt, chat_history, message) -> [str]:
        texts = [f"<|im_start|>system\n{system_prompt}<|im_end|>"]
        for user_input, response in chat_history:
            texts.append(f"\n<|im_start|>user\n{user_input.strip()}<|im_end|>\n<|im_start|>assistant\n{response.strip()}<|im_end|>")
        texts.append(f"\n<|im_start|>user\n{message.strip()}<|im_end|>\n<|im_start|>assistant\n")
        return texts


class Baichuan2Formatter(Formatter):
    DESCRIPTION = """
    # baichuan2-webui
    """
    stop_words = ["Q:"]

    def format_texts(self, system_prompt, chat_history, message) -> [str]:
        texts = [f"{system_prompt}\n"]
        for user_input, response in chat_history:
            texts.append(f"Q:{user_input.strip()} A:{response.strip()}")
        texts.append(f"Q:{message.strip()} A:")
        return texts


class ModelFormatterHolder:
    model_formatter = None

    @staticmethod
    def get_model_formatter() -> Formatter:
        return ModelFormatterHolder.model_formatter

    @staticmethod
    def set_model_formatter(model_path:str):
        model_type = model_path.split("/")[-1].split("-")[0]  # 从模型路径中提取 model_type
        formatter_class = globals().get(f"{model_type.capitalize()}Formatter")
        if formatter_class:
            ModelFormatterHolder.model_formatter  = formatter_class()
        else:
            raise ValueError(f"Unsupported model_type: {model_type}")


