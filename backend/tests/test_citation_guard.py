from app.graph.citation_guard import apply_citation_guard, excerpt_supported
from app.schemas.common import Confidence, ContentType, FindingDraft, Label, SourceRecord


def make_source(url="https://example.test/p1", abstract="Stacked dies reach 1.2 TB/s of bandwidth in the synthetic test.", mock=False):
    return SourceRecord(
        url=url, source_name="Fixture", content_type=ContentType.PAPER,
        title="FIXTURE: Stacked memory", abstract=abstract, is_mock=mock,
    )


def draft(**kw):
    base = dict(claim="The paper reports stacked dies reaching 1.2 TB/s.", label=Label.VERIFIED_FACT,
                confidence=Confidence.HIGH)
    base.update(kw)
    return FindingDraft(**base)


def test_verified_fact_with_real_excerpt_is_kept():
    src = make_source()
    d = draft(source_ids=[src.id], supporting_excerpt="Stacked dies reach 1.2 TB/s of bandwidth")
    result = apply_citation_guard([d], {src.id: src})
    assert result.findings[0].label == Label.VERIFIED_FACT
    assert result.findings[0].confidence == Confidence.HIGH
    assert result.issues == []


def test_excerpt_matching_ignores_case_whitespace_and_ellipsis():
    src = make_source(abstract="Stacked dies reach 1.2 TB/s\n of bandwidth. Thermal limits remain the main obstacle.")
    assert excerpt_supported("stacked DIES reach 1.2 TB/s of bandwidth ... thermal limits remain the main obstacle", [src.searchable_text()])


def test_fabricated_excerpt_is_downgraded_not_dropped():
    src = make_source()
    d = draft(source_ids=[src.id], supporting_excerpt="This sentence never appears in the abstract at all")
    result = apply_citation_guard([d], {src.id: src})
    f = result.findings[0]
    assert f.label == Label.UNVERIFIED_CLAIM and f.confidence == Confidence.LOW
    assert "excerpt" in f.guard_note
    assert result.issues[0].action == "downgraded"


def test_missing_excerpt_is_downgraded():
    src = make_source()
    result = apply_citation_guard([draft(source_ids=[src.id], supporting_excerpt=None)], {src.id: src})
    assert result.findings[0].label == Label.UNVERIFIED_CLAIM


def test_invented_source_id_is_removed_and_fact_downgraded():
    result = apply_citation_guard([draft(source_ids=["src_doesnotexist"], supporting_excerpt="anything long enough here")], {})
    f = result.findings[0]
    assert f.source_ids == []
    assert f.label == Label.UNVERIFIED_CLAIM
    assert {i.action for i in result.issues} == {"removed_unknown_source_ids", "downgraded"}


def test_one_valid_and_one_invented_id_keeps_the_valid_one():
    src = make_source()
    d = draft(source_ids=[src.id, "src_fake", src.id], supporting_excerpt="Stacked dies reach 1.2 TB/s of bandwidth")
    f = apply_citation_guard([d], {src.id: src}).findings[0]
    assert f.source_ids == [src.id]
    assert f.label == Label.VERIFIED_FACT
    assert "unknown source id" in f.guard_note


def test_mock_sources_cannot_verify_facts():
    src = make_source(mock=True)
    d = draft(source_ids=[src.id], supporting_excerpt="Stacked dies reach 1.2 TB/s of bandwidth")
    assert apply_citation_guard([d], {src.id: src}).findings[0].label == Label.UNVERIFIED_CLAIM
    assert apply_citation_guard([d], {src.id: src}, allow_mock_verified=True).findings[0].label == Label.VERIFIED_FACT


def test_interpretations_and_forecasts_do_not_need_excerpts():
    src = make_source()
    items = [
        draft(label=Label.AI_INTERPRETATION, source_ids=[src.id], supporting_excerpt=None),
        draft(label=Label.FORECAST, source_ids=[], supporting_excerpt=None),
    ]
    result = apply_citation_guard(items, {src.id: src})
    assert [f.label for f in result.findings] == [Label.AI_INTERPRETATION, Label.FORECAST]
