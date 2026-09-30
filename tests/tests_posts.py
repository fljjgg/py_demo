import requests
import pytest
from config.settings import BASE_URL, TIMEOUT
import yaml
from pathlib import Path

def load_cases():
    path = Path(__file__).parent.parent / "data" / "post_cases.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)["boundary_cases"]

@pytest.fixture
def api_client():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()

def test_get_post_detail(api_client):
    url = f"{BASE_URL}/posts/1"
    response = api_client.get(url, timeout=TIMEOUT)

    # 1. HTTP 层
    assert response.status_code == 200

    # 2. 结构层
    data = response.json()
    assert "id" in data
    assert "title" in data
    assert "body" in data

    # 3. 业务层
    assert data["id"] == 1
    assert isinstance(data["title"], str)

@pytest.mark.parametrize("case", load_cases())
def test_get_post_boundary_yaml(api_client, case):
    url = f"{BASE_URL}/posts/{case['post_id']}"
    response = api_client.get(url, timeout=TIMEOUT)
    assert response.status_code == case["expected_status"]


def test_post_missing_fields(api_client):
    """POST 缺少必填字段时的行为"""
    url = f"{BASE_URL}/posts"
    payload = {"title": "只有标题"}   # 故意缺 body 和 userId
    response = api_client.post(url, json=payload, timeout=TIMEOUT)
    # JSONPlaceholder 会返回 201，但真实项目应该断 400
    # 这里我们记录实际行为，面试时讲"我发现它没有做必填校验"
    assert response.status_code == 201
    data = response.json()
    assert "body" not in data or data.get("body") is None


def test_create_then_get(api_client):
    """创建一条数据，再用返回的 id 查询，验证一致性"""
    create_url = f"{BASE_URL}/posts"
    payload = {
        "title": "测试标题",
        "body": "测试内容",
        "userId": 1
    }
    create_resp = api_client.post(create_url, json=payload, timeout=TIMEOUT)
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["title"] == payload["title"]
    assert created["userId"] == payload["userId"]

    # 用返回的 id 查询
    new_id = created["id"]
    get_resp = api_client.get(f"{BASE_URL}/posts/{new_id}", timeout=TIMEOUT)

    assert get_resp.status_code == 404,"JSONPlaceholder 不持久化数据，预期返回 404"
    fetched = get_resp.json()
    assert fetched== {},"404 响应体应该为空 JSON"
