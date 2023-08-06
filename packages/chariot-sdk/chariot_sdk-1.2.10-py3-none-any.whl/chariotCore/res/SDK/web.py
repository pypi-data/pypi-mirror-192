from fastapi import FastAPI, File, Request
from fastapi.responses import JSONResponse
import uvicorn
import typing
import multiprocessing
import signal

try:
    from . import models
    from .base import *
except Exception as error:
    import models
    from base import *

####
#
#   插件的Rest API服务
#   全局变量前面请加下划线，这些变量应该只被web.py内方法调用
#   **预计在将来某一个版本中被另外一种方法替代**
#
####
_rest_server = FastAPI(title="千乘插件API接口", version="1.2.10", description="")

#   插件功能对象
#   它的类位于生成插件之后根目录下main.py文件内
_plugins = None

#   触发器进程列表
_triggers_process_list = []

#   告警接收器进程列表
_alarm_receivers_process_list = []

#   情报接收器进程列表
_indicator_receivers_process_list = []


@_rest_server.post("/actions/{action_name}", tags=["动作"])
async def actions(action_name, plugin_stdin: typing.Optional[models.PLUGIN_TEST_MODEL] = None):
    """
    #   动作接口
    """
    clearLog(clear_size=1)

    action = _plugins.actions[action_name]

    #   取出body
    data = plugin_stdin.dict()
    checkModel(data, models.PLUGIN_TEST_MODEL)
    data_body = data.get("body")

    #   获取input
    input_data = data_body.get("input")
    connection_data = data_body.get("connection")

    if data_body.get("config"):
        log("info", "获取请求中配置信息")
        loadConfig(data_body["config"])
    else:
        log("info", "请求中无配置信息，使用默认配置")

    #   执行 run 相关操作
    output = action._run(input_data, connection_data)
    if output["body"]["status"] != "True":
        return JSONResponse(content=output, status_code=500)
    else:
        return output


@_rest_server.post("/actions/{action_name}/test", tags=["动作"])
async def actions_test(action_name: str, plugin_stdin: typing.Optional[models.PLUGIN_TEST_MODEL] = None):
    """
    #   动作连接器测试接口
    """
    clearLog(clear_size=1)

    action = _plugins.actions[action_name]

    #   取出body
    data = plugin_stdin.dict()
    checkModel(data, models.PLUGIN_TEST_MODEL)
    data_body = data.get("body")

    connection_data = data_body.get("connection")

    output = action._test(connection_data)

    if data_body.get("config"):
        log("info", "获取请求中配置信息")
        loadConfig(data_body["config"])
    else:
        log("info", "请求中无配置信息，使用默认配置")

    if output["body"]["status"] != "True":
        return JSONResponse(content=output, status_code=500)
    else:
        return output


@_rest_server.post("/triggers/{trigger_name}", tags=["触发器"])
async def triggers(trigger_name: str, plugin_stdin: typing.Optional[models.PLUGIN_TEST_MODEL]):
    """
    #   触发器接口
    """
    clearLog(clear_size=1)

    #   外部类
    trigger = _plugins.triggers[trigger_name]

    #   取出body
    data = plugin_stdin.dict()
    checkModel(data, models.PLUGIN_TEST_MODEL)
    data_body = data.get("body")

    #   获取input
    input_data = data_body.get("input")
    connection_data = data_body.get("connection")
    dispatcher_url = data_body.get("dispatcher").get("url")
    cache_url = data_body.get("dispatcher").get("cache_url")

    if data_body.get("config"):
        log("info", "获取请求中配置信息")
        loadConfig(data_body["config"])
    else:
        log("info", "请求中无配置信息，使用默认配置")

    #   创建触发器进程
    global _triggers_process_list
    trigger_process = multiprocessing.Process(target=trigger._run,
                                              args=(input_data, connection_data, dispatcher_url, cache_url,))
    trigger_process.start()
    _triggers_process_list.append(trigger_process)

    return {
        "version": "v1",
        "type": "trigger_event",
        "body": {
            "status": "True",
            "log": "",
            "error_trace": "",
            "msg": "触发器进程已创建完成"
        }
    }


@_rest_server.post("/triggers/{trigger_name}/test", tags=["触发器"])
async def trigger_test(trigger_name: str, plugin_stdin: typing.Optional[models.PLUGIN_TEST_MODEL] = None):
    """
    #   触发器连接器测试接口
    """
    clearLog(clear_size=1)

    #   外部类
    trigger = _plugins.triggers[trigger_name]

    #   取出body
    data = plugin_stdin.dict()
    checkModel(data, models.PLUGIN_TEST_MODEL)
    data_body = data.get("body")

    connection_data = data_body.get("connection")

    if data_body.get("config"):
        log("info", "获取请求中配置信息")
        loadConfig(data_body["config"])
    else:
        log("info", "请求中无配置信息，使用默认配置")

    output = trigger._test(connection_data)

    return output


@_rest_server.post("/alarm_receivers/{alarm_receiver_name}", tags=["告警接收器"])
async def alarm_receivers(alarm_receiver_name: str, plugin_stdin: typing.Optional[models.PLUGIN_TEST_MODEL]):
    """
    #   告警接收器接口
    """
    clearLog(clear_size=1)

    #   外部类
    alarm_receiver = _plugins.alarm_receivers[alarm_receiver_name]

    # 取出body
    data = plugin_stdin.dict()
    checkModel(data, models.PLUGIN_TEST_MODEL)
    data_body = data.get("body")

    #   获取input
    input_data = data_body.get("input")
    connection_data = data_body.get("connection")
    dispatcher_url = data_body.get("dispatcher").get("url")
    cache_url = data_body.get("dispatcher").get("cache_url")

    if data_body.get("config"):
        log("info", "获取请求中配置信息")
        loadConfig(data_body["config"])
    else:
        log("info", "请求中无配置信息，使用默认配置")

    #   创建告警接收器进程
    global _alarm_receivers_process_list
    alarm_receiver_process = multiprocessing.Process(target=alarm_receiver._run,
                                                     args=(input_data, connection_data, dispatcher_url, cache_url,))
    alarm_receiver_process.start()
    _alarm_receivers_process_list.append(alarm_receiver_process)

    return {
        "version": "v1",
        "type": "alarm_receiver_event",
        "body": {
            "status": "True",
            "log": "",
            "error_trace": "",
            "msg": "告警接收器进程已创建完成"
        }
    }


@_rest_server.post("/alarm_receivers/{alarm_receiver_name}/test", tags=["告警接收器"])
async def alarm_receivers_test(alarm_receiver_name: str,
                               plugin_stdin: typing.Optional[models.PLUGIN_TEST_MODEL] = None):
    """
    #   告警接收器连接器测试接口
    """
    clearLog(clear_size=1)

    #   外部类
    alarm_receiver = _plugins.alarm_receivers[alarm_receiver_name]

    #   取出body
    data = plugin_stdin.dict()
    checkModel(data, models.PLUGIN_TEST_MODEL)
    data_body = data.get("body")

    connection_data = data_body.get("connection")

    if data_body.get("config"):
        log("info", "获取请求中配置信息")
        loadConfig(data_body["config"])
    else:
        log("info", "请求中无配置信息，使用默认配置")

    output = alarm_receiver._test(connection_data)

    return output


@_rest_server.post("/indicator_receivers/{indicator_receiver_name}", tags=["情报接收器"])
async def indicator_receivers(indicator_receiver_name: str, plugin_stdin: typing.Optional[models.PLUGIN_TEST_MODEL]):
    """
    #   情报接收器接口
    """
    clearLog(clear_size=1)

    #   外部类
    indicator_receiver = _plugins.indicator_receivers[indicator_receiver_name]

    #   取出body
    data = plugin_stdin.dict()
    checkModel(data, models.PLUGIN_TEST_MODEL)
    data_body = data.get("body")

    #   获取input
    input_data = data_body.get("input")
    connection_data = data_body.get("connection")
    dispatcher_url = data_body.get("dispatcher").get("url")
    cache_url = data_body.get("dispatcher").get("cache_url")

    if data_body.get("config"):
        log("info", "获取请求中配置信息")
        loadConfig(data_body["config"])
    else:
        log("info", "请求中无配置信息，使用默认配置")

    #   创建情报接收器进程
    global _indicator_receivers_process_list
    indicator_receiver_process = multiprocessing.Process(target=indicator_receiver._run,
                                                         args=(input_data, connection_data, dispatcher_url, cache_url,))
    indicator_receiver_process.start()
    _indicator_receivers_process_list.append(indicator_receiver_process)

    return {
        "version": "v1",
        "type": "alarm_receiver_event",
        "body": {
            "status": "True",
            "log": "",
            "error_trace": "",
            "msg": "情报接收器进程已创建完成"
        }
    }


@_rest_server.post("/indicator_receivers/{indicator_receiver_name}/test", tags=["情报接收器"])
async def indicator_receivers_test(indicator_receiver_name: str,
                                   plugin_stdin: typing.Optional[models.PLUGIN_TEST_MODEL] = None):
    """
    #   情报接收器连接器测试接口
    """
    clearLog(clear_size=1)

    # 外部类
    indicator_receiver = _plugins.indicator_receivers[indicator_receiver_name]

    # 取出body
    data = plugin_stdin.dict()
    checkModel(data, models.PLUGIN_TEST_MODEL)
    data_body = data.get("body")

    connection_data = data_body.get("connection")

    if data_body.get("config"):
        log("info", "获取请求中配置信息")
        loadConfig(data_body["config"])
    else:
        log("info", "请求中无配置信息，使用默认配置")

    output = indicator_receiver._test(connection_data)

    return output


@_rest_server.post("/update_plugin", tags=["插件热更新"])
async def update_plugin(update_pack: bytes = File()):
    """
    #   上传更新包
    """
    #   保存插件更新包到插件目录下update文件夹，然后重启一下就能auto update了
    save_update_pack(update_pack)

    #   重启前记得把子进程关完
    global _triggers_process_list
    global _alarm_receivers_process_list
    global _indicator_receivers_process_list

    for process in _triggers_process_list:
        process.terminate()
        log("info", f"{process} shutdown")
    for process in _alarm_receivers_process_list:
        process.terminate()
        log("info", f"{process} shutdown")
    for process in _indicator_receivers_process_list:
        process.terminate()
        log("info", f"{process} shutdown")

    restartProgram("http")


@_rest_server.post("/generate_plugin", tags=["插件生成器"])
async def generate_plugin(plugin_construction: models.PLUGIN_CONSTRUCTION):
    """
    #   自动生成插件接口
    """
    clearLog(clear_size=1)

    data = plugin_construction.dict()

    #   将特殊定义文件放到缓存下，等待SDK调用
    setLocalCache(data, "plugin_construction")

    os.system("chariot-plugin -ag {}".format(os.path.join("__sdkcache__", "plugin_construction.chariot-128.sdkc")))
    restartProgram("http", False)


@_rest_server.get("/plugin_data", tags=["插件生成器"])
async def get_plugin_data():
    """
    #   获取插件定义数据接口
    """
    plugin_data_path = os.path.join(os.getcwd(), "plugin.spec.json")

    if os.path.exists(plugin_data_path):
        plugin_data = json.load(open(plugin_data_path, "r"))
        return plugin_data

    else:
        content = {
            "error": "插件定义数据不存在"
        }
        return JSONResponse(content=content, status_code=404)


@_rest_server.post("/transpond", tags=["转发数据接收"])
async def receive_transponded(request: Request):
    """ 
    #   测试用接口，用于接收转发的数据
    """
    try:
        data = await request.body()
        log("info", f"获得转发数据：\n {data.decode()}")
        resp_data = {
            "msg": "接收成功",
            "error": ""
        }
        return JSONResponse(content=resp_data)
    except Exception as error:
        resp_data = {
            "msg": "接收失败",
            "error": str(error)
        }
        return JSONResponse(content=resp_data, status_code=500)


@_rest_server.get("/shutdown", tags=["API服务"])
async def shutdown():
    """
    #   关闭插件服务
    """
    global _triggers_process_list
    global _alarm_receivers_process_list
    global _indicator_receivers_process_list

    for process in _triggers_process_list:
        process.terminate()
        log("info", f"{process} shutdown")
    for process in _alarm_receivers_process_list:
        process.terminate()
        log("info", f"{process} shutdown")
    for process in _indicator_receivers_process_list:
        process.terminate()
        log("info", f"{process} shutdown")

    os.kill(os.getpid(), signal.SIGINT)


def runserver(plugin_object: object):
    global _plugins
    _plugins = plugin_object
    os.system("")
    log("attention", "在浏览器内输入 http://127.0.0.1:10001/docs 以进行接口测试")
    uvicorn.run(_rest_server, host="0.0.0.0", port=10001)
