import json
from pathlib import Path

import httpx

# BASE_URL = "http://127.0.0.1:5031/"
BASE_URL = "https://shiping.djpsd.com/"

API_KEY = "自己的apikey"
ROOT_PATH = Path(__file__).resolve().parent
参考图列表 = ["1.jpg", "2.png"]


def main():
    with httpx.Client(timeout=30) as client:
        查询模型列表(client)
        rules = 获取启用扣费规则(client)
        image_urls = 上传参考图列表(client)
        relay_image_urls = 中转上传参考图列表(client)
        relay_task_ids = 创建中转视频测试用例(client, relay_image_urls)
        relay_task_ids.extend(创建中转生图测试用例(client, rules, relay_image_urls))
        for task_id in relay_task_ids:
            查询中转任务(client, task_id)
        task_ids = 创建视频测试用例(client, rules, image_urls)
        for task_id in task_ids:
            查询任务(client, task_id)
        if task_ids:
            查询任务列表(client, len(task_ids))
        测试无效key创建任务(client)
        测试无效key创建中转任务(client)
        测试无效key查询任务列表(client)
        测试无效key查询中转任务(client)
        测试无效任务查询(client)


def 读取参考图路径():
    return [ROOT_PATH / name for name in 参考图列表]


def 上传参考图列表(client):
    urls = []
    for image_path in 读取参考图路径():
        with image_path.open("rb") as fp:
            files = {"file": (image_path.name, fp, "image/jpeg" if image_path.suffix.lower() == ".jpg" else "image/png")}
            response = client.post(f"{BASE_URL}task/upload", files=files, headers={"api-key": API_KEY})
        data = 打印结果("api_key上传参考图{}".format(image_path.name), response)
        item = data.get("data") or {}
        url = item.get("url") or ""
        if url:
            urls.append(url)
    return urls


def 中转上传参考图列表(client):
    urls = []
    for image_path in 读取参考图路径():
        with image_path.open("rb") as fp:
            files = {"file": (image_path.name, fp, "image/jpeg" if image_path.suffix.lower() == ".jpg" else "image/png")}
            response = client.post(f"{BASE_URL}v1/media/upload", files=files, headers={"Authorization": f"Bearer {API_KEY}"})
        data = 打印结果("v1上传参考图{}".format(image_path.name), response)
        url = data.get("url") or ""
        if url:
            urls.append(url)
    return urls


def 获取启用扣费规则(client):
    response = client.get(f"{BASE_URL}task/cost-rules")
    data = 打印结果("启用扣费规则", response)
    return data.get("data") or []


def 查询模型列表(client):
    response = client.get(f"{BASE_URL}v1/models")
    打印结果("v1模型列表", response)


def 规则索引(rules):
    mapping = {}
    for rule in rules:
        key = (
            str(rule.get("task_type") or ""),
            str(rule.get("resolution_tier") or ""),
            int(rule.get("duration_seconds") or 0),
        )
        mapping[key] = rule
    return mapping


def 创建中转视频测试用例(client, image_urls):
    cases = [{
        "title": "v1单图参考视频任务",
        "payload": {
            "model": "video-v1",
            "prompt": "测试v1单图参考视频任务-10秒",
            "params": {
                "duration": 10,
                "aspect_ratio": "16:9",
                "images": image_urls[:1],
            },
        },
    }]
    if len(image_urls) >= 2:
        cases.append({
            "title": "v1双图参考视频任务",
            "payload": {
                "model": "video-v1",
                "prompt": "测试v1双图参考视频任务-10秒",
                "params": {
                    "duration": 10,
                    "aspect_ratio": "16:9",
                    "images": image_urls[:2],
                },
            },
        })
    task_ids = []
    for case in cases:
        response = client.post(f"{BASE_URL}v1/media/generate", json=case["payload"], headers={"x-api-key": API_KEY})
        data = 打印结果(case["title"], response)
        task_id = data.get("task_id")
        if task_id:
            task_ids.append(task_id)
    return task_ids


def 创建中转生图测试用例(client, rules, image_urls):
    rule_map = 规则索引(rules)
    cases = []
    for model, task_type, tier, title in [
        ("image-v1", "image", "", "v1基础生图任务"),
        ("image-v1-2k", "image_2k", "2k", "v1 2K生图任务"),
        ("image-v1-4k", "image_4k", "4k", "v1 4K生图任务"),
    ]:
        if (task_type, tier, 0) not in rule_map:
            continue
        cases.append({
            "title": title,
            "payload": {
                "model": model,
                "prompt": "{}-接口测试".format(title),
                "params": {
                    "aspect_ratio": "16:9",
                    "images": image_urls[:1],
                },
            },
        })
    task_ids = []
    for case in cases:
        response = client.post(f"{BASE_URL}v1/media/generate", json=case["payload"], headers={"x-api-key": API_KEY})
        data = 打印结果(case["title"], response)
        task_id = data.get("task_id")
        if task_id:
            task_ids.append(task_id)
    return task_ids


def 创建视频测试用例(client, rules, image_urls):
    rule_map = 规则索引(rules)
    cases = []

    if ("video", "", 10) in rule_map:
        cases.append({
            "title": "普通10秒视频任务",
            "payload": {
                "api_key": API_KEY,
                "prompt": "测试视频任务-10秒",
                "task_type": "video",
                "extra_params": json.dumps({
                    "ratio": "16:9横屏",
                    "duration": 10,
                }, ensure_ascii=False),
            },
        })

    if len(image_urls) >= 2 and ("video", "", 10) in rule_map:
        cases.append({
            "title": "带参考图10秒视频任务",
            "payload": {
                "api_key": API_KEY,
                "prompt": "测试带参考图视频任务-10秒",
                "image_url": json.dumps(image_urls, ensure_ascii=False),
                "task_type": "video",
                "extra_params": json.dumps({
                    "ratio": "16:9横屏",
                    "duration": 10,
                }, ensure_ascii=False),
            },
        })

    if ("video", "", 5) in rule_map:
        cases.append({
            "title": "5秒视频任务",
            "payload": {
                "api_key": API_KEY,
                "prompt": "测试视频任务-5秒",
                "task_type": "video",
                "extra_params": json.dumps({
                    "ratio": "16:9横屏",
                    "duration": 5,
                }, ensure_ascii=False),
            },
        })

    if ("video", "", 15) in rule_map:
        cases.append({
            "title": "15秒视频任务",
            "payload": {
                "api_key": API_KEY,
                "prompt": "测试视频任务-15秒",
                "task_type": "video",
                "extra_params": json.dumps({
                    "ratio": "16:9横屏",
                    "duration": 15,
                }, ensure_ascii=False),
            },
        })

    task_ids = []
    for case in cases:
        response = client.post(f"{BASE_URL}api/v1/video-jobs", json=case["payload"])
        data = 打印结果(case["title"], response)
        task = data.get("data") or {}
        task_id = task.get("id")
        if task_id:
            print("task_id=", task_id, "callback_url=", task.get("callback_url", ""))
            task_ids.append(task_id)
    return task_ids


def 测试无效key创建任务(client):
    response = client.post(
        f"{BASE_URL}api/v1/video-jobs",
        json={
            "api_key": "invalid-key",
            "prompt": "测试无效key",
            "task_type": "video",
            "extra_params": json.dumps({"ratio": "16:9横屏", "duration": 10}, ensure_ascii=False),
        },
    )
    打印结果("无效key创建任务", response)


def 测试无效key创建中转任务(client):
    response = client.post(
        f"{BASE_URL}v1/media/generate",
        json={
            "model": "video-v1",
            "prompt": "测试v1无效key",
            "params": {"duration": 10, "aspect_ratio": "16:9", "images": []},
        },
        headers={"api-key": "invalid-key"},
    )
    打印结果("v1无效key创建任务", response)


def 测试无效key查询任务列表(client):
    response = client.get(
        f"{BASE_URL}api/v1/video-jobs?page=1&page_size=20&status=",
        headers={"api-key": "invalid-key"},
    )
    打印结果("无效key查询任务列表", response)


def 测试无效任务查询(client):
    response = client.get(
        f"{BASE_URL}api/v1/video-jobs/999999999",
        headers={"api-key": API_KEY},
    )
    打印结果("不存在任务查询", response)


def 测试无效key查询中转任务(client):
    response = client.get(
        f"{BASE_URL}v1/media/status?task_id=1",
        headers={"x-api-key": "invalid-key"},
    )
    打印结果("v1无效key查询任务", response)


def 查询任务(client, task_id):
    response = client.get(
        f"{BASE_URL}api/v1/video-jobs/{task_id}",
        headers={"api-key": API_KEY},
    )
    打印结果("有效key查询任务", response)


def 查询中转任务(client, task_id):
    response = client.get(
        f"{BASE_URL}v1/media/status?task_id={task_id}",
        headers={"x-goog-api-key": API_KEY},
    )
    data = 打印结果("v1查询任务", response)
    if "status_group" in data:
        print("错误：v1状态响应不应包含 status_group")


def 查询任务列表(client, page_size):
    response = client.get(
        f"{BASE_URL}api/v1/video-jobs?page=1&page_size={max(page_size, 20)}&status=",
        headers={"api-key": API_KEY},
    )
    打印结果("有效key查询任务列表", response)


def 打印结果(title, response):
    print(f"\n=== {title} ===")
    print("status=", response.status_code)
    try:
        data = response.json()
    except Exception:
        print(response.text)
        return {}
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return data


if __name__ == "__main__":
    main()
