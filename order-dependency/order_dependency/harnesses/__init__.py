"""Answer backends. Each exposes ``async answer(mcq, perm_index, perm, sample) -> Trial``.

* ``claude_answerer.ClaudeAnswerer`` - Anthropic Messages API, parses the sampled letter.
* ``hf_answerer.HFAnswerer`` - local Hugging Face model, argmax of the option-letter logits.
"""
