from typing import List
from llama.specification.base_specification import BaseSpecification
from powerml import PowerML
from random import sample
import openai
import faiss
import numpy as np
from collections.abc import MutableMapping


# TODO: confirm what cue works best for lists
# LIST_CUE = '['
# LIST_CUE = '1.'
LIST_CUE = "\n-"
ESC_LIST_CUE = "\\n-"
MAX_INPUT_TOKENS = 3872
EMBEDDING_MODEL = lambda prompt: openai.Embedding.create(
    input=[prompt], model="text-embedding-ada-002"
)["data"][0]["embedding"]
SEPARATOR = "\n"
EXAMPLE_SEPARATOR = "\n"
FIXED_TEMPERATURE = 0.0
RANDOM_TEMPERATURE = 0.7


def count_tokens(string):
    return len(string)  # TODO: use better heuristic or actual count


def get_example_length(example):
    example_prompt = ""
    example_prompt = add_input_to_prompt(example_prompt, example["input"])
    example_prompt = add_output_to_prompt(
        example_prompt, type(example["output"]), example["output"]
    )
    return count_tokens(example_prompt)


class BaseSelector:
    def __init__(self, max_input_tokens=MAX_INPUT_TOKENS):
        self.max_input_tokens = max_input_tokens

    def sort(self, examples, _):
        return examples

    def run(self, examples, input, output_spec):
        prompt = ""
        prompt = add_instruction_to_prompt(prompt, input, output_spec)
        prompt = add_input_to_prompt(prompt, input)
        prompt = add_output_to_prompt(prompt, output_spec)
        ordered_examples = self.sort(examples, input)
        selected_examples = []
        prompt_length = len(prompt)
        for example in ordered_examples:
            example_length = get_example_length(example)
            if prompt_length + example_length > self.max_input_tokens:
                break
            prompt_length += example_length
            selected_examples.append(example)
        return selected_examples


class LengthSelector(BaseSelector):
    def sort(self, examples, _):
        return sample(examples, len(examples))


class SimilaritySelector(BaseSelector):
    def __init__(
        self, max_input_tokens=MAX_INPUT_TOKENS, embedding_model=EMBEDDING_MODEL
    ):
        super().__init__(max_input_tokens)
        self.embedding_model = embedding_model

    def __merge_input(self, input):
        merged_input = ""
        parsed_input = input.schema()

        input_properties = parsed_input.get("properties", {})
        for param, _ in input_properties.items():
            merged_input += get_arg(input, param) + SEPARATOR

        return merged_input

    def _get_embedding(self, input):
        merged_input = self.__merge_input(input)
        return self.embedding_model(merged_input)

    def sort(self, examples, input):
        _, sorted_example_indices = self.index.search(
            np.array([self._get_embedding(input)], dtype=np.float32), len(examples)
        )
        return [
            examples[sorted_example_index]
            for sorted_example_index in sorted_example_indices[0]
        ]


class MaxMarginalRelevanceSelector(SimilaritySelector):
    def __cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def __sort_by_max_marginal_relevance(
        self,
        input_embedding,
        embeddings,
    ):
        lambda_multiplier = 0.5
        sorted_indices = []
        while len(sorted_indices) < len(embeddings):
            best_score = -float("inf")
            best_index = -1
            for i, embedding in enumerate(embeddings):
                if i in sorted_indices:
                    continue
                similarity_score = self.__cosine_similarity(input_embedding, embedding)
                diversity_score = 0.0
                if sorted_indices:
                    diversity_score = -1.0
                for j in sorted_indices:
                    similarity = self.__cosine_similarity(embedding, embeddings[j])
                    if similarity > diversity_score:
                        diversity_score = similarity
                curr_score = (
                    lambda_multiplier * similarity_score
                    - (1 - lambda_multiplier) * diversity_score
                )
                if curr_score > best_score:
                    best_score = curr_score
                    best_index = i
            sorted_indices.append(best_index)
        return sorted_indices

    def sort(self, examples, input):
        input_embedding = self._get_embedding(input)
        _, sorted_example_indices = self.index.search(
            np.array([input_embedding], dtype=np.float32), len(examples)
        )
        example_embeddings = [
            self.index.reconstruct(int(sorted_example_index))
            for sorted_example_index in sorted_example_indices[0]
        ]
        sorted_example_indices = self.__sort_by_max_marginal_relevance(
            input_embedding, example_embeddings
        )
        return [
            examples[sorted_example_index]
            for sorted_example_index in sorted_example_indices
        ]


class Llama:
    def __init__(self, config=None, example_selector=LengthSelector()):
        if config is None:
            self.llm = PowerML()
        else:
            self.llm = PowerML(config)

        self.examples = []
        self.example_selector = example_selector

    def fit(self, examples: list):
        self.examples = examples
        if issubclass(type(self.example_selector), SimilaritySelector):
            embeddings = [
                self.example_selector._get_embedding(example["input"])
                for example in examples
            ]
            index = faiss.IndexFlatL2(len(embeddings[0]))
            index.add(np.array(embeddings, dtype=np.float32))
            self.example_selector.index = index

    def run(
        self,
        input: BaseSpecification,
        output_spec: BaseSpecification,
        temperature=FIXED_TEMPERATURE,
        random: bool = False,
        use_examples: bool = True,
    ):
        if use_examples:
            examples = self.example_selector.run(self.examples, input, output_spec)
        else:
            examples = []

        prompt = ""
        prompt = add_instruction_to_prompt(prompt, input, output_spec)
        for example in examples:
            prompt = add_input_to_prompt(prompt, example["input"])
            prompt = add_output_to_prompt(prompt, output_spec, example["output"])
            prompt += EXAMPLE_SEPARATOR
        prompt = add_input_to_prompt(prompt, input)
        prompt = add_output_to_prompt(prompt, output_spec)
        temperature = RANDOM_TEMPERATURE if random else temperature
        # print("prompt--------------------------\n", prompt, "---------------------------\n")
        result = self.llm.predict(prompt, temperature=temperature, max_tokens=256)
        return parse_cue(apply_cue(output_spec) + result, output_spec)


def parse_properties(properties, definitions, param_list: List[str] = []):
    results = {}
    for param, fields in properties.items():
        new_param_list = param_list + [param]
        if "allOf" in fields or "$ref" in fields:
            if "allOf" in fields:
                ref_properties_path = fields["allOf"][0]["$ref"]  # e.g. "#/definitions/Example"
            if "$ref" in fields:
                ref_properties_path = fields["$ref"]  # e.g. "#/definitions/Example"
            ref_class_name = ref_properties_path.split("/")[-1]  # e.g. "Example"
            ref_class = definitions[ref_class_name]
            input_properties = ref_class.get("properties", {})
            results.update(parse_properties(input_properties, definitions, new_param_list))
        else:
            fields['path'] = new_param_list
            results[param] = fields
    return results


def add_instruction_to_prompt(
    prompt: str, input: BaseSpecification, output_spec: BaseSpecification
):
    parsed_input = input.schema()
    parsed_output = output_spec.schema()
    prompt = f"Given:{SEPARATOR}"

    input_definitions = parsed_input.get("definitions", {})
    input_properties = parsed_input.get("properties", {})

    # Get every leaf field in input
    properties = parse_properties(input_properties, input_definitions)
    for param, fields in properties.items():
        prompt += f"{fields['description']}{SEPARATOR}"

    prompt += f"Generate:{SEPARATOR}"

    output_definitions = parsed_output.get("definitions", {})
    output_properties = parsed_output.get("properties", {})
    properties = parse_properties(output_properties, output_definitions)
    for param, fields in properties.items():
        if fields["type"] == "array":
            prompt += f"{fields['description']} after '{param}:{ESC_LIST_CUE}'{SEPARATOR}"  # TODO: figure how not to hardcode this
        else:
            prompt += f"{fields['description']} after '{param}:'{SEPARATOR}"
    return prompt


def list_to_nl(list: list):
    if len(list) == 1:
        return str(list[0])
    elif len(list) == 2:
        return str(list[0]) + " and " + str(list[1])
    else:
        return ", ".join([str(l) for l in list[:-1]]) + " and " + str(list[-1])


def get_recursive_attr(input, field_path):
    for field in field_path:
        input = input._get_attribute_raw(field)
    return input


def add_input_to_prompt(prompt: str, input: BaseSpecification):
    parsed_input = input.schema()
    input_definitions = parsed_input.get("definitions", {})
    input_properties = parsed_input.get("properties", {})
    properties = parse_properties(input_properties, input_definitions)
    for _, fields in properties.items():
        user_attr = get_recursive_attr(input, fields['path'])
        description = str(fields["description"])
        prompt += description
        if (
            "type" in fields
            and fields["type"] == "array"
            and len(user_attr) > 1
        ):
            prompt += f" are " + list_to_nl(user_attr) # TODO: does not unpack complex lists
        else:
            prompt += " is " + str(user_attr)
        prompt += SEPARATOR
    return prompt


def add_output_to_prompt(prompt: str, output_spec: BaseSpecification, output=None):
    parsed_output = output_spec.schema()

    output_definitions = parsed_output.get("definitions", {})
    output_properties = parsed_output.get("properties", {})

    if output:
        properties = parse_properties(output_properties, output_definitions)
        for param, fields in properties.items():
            if fields["type"] == "array":
                prompt += f"{param}:"
                for el in output._get_attribute_raw(param):
                    prompt += f"{LIST_CUE}{el}"
                prompt += SEPARATOR
            else:
                prompt += f"{param}: {output._get_attribute_raw(param)}{SEPARATOR}"
    else:
        prompt += apply_cue(output_spec)
    return prompt


def apply_cue(output_spec: BaseSpecification):
    output_name, output_type = list(output_spec.__annotations__.items())[0]
    if output_type == list:
        cue = f"{output_name}:{LIST_CUE}"
    else:
        cue = f"{output_name}:"
    return cue


def parse_cue(output, output_spec: BaseSpecification):
    output_values = {}
    remainder = output
    for cue_key, cue_type in reversed(output_spec.__annotations__.items()):
        remainder, _, cue_value = remainder.partition(f"{cue_key}:")
        output_values[cue_key] = parse_output(cue_value, cue_type)
    return output_spec.parse_obj(output_values)


def parse_output(output, output_type):
    if output_type == list:
        output = [el.strip() for el in output.split(LIST_CUE) if len(el.strip()) > 0]
    else:
        output = output_type(output.strip())
    return output


def get_arg(input, name):
    value = input.dict().get(name)
    return str(value)
