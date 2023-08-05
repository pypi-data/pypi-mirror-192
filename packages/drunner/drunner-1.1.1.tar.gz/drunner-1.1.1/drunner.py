# encoding: utf-8
"""
pip install --editable .
"""
import os
import click
import json
import requests
import tarfile
import hashlib
import platform


AllowDeployType = [
    'notebook'
]
dRunnerStore = {
    'Darwin': f'{os.environ.get("HOME")}/Library/Application Support/drunner-python/',  # Mac,
    'Windows': f'{os.environ.get("APPDATA")}/drunner-python/'  # Windows
}
dRunnerServersFilename = 'servers-info.json'


def reset(tarinfo):
    """
        设置压缩包信息

        :param job_type:
        :param entrypoint:
        :param src:
    """
    tarinfo.uid = tarinfo.gid = 0
    tarinfo.uname = tarinfo.gname = "root"
    return tarinfo


def checksum(files):
    """
        计算文件校验码
    """
    m = hashlib.md5()
    for file in files:
        with open(file, "rb") as f:
            while chunk := f.read(128 * m.block_size):
                m.update(chunk)
    return m.hexdigest()


def zctar(tar_name, entrypoint, src):
    """
        压缩打包

        :param tar_name:
        :param entrypoint:
        :param src:
        :return: xxx.tar.gz
    """

    with tarfile.open(tar_name, "w:gz") as tar:
        tar.add(entrypoint, filter=reset)
        for filename in src:
            tar.add(filename, filter=reset)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Running command: drunner. I was invoked without subcommand')
    else:
        # click.echo(f"Running: drunner {ctx.invoked_subcommand}. I am about to invoke {ctx.invoked_subcommand}")
        pass


@cli.command()
@click.argument('job_type', type=str)
@click.argument('entrypoint', type=str)
@click.argument('src', nargs=-1)
@click.option('--python_version')
@click.option('--server_name', required=True, type=str, help="Registed server name.")
def deploy(job_type, entrypoint, src, python_version, server_name):
    """
        drunner deploy <type> to create a job.
        rsconnect deploy notebook x.ipynb db.py -n connect -a 14d06f33-a222-408a-b0aa-614d98642ba

        ------
        drunner deploy notebook start.ipynb hello.py hello.txt 1.html l.jpg requirements.txt --python_version 3.6
        drunner deploy notebook start.ipynb hello.py hello.txt 1.html l.jpg requirements.txt --python_version 3.6 --server_name myDevelop
    """

    # 参数校验
    validate_args(job_type, entrypoint, src)

    # 获取用户信息、获取服务信息
    ukey, server_url = _get_server_info(server_name)

    # 计算摘要
    hexdigest_code = checksum([entrypoint] + list(src))
    # print(f"文件校验码：{hexdigest_code}")

    # 压缩
    tar_name = hexdigest_code + '.tar.gz'
    zctar(tar_name, entrypoint, src)
    # print(f"压缩包名称：{tar_name}")

    # 上传压缩包 TODO faster
    upload_status = upload_tar(tar_name, dRunnerSever=server_url)
    if upload_status is False:
        print(f"压缩包上传失败, {tar_name}")
        exit(1)
    # print(f"已上传压缩包：{upload_status}")

    # 创建Job
    TAG = job_create(job_type, entrypoint, src, python_version, hexdigest_code, tar_name, ukey, dRunnerSever=server_url)
    if not TAG:
        print("无法创建Job")
        exit(1)
    print(f"已创建, Tag: {TAG}, 稍后可在首页查看")


def validate_args(job_type, entrypoint, src):
    """
        CLI 参数校验

        :param job_type:
        :param entrypoint:
        :param src:
    """

    if job_type not in AllowDeployType:
        print(f"TypeNotAllowed: {job_type}")
        exit(1)
    if not isinstance(entrypoint, str):
        print(f"Entrypoint must be a string. TypeError: {entrypoint}")
        exit(1)
    if 'requirements.txt' not in src:
        print("Error: NotFound requirements.txt")
        exit(1)


def upload_tar(tar_name, file_type='.tar.gz', dRunnerSever=None):
    """
        上传

        :param job_type:
        :param entrypoint:
        :param src:
    """

    files = {
        'file': open(tar_name, 'rb')
    }
    data = {
        "file_name": tar_name,
        "file_type": file_type
    }

    try:
        res = requests.post(f'{dRunnerSever}/upload/tar', files=files, data=data)
        # print(res.json())
    except Exception as ei:
        print(ei)
        return False
    return True


def job_create(job_type, entrypoint, src, python_version, hexdigest_code, key, ukey, dRunnerSever=None):
    """
        Job 创建

        :param job_type:
        :param entrypoint:
        :param src:
    """

    data = {
        "jobtype": job_type,
        "python_version": python_version if python_version else "3.8",
        "entrypoint": entrypoint,
        "user_key": ukey,
        "file_fingerprinting": hexdigest_code,
        "schedule": {  # 初始化
            "every": 365,
            "period": "days"
        },
        "parameters": {},
        "start": "no",
        "key": key  # s3 bucket.key
    }

    try:
        res = requests.post(f'{dRunnerSever}/job/crud', json=data)
        # print(res.json())
    except Exception as ei:
        print(ei)
        return False
    return res.json().get("data").get("TAG")


def _get_system():
    return platform.system()


def _get_server_info(server_name=None):
    """
        获取server info
            - ukey
            - server url

        :param server_name:
    """

    dRunnerStorePath = dRunnerStore[_get_system()]
    if not os.path.exists(f"{dRunnerStorePath}{dRunnerServersFilename}"):
        raise Exception(f"No such file or directory: {dRunnerStorePath}{dRunnerServersFilename}, please initialize server first.")

    with open(f'{dRunnerStorePath}{dRunnerServersFilename}', 'r') as fr:
        content = json.loads(fr.read())

    if not list(content.keys()):  # 当前配置下无任何server
        raise Exception("Please initialize server first.")

    if server_name is not None and server_name not in content.keys():  # server未做初始化
        raise Exception(f"{server_name} no exists, please initialize server first.")

    if server_name is None:
        # 未指定--server_name, 默认返回第一个
        return (content[list(content.keys())[0]]["ukey"], content[list(content.keys())[0]]["server_url"])

    return (content[server_name]["ukey"], content[server_name]["server_url"])


@cli.command()
@click.option('--server', required=True, type=str, help="The target server url.")
@click.option('--server_name', required=True, type=str, help="The server name.")
@click.option('--ukey', required=True, type=str, help="User unique auth.")
def init(server, server_name, ukey):
    """
        Server init, save user information to operating system.

        保存用户info到系统目录

        Platform	    Location

        Mac	            $HOME/Library/Application Support/rsconnect-python/
        Linux	        $HOME/.rsconnect-python/ or $XDG_CONFIG_HOME/rsconnect-python/
        Windows	        $APPDATA/rsconnect-python

        >>> import platform
        >>> platform.system()  # mac: Darwin, ubuntu: Linux, windows: Windows


        rsconnect add --server https://my.connect.server/ --name myServer --api-key $CONNECT_API_KEY

        ------
        drunner init --server https://my.connect.server/ --server_name myDevelop --ukey cfd7a41fc0ac3107aa74c85f43cf9de0
    """
    # mkdir dRunner-python
    # touch init-config.json

    # 创建文件目录
    dRunnerStorePath = dRunnerStore[_get_system()]
    if not os.path.exists(dRunnerStorePath):
        os.mkdir(dRunnerStorePath)

    if os.path.exists(dRunnerStorePath):
        if not os.path.exists(f'{dRunnerStorePath}{dRunnerServersFilename}'):
            # 首次写入
            with open(f'{dRunnerStorePath}{dRunnerServersFilename}', 'w') as fp:
                fp.write(
                    json.dumps({
                        server_name: {
                            "server_name": server_name,
                            "ukey": ukey,
                            "server_url": server
                        }
                    })
                )
        else:
            # 追加server
            with open(f'{dRunnerStorePath}{dRunnerServersFilename}', 'r') as fr:
                content = json.loads(fr.read())
            if server_name in content.keys():
                raise Exception(f"{server_name} already exists.")

            content[server_name] = {
                "server_name": server_name,
                "ukey": ukey,
                "server_url": server
            }
            with open(f'{dRunnerStorePath}{dRunnerServersFilename}', 'w') as fp:
                fp.write(json.dumps(content))
    else:
        raise Exception(f"{dRunnerStorePath} directory no exists, initialize failed.")

    print("Initialize successful.")
