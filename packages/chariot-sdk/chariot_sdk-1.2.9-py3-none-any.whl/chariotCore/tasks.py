from chariotCore import VERSION
from chariotCore.tools import *
from chariotCore.templates import *
import traceback


def generate(work_path: str, file_path: str):
    """
    #   生成插件
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    file_path:str,    #   插件定义文件相对路径

    #   生成失败时显示错误log，并返回
    """

    log("info", f"正在使用千乘插件开发工具 v{VERSION} 生成插件")

    try:

        #   读取插件定义文件
        data = readGenerateFile(work_path, file_path)

        #   在没有任何功能的数据和非自动生成插件的情况下
        if not (data.get("actions") or data.get("triggers") or data.get("alarm_receivers") or data.get(
                "indicator_receivers")):

            log("info", "未检测到任何功能的数据，需要生成自适应Request插件吗？[Y/N]")

            if input() != "Y":
                log("info", "已结束生成")
                return

            #   生成基础文件
            generateBaseFile(work_path)

            #   生成入口文件 main.py 用于给千乘执行
            plugin_name = "auto_generator"
            generateMainFile(work_path, plugin_name, [], [], [], [])

            #   生成存储热更新包的文件夹，自动生成插件包后将放置在这里
            generateUpdateFile(work_path)

            return

        #   生成基础文件
        generateBaseFile(work_path)

        #   生成自定义类
        types = data.get("types")
        if types:
            #   生成自定义类的校验数据
            types_model = generateTypesModel(types)
        else:
            types_model = ""
            log("attention", "未检测到自定义类型，跳过自定义类型校验数据的生成")

        #   生成connection
        connection_params = data.get("connection")
        if connection_params:
            #   生成连接器的校验数据
            connection_model = generateConnectionModel(connection_params)
            #   获取参数列表，用于生成功能文件
            connection_keys = list(connection_params.keys())
        else:
            #   没有连接器也需要生成空的校验数据，因为在所有模块中都默认导入连接器类
            connection_model = generateConnectionModel({})
            connection_keys = []
            log("attention", "未检测到连接器，跳过连接器的生成")

        #   生成tests文件夹
        tests_path = os.path.join(work_path, "tests")
        if not os.path.exists(tests_path):
            os.mkdir(tests_path)

        #   检测旧版本
        updateModuleFile(work_path)

        #   生成actions
        actions = data.get("actions")
        if actions:
            #   生成动作的校验数据
            actions_model = generateModel("actions", actions)
            #   组合校验文件数据
            actions_model = model_header + types_model + connection_model + actions_model
            #   生成动作的校验文件
            generateModelFile(work_path, "actions", actions_model)
            #   生成动作的所有功能文件，返回所有动作的列表用于生成入口文件
            actions_list = generateModuleFile(work_path, "actions", actions, connection_keys)
        else:
            actions_list = []
            log("attention", "未检测到动作，跳过动作的生成")

        #   生成triggers
        triggers = data.get("triggers")
        if triggers:
            #   生成触发器的校验数据
            triggers_model = generateModel('triggers', triggers)
            #   组合校验文件数据
            triggers_model = model_header + types_model + connection_model + triggers_model
            #   生成触发器的校验文件
            generateModelFile(work_path, "triggers", triggers_model)
            #   生成触发器的所有功能文件，返回所有触发器的列表用于生成入口文件
            triggers_list = generateModuleFile(work_path, "triggers", triggers, connection_keys)
        else:
            triggers_list = []
            log("attention", "未检测到触发器，跳过触发器的生成")

        #   生成indicator_receivers
        indicator_receivers = data.get("indicator_receivers")
        if indicator_receivers:
            #   生成情报接收器的校验数据
            indicator_receivers_model = generateModel('indicator_receivers', indicator_receivers)
            #   组合校验文件数据
            indicator_receivers_model = model_header + indicator_receivers_model_types + types_model + connection_model + indicator_receivers_model
            #   生成情报接收器的校验文件
            generateModelFile(work_path, "indicator_receivers", indicator_receivers_model)
            #   生成情报接收器的所有功能文件，返回所有情报接收器的列表用于生成入口文件
            indicator_receivers_list = generateModuleFile(work_path, "indicator_receivers", indicator_receivers,
                                                          connection_keys)
        else:
            indicator_receivers_list = []
            log("attention", "未检测到情报接收器，跳过情报接收器的生成")

        #   生成alarm_receivers
        alarm_receivers = data.get("alarm_receivers")
        if alarm_receivers:
            #   生成告警接收器的校验数据
            alarm_receivers_model = generateModel('alarm_receivers', alarm_receivers)
            #   组合校验文件数据
            alarm_receivers_model = model_header + alarm_receivers_model_types + types_model + connection_model + alarm_receivers_model
            #   生成告警接收器的校验文件
            generateModelFile(work_path, "alarm_receivers", alarm_receivers_model)
            #   生成告警接收器的所有功能文件，返回所有告警接收器的列表用于生成入口文件
            alarm_receivers_list = generateModuleFile(work_path, "alarm_receivers", alarm_receivers, connection_keys)
        else:
            alarm_receivers_list = []
            log("attention", "未检测到告警接收器，跳过告警接收器的生成")

        #   生成入口文件 main.py
        plugin_name = data.get("name")
        generateMainFile(work_path, plugin_name, actions_list, triggers_list, indicator_receivers_list,
                         alarm_receivers_list)

        #   生成本地REST测试服务器文件
        # generateTestServerFile(work_path,actions_list,triggers_list,indicator_receivers_list,alarm_receivers_list)

        #   生成帮助文件
        generateHelpFile(work_path, data)

        #   生成通用文件存储的文件夹
        generateUtilFile(work_path)

        #   生成存储热更新包的文件夹
        generateUpdateFile(work_path)

    except Exception as error:
        log("error", error)
        return

    log("info", "所有插件文件生成完成")


def autoGenerate(work_path, file_path):
    """
    #   生成插件
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    file_path:str,    #   特殊定义文件相对路径

    #   生成失败时显示错误log，并返回
    """
    log("info", f"正在使用千乘插件开发工具 v{VERSION} 自动生成插件中")

    try:

        log("info", "读取插件数据中")

        try:
            file_readbytes = open(os.path.join(work_path, file_path), "rb").read()
            data = json.loads(file_readbytes.decode())
        except Exception as error:
            raise Exception(f"读取插件数据失败\n  失败原因：{error}")

        log("info", "读取完成")

        #   生成tests文件夹
        tests_path = os.path.join(work_path, "tests")
        if not os.path.exists(tests_path):
            os.mkdir(tests_path)

        #   转换插件特殊定义文件
        trans_data = autoGenerateDataTrans(data)
        #   生成一般插件定义文件
        autoGeneratePluginSpecFile(trans_data)
        #   生成校验数据
        actions_model = generateModel("actions", trans_data.get("actions"))
        #   生成连接器校验数据
        connection_model = generateConnectionModel(trans_data.get("connection", {}))
        #   组合校验文件数据
        actions_model = model_header + connection_model + actions_model
        #   生成校验文件
        generateModelFile(work_path, "actions", actions_model)
        #   生成动作文件
        actions_list = autoGenerateActionsFile(work_path, trans_data)
        #   生成入口文件 main.py
        plugin_name = data.get("name")
        generateMainFile(work_path, plugin_name, actions_list, [], [], [])

        #   生成本地REST测试服务器文件
        # generateTestServerFile(work_path,actions_list,[],[],[])

        #   生成帮助文件
        generateHelpFile(work_path, data)

        #   生成通用文件存储的文件夹
        generateUtilFile(work_path)

        #   生成存储热更新包的文件夹
        generateUpdateFile(work_path)

    except Exception as error:
        log("error", error)
        print(traceback.format_exc())
        return


def generateYaml(work_path: str):
    """
    #   在当前工作目录下生成一个yaml模板文件
    参数说明：
    work_path:str,    #   当前工作区绝对路径

    """
    try:
        #   获取res文件夹
        res_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "res")
        #   获取plugin.spec.yaml模板文件
        yaml_template = os.path.join(res_dir, "plugin.spec.yaml")
        #   生成位置
        file_path = os.path.join(work_path, "plugin.spec.yaml")

        #   若文件存在则跳过生成
        if os.path.exists(file_path):
            log("attention", rf"\plugin.spec.yaml 已存在，跳过生成")
            return
        else:
            shutil.copy2(yaml_template, file_path)
        log("info", rf"\plugin.spec.yaml 生成完成")
    except Exception as error:
        raise Exception(rf"\plugin.spec.yaml 生成失败，错误未知：" + f"\n{error}")


def run(work_path: str, test_path: str):
    """
    #   运行插件指定功能
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    test_path:str,    #   测试用的数据文件的相对路径

    """

    log("info", f"正在根据 {test_path} 的数据运行功能")

    main_path = os.path.join(work_path, "main.py")

    test_path = os.path.join(work_path, test_path)

    if not os.path.exists(test_path):
        raise Exception(f"测试文件路径错误：\n{test_path}")

    else:
        cmd = f"python {main_path} run {test_path}"
        os.system(cmd)


def http(work_path: str):
    """
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    """
    main_path = os.path.join(work_path, "main.py")

    cmd = f"python {main_path} http"
    os.system(cmd)


def test(work_path: str, tests: str):
    """
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    tests:str,    #   测试用的数据文件的相对路径
    """
    main_path = os.path.join(work_path, "main.py")
    test_path = os.path.join(work_path, tests)

    if not os.path.exists(test_path):
        logging.error(f"请正确输入路径")

    cmd = f"python {main_path} test {test_path}"
    os.system(cmd)


def tarball(work_path: str):
    """
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    """
    Makefile_path = os.path.join(work_path, "Makefile")
    if os.path.exists(Makefile_path):
        cmd = "make tarball"
        os.system(cmd)


def mkimg(work_path: str):
    """
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    """
    Makefile_path = os.path.join(work_path, "Makefile")
    if os.path.exists(Makefile_path):
        cmd = "make image"
        os.system(cmd)


def testserver(work_path: str):
    """
    **此方法暂时弃用**

    参数说明：
    work_path:str,    #   当前工作区绝对路径
    """
    testserver_path = os.path.join(work_path, "testserver.py")

    cmd = f"python {testserver_path}"
    os.system(cmd)
