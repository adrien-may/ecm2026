def test_page_uses_expected_template(client, captured_templates):
    client.get("/bonjour", query_string={"name": "Samira"})
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "hello.html"
    assert context["name"] == "Samira"
