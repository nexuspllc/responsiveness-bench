from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]


def test_annotation_guide_leads_with_compatibility_test() -> None:
    guide = (ROOT / "docs" / "annotation-guide.md").read_text(encoding="utf-8")

    assert "## Compatibility test" in guide
    assert "Assume everything the response asserts is true" in guide
    assert "can the claim layer still be true" in guide
    assert guide.index("## Compatibility test") < guide.index("## Claim layers")
    assert "narrows_within_scope" in guide
    assert "scope_mismatch" in guide
    assert "backed" in guide
    assert "contested" in guide


def test_readme_publishes_measurement_and_exploit_audit() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "Inference mode" in readme
    assert "Structure-flip rate" in readme
    assert "Content Effect" in readme
    assert "Directional Asymmetry" in readme
    assert "always_request_evidence" in readme
    assert "63.64%" in readme
    assert "33 cases" in readme
    assert "11" in readme


def test_ci_enforces_full_gate_and_exploit_audit() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(
        encoding="utf-8"
    )

    assert "pytest" in workflow
    assert "compileall" in workflow
    assert "validate data/seed" in workflow
    assert "audit data/seed --check" in workflow


def test_release_version_is_protocol_v2() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")

    assert 'version = "0.2.0"' in pyproject
    assert "version: 0.2.0" in citation


def test_repository_contains_no_process_or_promotion_layer() -> None:
    forbidden_names = {"AGENTS.md", "HANDOFF.md", "substack-note.md"}
    assert not any(path.name in forbidden_names for path in ROOT.rglob("*"))

    forbidden_phrases = (
        "substack",
        "chatgpt",
        "human-ai collaboration",
        "ai-assisted",
        "publication draft",
    )
    text_suffixes = {".md", ".txt", ".toml", ".yml", ".yaml", ".py", ".json", ".cff"}
    for path in ROOT.rglob("*"):
        if (
            ".git" in path.parts
            or path == Path(__file__)
            or not path.is_file()
            or path.suffix not in text_suffixes
        ):
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        assert not any(phrase in lowered for phrase in forbidden_phrases), path

@pytest.mark.parametrize(
    "relative_path",
    ["results/run-a/README.md", "results/run-b/README.md"],
)
def test_result_provenance_can_name_the_model_surface(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, relative_path: str
) -> None:
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True)
    path.write_text("Surface: ChatGPT. Model: example.\n", encoding="utf-8")
    monkeypatch.setattr(__name__ + ".ROOT", tmp_path)

    test_repository_contains_no_process_or_promotion_layer()


@pytest.mark.parametrize(
    "relative_path",
    [
        "README.md",
        "docs/method-note.md",
        "results/README.md",
        "results/run-a/notes.md",
        "results/run-a/nested/README.md",
    ],
)
def test_model_surface_exception_is_confined_to_run_readmes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, relative_path: str
) -> None:
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("Surface: ChatGPT.\n", encoding="utf-8")
    monkeypatch.setattr(__name__ + ".ROOT", tmp_path)

    with pytest.raises(AssertionError):
        test_repository_contains_no_process_or_promotion_layer()


@pytest.mark.parametrize(
    "phrase",
    ["substack", "human-ai collaboration", "ai-assisted", "publication draft"],
)
def test_result_provenance_keeps_other_hygiene_restrictions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, phrase: str
) -> None:
    path = tmp_path / "results" / "run-a" / "README.md"
    path.parent.mkdir(parents=True)
    path.write_text(phrase + "\n", encoding="utf-8")
    monkeypatch.setattr(__name__ + ".ROOT", tmp_path)

    with pytest.raises(AssertionError):
        test_repository_contains_no_process_or_promotion_layer()
