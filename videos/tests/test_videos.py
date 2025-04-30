# videos/tests/test_videos.py
import pytest
import tempfile, shutil
from django.urls import reverse
from rest_framework.test import APIClient
from videos.helpers import CSV_PATH, write_all, FIELDNAMES

@pytest.fixture(autouse=True)
def use_temp_csv(tmp_path, monkeypatch):
    # redirect CSV_PATH to a temp file
    tmp = tmp_path / "videos.csv"
    # write header only
    tmp.write_text("\t".join(FIELDNAMES)+"\n")
    monkeypatch.setattr("videos.helpers.CSV_PATH", tmp)
    return tmp

client = APIClient()

def make_item(i):
    return {
        "source_post_id": str(1000+i),
        "post_url": f"https://x/{i}",
        "post_description": f"desc{i}",
        "post_created": "01/01/20",
        "likes_count": i,
        "shares_count": i,
        "views_count": i*10,
        "comments_count": i,
    }

def test_create_and_get():
    url = reverse("video-list-create")
    data = make_item(1)
    resp = client.post(url, data, format="json")
    assert resp.status_code == 201
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.json()[0]["source_post_id"] == "1001"

def test_unique_constraint():
    url = reverse("video-list-create")
    client.post(url, make_item(2), format="json")
    resp = client.post(url, make_item(2), format="json")
    assert resp.status_code == 400
    assert "must be unique" in resp.json()["source_post_id"][0]

def test_update_and_delete():
    url = reverse("video-list-create")
    client.post(url, make_item(3), format="json")
    detail = reverse("video-detail", args=["1003"])
    upd = make_item(30)
    resp = client.put(detail, upd, format="json")
    assert resp.status_code == 200
    assert resp.json()["likes_count"] == 30
    resp = client.delete(detail)
    assert resp.status_code == 204
    # now 404
    resp = client.delete(detail)
    assert resp.status_code == 404

def test_sorting():
    url = reverse("video-list-create")
    client.post(url, make_item(1), format="json")
    client.post(url, make_item(2), format="json")
    resp = client.get(url + "?sort_by=views_count&order=desc")
    data = resp.json()
    assert data[0]["views_count"] >= data[1]["views_count"]
