#!/usr/bin/env python3
"""
mcd_client.py — 麦当劳中国 MCP 客户端（麦门海报工坊核心依赖）
封装 Streamable HTTP JSON-RPC 调用：initialize → tools/list → tools/call

用法:
    export MCD_TOKEN="你的MCP_Token"
    python3 mcd_client.py list                          # 列出全部工具
    python3 mcd_client.py call campaign-calendar        # 查当月活动
    python3 mcd_client.py call available-coupons        # 查可领优惠券
    python3 mcd_client.py call list-nutrition-foods     # 查营养数据
    python3 mcd_client.py call query-nearby-stores '{"longitude":121.47,"latitude":31.23,"orderType":1}'
"""
import json, os, sys, urllib.request, urllib.error

MCP_URL = os.environ.get("MCD_MCP_URL", "https://mcp.mcd.cn")
TOKEN = os.environ.get("MCD_TOKEN", "")
_id = [0]


def _headers():
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }


def rpc(method, params=None, notify=False):
    """发送 JSON-RPC 请求；自动兼容 SSE(data:) 与纯 JSON 两种响应格式"""
    _id[0] += 1
    body = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        body["params"] = params
    if not notify:
        body["id"] = _id[0]
    req = urllib.request.Request(MCP_URL, data=json.dumps(body).encode(), headers=_headers(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode("utf-8")
            if notify or not raw.strip():
                return {}
            if "data:" in raw:
                for line in raw.splitlines():
                    if line.startswith("data:"):
                        raw = line[5:].strip()
                        break
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:200]}") from e


def ensure_session():
    rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                       "clientInfo": {"name": "mcd-poster-studio", "version": "1.0.0"}})
    rpc("notifications/initialized", notify=True)


def call_tool(name, arguments=None):
    """调用 MCP 工具，返回拼接后的文本结果"""
    resp = rpc("tools/call", {"name": name, "arguments": arguments or {}})
    if "error" in resp:
        raise RuntimeError(f"工具 {name} 调用失败: {resp['error']}")
    content = resp.get("result", {}).get("content", [])
    return "\n".join(c.get("text", "") for c in content if c.get("type") == "text")


def main():
    if not TOKEN:
        print("❌ 请先 export MCD_TOKEN=你的Token（open.mcd.cn 控制台获取）")
        sys.exit(1)
    ensure_session()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        tools = rpc("tools/list", {}).get("result", {}).get("tools", [])
        print(f"共 {len(tools)} 个工具：")
        for t in tools:
            print(f"  - {t['name']}: {(t.get('description') or '').splitlines()[0][:60]}")
    elif cmd == "call":
        name = sys.argv[2]
        args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        print(call_tool(name, args))
    else:
        print(f"未知命令: {cmd}（支持 list / call）")
        sys.exit(1)


if __name__ == "__main__":
    main()
