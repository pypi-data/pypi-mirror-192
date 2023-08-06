# coding: utf-8

import typing
import httpx
from parsel.selector import Selector
from parsel.utils import iflatten, extract_regex
from httpx._client import USE_CLIENT_DEFAULT, UseClientDefault
from httpx._config import DEFAULT_TIMEOUT_CONFIG, DEFAULT_LIMITS, DEFAULT_MAX_REDIRECTS
from httpx._transports.default import AsyncResponseStream, map_httpcore_exceptions, httpcore

__all__ = [
    'Request',
    'Response',
    'Client',
]


class Request(httpx.Request):

    def __init__(self, *, url, method='GET', headers=None, params=None, content=None, data=None, json=None,
                 files=None, cookies=None, stream=None, extensions=None, auth=None, verify=None, cert=None,
                 http1=True, http2=False, proxies=None, mounts=None, timeout=DEFAULT_TIMEOUT_CONFIG,
                 follow_redirects=True, limits=DEFAULT_LIMITS, max_redirects=DEFAULT_MAX_REDIRECTS,
                 event_hooks=None, transport=None, trust_env=True, default_encoding='utf-8', stream_model=False,
                 default_client=None, client=None, filter_req=False, callback=None, meta=None, cb_kw=None):
        super().__init__(method, url, params=params, headers=headers, cookies=cookies, content=content,
                         data=data, files=files, json=json, stream=stream, extensions=extensions)
        self.client_params = {
            'auth': auth, 'verify': verify, 'cert': cert, 'http1': http1, 'http2': http2, 'proxies': proxies,
            'mounts': mounts, 'timeout': timeout, 'follow_redirects': follow_redirects, 'limits': limits,
            'max_redirects': max_redirects, 'event_hooks': event_hooks, 'transport': transport,
            'trust_env': trust_env, 'default_encoding': default_encoding
        }
        self.stream_model = stream_model
        self.default_client: typing.Optional[Client] = default_client
        self.client: typing.Optional[Client] = client
        self.filter_req = filter_req
        self.callback = callback
        self.meta: typing.Optional[dict] = meta or {}
        self.cb_kw: typing.Optional[dict] = cb_kw or {}
        self.exception = None

    async def send(self):
        client = self.client
        self.set_timeout(client)
        try:
            if self.client is None:
                client = Client(**self.client_params)
                if self.stream_model:
                    self.default_client = client
            return await client.send(self, stream=self.stream_model, auth=client.auth,
                                     follow_redirects=client.follow_redirects)
        except httpx.HTTPError as exc:
            self.exception = exc
        finally:
            if not self.stream_model and self.client is None:
                await client.aclose()

    def set_timeout(self, client):
        if 'timeout' not in self.extensions:
            timeout = self.client_params['timeout'] if client is None else client.timeout
            if not isinstance(timeout, UseClientDefault):
                timeout = httpx.Timeout(timeout)
            self.extensions['timeout'] = timeout.as_dict()


class Response(httpx.Response):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_selector = None

    @property
    def request(self) -> Request:
        return self._request

    @request.setter
    def request(self, value: Request):
        self._request = value

    @property
    def selector(self):
        if self._cached_selector is None:
            self._cached_selector = Selector(self.text)
        return self._cached_selector

    def xpath(self, query, **kwargs):
        return self.selector.xpath(query=query, **kwargs)

    def css(self, query):
        return self.selector.css(query)

    def re(self, regex, replace_entities=True):
        return extract_regex(regex, self.selector.get(), replace_entities=replace_entities)

    def re_first(self, regex, default=None, replace_entities=True):
        return next(iflatten(self.re(regex, replace_entities=replace_entities)), default)

    async def close_default_client(self):
        default_client = self.request.default_client
        if default_client is not None:
            await default_client.aclose()
            self.request.default_client = None


class HttpTransport(httpx.AsyncHTTPTransport):

    async def handle_async_request(self, request):
        assert isinstance(request.stream, httpx.AsyncByteStream)
        req = httpcore.Request(
            method=request.method,
            url=httpcore.URL(
                scheme=request.url.raw_scheme,
                host=request.url.raw_host,
                port=request.url.port,
                target=request.url.raw_path,
            ),
            headers=request.headers.raw,
            content=request.stream,
            extensions=request.extensions,
        )
        with map_httpcore_exceptions():
            resp = await self._pool.handle_async_request(req)
        assert isinstance(resp.stream, typing.AsyncIterable)
        return Response(
            status_code=resp.status,
            headers=resp.headers,
            stream=AsyncResponseStream(resp.stream),
            extensions=resp.extensions,
        )


class Client(httpx.AsyncClient):

    def _init_transport(self, verify=True, cert=None, http1=True, http2=False, limits=DEFAULT_LIMITS,
                        transport=None, app=None, trust_env=True):
        if transport is not None:
            return transport
        return HttpTransport(
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            limits=limits,
            trust_env=trust_env,
        )

    def _init_proxy_transport(self, proxy, verify=True, cert=None, http1=True, http2=False, limits=DEFAULT_LIMITS,
                              trust_env=True):
        return HttpTransport(
            verify=verify,
            cert=cert,
            http2=http2,
            limits=limits,
            trust_env=trust_env,
            proxy=proxy,
        )

    def _build_redirect_request(self, request: Request, response: Response) -> Request:
        method = self._redirect_method(request, response)
        url = self._redirect_url(request, response)
        headers = self._redirect_headers(request, url, method)
        stream = self._redirect_stream(request, method)
        cookies = httpx.Cookies(self.cookies)
        return Request(
            url=url,
            method=method,
            headers=headers,
            cookies=cookies,
            stream=stream,
            extensions=request.extensions,
            stream_model=request.stream_model,
            default_client=request.default_client,
            client=request.client,
            filter_req=request.filter_req,
            callback=request.callback,
            meta=request.meta,
            cb_kw=request.cb_kw,
            **request.client_params
        )

    async def send(self, request, *, stream=False, auth=USE_CLIENT_DEFAULT,
                   follow_redirects=USE_CLIENT_DEFAULT) -> Response:
        return await super().send(request, stream=stream, auth=auth, follow_redirects=follow_redirects)
