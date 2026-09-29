"""Request and response bodies. These also drive the OpenAPI reference."""
from typing import Literal

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    model: str = Field(description="ID of the model to use. List them with GET /v1/models.", examples=["lugha-demo-large"])
    prompt: str = Field(min_length=1, max_length=4000, description="The text you want the model to respond to.", examples=["Habari, tafadhali nieleze Kampala ni nini."])
    language: str = Field(default="en", description="Language code of the prompt. Each model supports a different set.", examples=["sw"])
    max_tokens: int = Field(default=64, ge=1, description="Upper limit on tokens in the response. Cannot exceed the model's max_output_tokens.", examples=[64])
    region: str = Field(default="ke", description="Where the request is processed: ke, ug, ma or mu.", examples=["ug"])


class Usage(BaseModel):
    prompt_tokens: int = Field(description="Tokens in the prompt.")
    completion_tokens: int = Field(description="Tokens in the response.")
    total_tokens: int = Field(description="prompt_tokens plus completion_tokens.")


class GenerateResponse(BaseModel):
    id: str = Field(description="Unique ID for this generation.", examples=["gen_3f9c2a71b8d4"])
    model: str = Field(description="The model that handled the request.")
    language: str = Field(description="The language code you sent.")
    output: str = Field(description="The generated text.")
    finish_reason: Literal["stop", "length"] = Field(description="stop means the response ended naturally. length means it was cut off at max_tokens.")
    usage: Usage = Field(description="Token counts for this request.")


class TokenCountRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20000, description="Text to count tokens for.", examples=["Habari ya asubuhi, rafiki yangu."])


class TokenCountResponse(BaseModel):
    token_count: int = Field(description="Number of tokens in the text.")
    word_count: int = Field(description="Number of words in the text, split on whitespace.")
    tokens_per_word: float = Field(description="token_count divided by word_count, rounded to two decimals.")


class ModelInfo(BaseModel):
    id: str = Field(description="Model ID. Pass this as model when you generate text.")
    max_output_tokens: int = Field(description="Largest max_tokens value this model accepts.")
    languages: list[str] = Field(description="Language codes this model accepts.")


class ModelList(BaseModel):
    data: list[ModelInfo] = Field(description="The available models.")


class ErrorDetail(BaseModel):
    type: str = Field(description="Machine readable error category. Branch your code on this value.", examples=["invalid_request"])
    message: str = Field(description="Human readable explanation. Do not parse it.", examples=["model: Field required"])
    request_id: str = Field(description="Quote this when contacting support.", examples=["req_8a1d4c92e07b"])


class ErrorResponse(BaseModel):
    error: ErrorDetail


class HealthResponse(BaseModel):
    status: str = Field(description="Always ok when the service is running.", examples=["ok"])
