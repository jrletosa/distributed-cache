import requests
import traceback
import errors


class ServiceFailedException(errors.CacheException):
    code = 500


def is_ok_code_response(code):
    return 200 <= code < 500


def _make_request(func, url, *args, **kwargs):
    response = None
    last_raised_exception = None
    last_raised_exception_tb = None

    try:
        response = func(url, *args, **kwargs)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as ex:
        last_raised_exception = ex
        last_raised_exception_tb = traceback.format_exc()

    if response is not None and is_ok_code_response(response.status_code):
        return response

    if response is not None:
        raise ServiceFailedException("Request Failed",
                                     url=url,
                                     response=response.text,
                                     status_code=response.status_code)
    else:
        raise ServiceFailedException("Request failed",
                                     url=url,
                                     exception=str(last_raised_exception),
                                     traceback=last_raised_exception_tb)


def get(url, retries=5, delay=1, backoff=1, *args, **kwargs):
    return _make_request(requests.get, url, *args, **kwargs)


def post(url, retries=0, delay=1, backoff=1, *args, **kwargs):
    return _make_request(requests.post, url, *args, **kwargs)
