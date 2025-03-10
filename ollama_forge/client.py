#!/usr/bin/env python3
"""
Core client functionality for interacting with the Ollama Forge v0.1.9.

This module provides a fully typed, self-documenting client interface to
all core Ollama API endpoints including model management, generation, chat,
embeddings, and more—aligned with Eidosian principles of recursive
refinement, structural integrity, and contextual excellence.

Features:
- Complete API coverage with both synchronous and asynchronous interfaces
- Comprehensive error handling with precise exception types
- Advanced fallback mechanisms for model availability
- Optimized embedding operations including batch processing
- Streaming support for all compatible endpoints
"""

import logging
import time
import json
import requests
import aiohttp

from typing import (
    Any, Dict, List, Optional, Iterator, Union,
    Callable, TypeVar, Tuple, Generator, AsyncIterator, cast
)
from requests.adapters import HTTPAdapter

from .helpers.common import (
    DEFAULT_OLLAMA_API_URL,
    make_api_request,
    async_make_api_request
)
from .exceptions import (
    ConnectionError,
    TimeoutError,
    OllamaAPIError,
    ModelNotFoundError,
    InvalidRequestError,
    StreamingError,
    ParseError
)
from .helpers.model_constants import (
    DEFAULT_CHAT_MODEL,
    BACKUP_CHAT_MODEL,
    DEFAULT_EMBEDDING_MODEL,
    BACKUP_EMBEDDING_MODEL,
    resolve_model_alias,
    get_fallback_model
)

logger = logging.getLogger(__name__)

T = TypeVar('T')
CacheKey = str
CacheValue = Tuple[float, Any]
APIResponse = Union[Dict[str, Any], requests.Response]


class OllamaClient:
    """
    Client for interacting with the Ollama Forge.
    """

    def __init__(
        self,
        base_url: str = DEFAULT_OLLAMA_API_URL,
        timeout: int = 300,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        cache_enabled: bool = False,
        cache_ttl: float = 300.0
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.cache_enabled = cache_enabled
        self.cache_ttl = cache_ttl
        self._response_cache: Dict[CacheKey, CacheValue] = {}

    def _with_retry(self, func: Callable[[], T]) -> T:
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return func()
            except (ConnectionError, TimeoutError) as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise e
        if last_exception:
            raise last_exception
        raise RuntimeError("Retry logic failed without an exception")

    def get_version(self) -> Dict[str, Any]:
        response = make_api_request(
            "GET",
            "/api/version",
            base_url=self.base_url,
            timeout=self.timeout,
        )
        return self._handle_response(response)

    async def aget_version(self) -> Dict[str, Any]:
        response = await async_make_api_request(
            "GET",
            "/api/version",
            base_url=self.base_url,
            timeout=self.timeout,
        )
        return response.json()

    def generate(
        self,
        model: str = DEFAULT_CHAT_MODEL,
        prompt: str,
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        data: Dict[str, Any] = {"model": model, "prompt": prompt, "stream": stream}
        if options:
            data.update(options)
        if stream:
            response = self._with_retry(lambda: requests.post(
                f"{self.base_url.rstrip('/')}/api/generate",
                json=data,
                stream=True,
                timeout=self.timeout
            ))
            def response_generator() -> Generator[Dict[str, Any], None, None]:
                for line in response.iter_lines():
                    if line:
                        try:
                            yield json.loads(line.decode('utf-8').strip())
                        except json.JSONDecodeError as e:
                            yield {"error": f"JSON decode error: {str(e)}"}
            return response_generator()
        else:
            response = make_api_request(
                "POST",
                "/api/generate",
                data=data,
                base_url=self.base_url,
                timeout=self.timeout
            )
            return self._ensure_dict(response)

    async def agenerate(
        self,
        model: str,
        prompt: str,
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Union[Dict[str, Any], AsyncIterator[Dict[str, Any]]]:
        data: Dict[str, Any] = {"model": model, "prompt": prompt, "stream": stream}
        if options:
            data.update(options)
        if not stream:
            response = await async_make_api_request(
                "POST",
                "/api/generate",
                data=data,
                base_url=self.base_url,
                timeout=self.timeout
            )
            if hasattr(response, 'json'):
                yield await response.json()
            else:
                yield response
        else:
            url = f"{self.base_url.rstrip('/')}/api/generate"
            timeout_obj = aiohttp.ClientTimeout(total=float(self.timeout))
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url, json=data) as resp:
                    while True:
                        line = await resp.content.readline()
                        if not line:
                            break
                        try:
                            chunk = json.loads(line.decode('utf-8').strip())
                            yield chunk
                            if chunk.get("done"):
                                break
                        except json.JSONDecodeError as e:
                            yield {"error": f"JSON decode error: {str(e)}"}

    def chat(
        self,
        model: str = DEFAULT_CHAT_MODEL,
        messages: List[Dict[str, str]],
        stream: bool = True,
        options: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        opt: Dict[str, Any] = options.copy() if options else {}
        timeout = min(opt.get("timeout", self.timeout), 600)
        if self._is_likely_embedding_model(model):
            msg = (f"Model '{model}' appears to be an embedding-only model "
                   "and doesn't support chat.")
            logger.error(msg)
            return self._error_generator(msg)

        data: Dict[str, Any] = {"model": model, "messages": messages, "stream": stream}
        data.update(opt)
        if stream:
            try:
                session = requests.Session()
                session.mount('http://', HTTPAdapter(max_retries=1))
                response = session.post(
                    f"{self.base_url.rstrip('/')}/api/chat",
                    json=data,
                    stream=True,
                    timeout=(30.0, timeout - 30.0)
                )
                if response.status_code == 400:
                    err_msg = "Bad request - the model may not support chat functionality"
                    try:
                        err_data = json.loads(response.content)
                        if "error" in err_data:
                            err_msg = err_data["error"]
                    except Exception:
                        pass
                    logger.error(f"Chat API error: {err_msg}")
                    return self._error_generator(err_msg)
                if response.status_code != 200:
                    logger.error(f"Chat API error: HTTP {response.status_code}")
                    return self._error_generator(f"HTTP error {response.status_code}")
                return self._safe_stream_generator(response, timeout)
            except Exception as e:
                logger.error(f"Chat request error: {str(e)}")
                return self._error_generator(str(e))
        else:
            try:
                response = make_api_request(
                    "POST",
                    "/api/chat",
                    data=data,
                    base_url=self.base_url,
                    timeout=min(timeout, 300)
                )
                return self._ensure_dict(response)
            except Exception as e:
                logger.error(f"Chat request error: {str(e)}")
                return {"error": str(e)}

    async def achat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Union[Dict[str, Any], AsyncIterator[Dict[str, Any]]]:
        data: Dict[str, Any] = {"model": model, "messages": messages, "stream": stream}
        if options:
            data.update(options)
        if not stream:
            response = await async_make_api_request(
                "POST",
                "/api/chat",
                data=data,
                base_url=self.base_url,
                timeout=self.timeout
            )
            yield await response.json()
        else:
            url = f"{self.base_url.rstrip('/')}/api/chat"
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, timeout=self.timeout) as resp:
                    while True:
                        line = await resp.content.readline()
                        if not line:
                            break
                        try:
                            chunk = json.loads(line.decode('utf-8').strip())
                            yield chunk
                            if chunk.get("done"):
                                break
                        except json.JSONDecodeError as e:
                            yield {"error": f"JSON decode error: {str(e)}"}

    def create_embedding(
        self,
        model: str = DEFAULT_EMBEDDING_MODEL,
        prompt: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        data: Dict[str, Any] = {"model": model, "prompt": prompt}
        if options:
            data.update(options)
        response = make_api_request(
            "POST",
            "/api/embed",
            data=data,
            base_url=self.base_url,
            timeout=self.timeout
        )
        return self._ensure_dict(response)

    async def acreate_embedding(
        self,
        model: str,
        prompt: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        data: Dict[str, Any] = {"model": model, "prompt": prompt}
        if options:
            data.update(options)
        response = await async_make_api_request(
            "POST",
            "/api/embed",
            data=data,
            base_url=self.base_url,
            timeout=self.timeout
        )
        return response.json()

    def batch_embeddings(
        self,
        model: str = DEFAULT_EMBEDDING_MODEL,
        prompts: List[str],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        data: Dict[str, Any] = {"model": model, "input": prompts}
        if options:
            data.update(options)
        response = make_api_request(
            "POST",
            "/api/embed",
            data=data,
            base_url=self.base_url,
            timeout=self.timeout
        )
        return self._ensure_dict(response)

    def list_models(self) -> Dict[str, Any]:
        try:
            response = make_api_request(
                "GET",
                "/api/tags",
                base_url=self.base_url,
                timeout=self.timeout,
            )
            return self._ensure_dict(response)
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            return {"error": str(e)}

    def list_running_models(self) -> Dict[str, Any]:
        try:
            response = make_api_request(
                "GET",
                "/api/ps",
                base_url=self.base_url,
                timeout=self.timeout,
            )
            return self._ensure_dict(response)
        except Exception as e:
            logger.error(f"Error listing running models: {str(e)}")
            return {"error": str(e)}

    def get_model_info(self, model: str) -> Dict[str, Any]:
        try:
            response = make_api_request(
                "GET",
                f"/api/show?name={model}",
                base_url=self.base_url,
                timeout=self.timeout,
            )
            return self._ensure_dict(response)
        except Exception as e:
            logger.error(f"Error getting model info for {model}: {str(e)}")
            return {"error": str(e)}

    def pull_model(
        self,
        model: str,
        stream: bool = False
    ) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]:
        data: Dict[str, Any] = {"model": model}
        if stream:
            try:
                response = self._with_retry(lambda: requests.post(
                    f"{self.base_url.rstrip('/')}/api/pull",
                    json=data,
                    stream=True,
                    timeout=self.timeout
                ))
                def response_generator() -> Generator[Dict[str, Any], None, None]:
                    try:
                        for line in response.iter_lines():
                            if line:
                                try:
                                    yield json.loads(line.decode('utf-8').strip())
                                except json.JSONDecodeError as e:
                                    logger.warning(f"Skipping invalid JSON: {e}")
                                    yield {"status": "parsing_error", "error": str(e)}
                    except Exception as ex:
                        logger.error(f"Error in pull stream: {str(ex)}")
                        yield {"status": "error", "error": str(ex)}
                return response_generator()
            except Exception as e:
                logger.error(f"Error pulling model {model}: {str(e)}")
                def error_generator() -> Generator[Dict[str, Any], None, None]:
                    yield {"status": "error", "error": str(e)}
                return error_generator()
        else:
            try:
                response = make_api_request(
                    "POST",
                    "/api/pull",
                    data=data,
                    base_url=self.base_url,
                    timeout=self.timeout
                )
                return self._ensure_dict(response)
            except Exception as e:
                logger.error(f"Error pulling model {model}: {str(e)}")
                return {"status": "error", "error": str(e)}

    def delete_model(self, model: str) -> bool:
        response = make_api_request(
            "DELETE",
            "/api/delete",
            data={"model": model},
            base_url=self.base_url,
            timeout=self.timeout,
        )
        return hasattr(response, "status_code") and response.status_code == 200

    def copy_model(self, source: str, destination: str) -> Dict[str, Any]:
        data: Dict[str, Any] = {"source": source, "destination": destination}
        try:
            response = make_api_request(
                "POST",
                "/api/copy",
                data=data,
                base_url=self.base_url,
                timeout=self.timeout
            )
            return self._ensure_dict(response)
        except Exception as e:
            logger.error(f"Error copying model from {source} to {destination}: {str(e)}")
            return {"error": str(e)}

    def create_model(
        self,
        name: str,
        modelfile: str,
        stream: bool = False
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        data: Dict[str, Any] = {"name": name, "modelfile": modelfile, "stream": stream}
        if stream:
            response = self._with_retry(lambda: requests.post(
                f"{self.base_url.rstrip('/')}/api/create",
                json=data,
                stream=True,
                timeout=self.timeout
            ))
            def response_generator() -> Generator[Dict[str, Any], None, None]:
                for line in response.iter_lines():
                    if line:
                        try:
                            yield json.loads(line.decode('utf-8').strip())
                        except json.JSONDecodeError as e:
                            yield {"error": f"JSON decode error: {str(e)}"}
            return response_generator()
        else:
            response = make_api_request(
                "POST",
                "/api/create",
                data=data,
                base_url=self.base_url,
                timeout=self.timeout
            )
            return self._ensure_dict(response)

    def push_model(
        self,
        name: str,
        stream: bool = False
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        data: Dict[str, Any] = {"model": name, "stream": stream}
        if stream:
            response = self._with_retry(lambda: requests.post(
                f"{self.base_url.rstrip('/')}/api/push",
                json=data,
                stream=True,
                timeout=self.timeout
            ))
            def response_generator() -> Generator[Dict[str, Any], None, None]:
                for line in response.iter_lines():
                    if line:
                        try:
                            yield json.loads(line.decode('utf-8').strip())
                        except json.JSONDecodeError as e:
                            yield {"error": f"JSON decode error: {str(e)}"}
            return response_generator()
        else:
            response = make_api_request(
                "POST",
                "/api/push",
                data=data,
                base_url=self.base_url,
                timeout=self.timeout
            )
            return self._ensure_dict(response)

    def _is_likely_embedding_model(self, model_name: str) -> bool:
        patterns = [
            "embed", "embedding", "text-embedding", "nomic-embed",
            "all-minilm", "e5-", "bge-", "instructor-", "sentence-"
        ]
        mn = model_name.lower()
        return any(pattern in mn for pattern in patterns)

    def _error_generator(self, error_msg: str) -> Generator[Dict[str, Any], None, None]:
        yield {"error": error_msg}
        yield {"done": True}

    def _safe_stream_generator(
        self, response: requests.Response, timeout: int
    ) -> Generator[Dict[str, Any], None, None]:
        start_time = time.time()
        i = 0
        for line in response.iter_lines():
            if i % 20 == 0 and (time.time() - start_time) > timeout:
                yield {"error": "Response timeout exceeded", "timeout": True}
                return
            if not line:
                continue
            try:
                chunk = json.loads(line.decode('utf-8').strip())
                yield chunk
                if chunk.get("done", False):
                    return
            except json.JSONDecodeError:
                try:
                    text = line.decode('utf-8', errors='replace')
                    yield {"message": {"content": text}, "raw": True}
                except Exception as e:
                    logger.error(f"Stream decoding error: {str(e)}")
            i += 1
        yield {"done": True}

    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        prompt_parts: List[str] = []
        for m in messages:
            role = m.get("role", "").upper()
            content = m.get("content", "")
            prompt_parts.append(f"[{role}]: {content}")
        prompt_parts.append("[ASSISTANT]:")
        return "\n\n".join(prompt_parts)

    def _handle_response(self, response: APIResponse) -> Dict[str, Any]:
        if hasattr(response, "json"):
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"error": "Failed to parse API response"}
        elif isinstance(response, dict):
            return response
        else:
            return {"error": f"Unexpected response type: {type(response)}"}

    def _ensure_dict(self, response: APIResponse) -> Dict[str, Any]:
        if isinstance(response, dict):
            return response
        elif hasattr(response, 'json'):
            try:
                return cast(requests.Response, response).json()
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON: {e}")
                return {"error": f"JSON decode error: {str(e)}"}
        logger.warning(f"Unexpected response type: {type(response)}")
        return {"error": f"Unexpected response type: {type(response)}"}
