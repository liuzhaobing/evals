# -*- coding:utf-8 -*-
import logging
import logging.config
import asyncio

from flask import Flask, has_request_context, copy_current_request_context, request, make_response
from gevent import pywsgi
from concurrent import futures
from functools import wraps

from evals.utils import cloudminds

app = Flask(__name__)
max_workers = 40

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "class": "logging.Formatter",
                "format": "[%(asctime)s][%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "server.log",
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            }
        },
        "loggers": {},
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"]
        },
    }
)


def run_async(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        call_result = futures.Future()

        def _run():
            loop = asyncio.new_event_loop()
            try:
                result = loop.run_until_complete(func(*args, **kwargs))
            except Exception as error:
                call_result.set_exception(error)
            else:
                call_result.set_result(result)
            finally:
                loop.close()

        loop_executor = futures.ThreadPoolExecutor(max_workers=max_workers)
        if has_request_context():
            _run = copy_current_request_context(_run)
        loop_future = loop_executor.submit(_run)
        loop_future.result()
        return call_result.result()

    return _wrapper


def all_models():
    return [model.MODEL_NAME for model in cloudminds.CloudMindsModel.__subclasses__() if hasattr(model, "MODEL_NAME")]


def completion(*args, **kwargs):
    if kwargs["model"] not in all_models():
        return False
    return cloudminds.ChatCompletion.create(*args, **kwargs)


@app.route("/models", methods=["GET"])
@run_async
async def get_all_models():
    return make_response(dict(success=True, data=all_models()))


@app.route("/chat", methods=["POST"])
@run_async
async def model_completion():
    req = request.get_json()
    res = completion(**req)
    if not res:
        return make_response(dict(success=False, error=f"no such model named [{req.model_name}]"))
    logging.info(dict(request=req, response=res))
    return make_response(dict(success=True, data=res))


def main():
    listener = ('0.0.0.0', 8091)
    server = pywsgi.WSGIServer(listener, app)
    logging.info("Starting HTTP server on %s", listener)
    server.serve_forever()


if __name__ == '__main__':
    main()
