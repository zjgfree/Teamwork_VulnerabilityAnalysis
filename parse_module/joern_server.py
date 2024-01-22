import subprocess, shlex, time
from cpgqls_client import CPGQLSClient
from config import tc_path, cpg_path, server_port


def kill_server():
    subprocess.run(
        "ps aux | grep 'joern-cli' | awk '{print $2}' | xargs kill -9",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def run_joern_parse():
    print("Running joern-parse...")
    start = time.perf_counter()
    subprocess.run(
        shlex.split(
            f"joern-parse {tc_path} -o {cpg_path} "
            f"--frontend-args --no-include-auto-discovery"
        ),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"Done, used {time.perf_counter() - start:<.2f}s\n")


def start_joern_server() -> CPGQLSClient:
    kill_server()                               # 强制终止其他joern-cli进程
    subprocess.Popen(                           # 启动新进程，并运行joern
        shlex.split(f"joern --server --server-port {server_port}"),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    run_joern_parse()                   # 解析文件

    server_endpoint = f"localhost:{server_port}"
    client = CPGQLSClient(server_endpoint)

    while True:
        try:
            client.execute("")
        except Exception:
            time.sleep(0.1)
            continue
        else:
            return client
