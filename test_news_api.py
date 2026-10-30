import app as backend


def test_news_endpoint_returns_structured_current_affairs(monkeypatch):
    expected = {
        "date": "2026-10-30",
        "date_label": "Friday, 30 October 2026",
        "total": 1,
        "categories": [
            {
                "key": "national",
                "label": "National · India",
                "articles": [{"title": "India news", "source": "Test Wire"}],
            }
        ],
        "message": "",
        "summary": "Current affairs for 30 October 2026. Found 1 headline(s).",
        "feeds": [],
    }
    monkeypatch.setattr(
        backend,
        "fetch_current_affairs",
        lambda query, date_override=None: (expected, 200),
    )

    response = backend.app.test_client().post(
        "/api/news",
        json={
            "query": "30 October 2026 current affairs international and national India",
            "date": "2026-10-30",
        },
    )

    assert response.status_code == 200
    assert response.json["date"] == "2026-10-30"
    assert response.json["categories"][0]["articles"][0]["title"] == "India news"


def test_news_endpoint_rejects_empty_query():
    response = backend.app.test_client().post("/api/news", json={"query": "  "})
    assert response.status_code == 400
    assert response.json["error"] is True