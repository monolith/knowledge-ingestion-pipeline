"""Tests for Pass 0's rich-format handlers -- PDF, DOCX, PPTX, XLSX, email.

These are the README's headline capability and they had no test at all. Their
failure mode is the dangerous kind: `normalize_sources` catches PipelineError
and quarantines, so a broken parser produces a GREEN run with a silently dropped
document rather than a crash anyone would notice.

Each fixture is built in the test rather than committed as a binary, so the
suite stays readable and the inputs stay inspectable. The PDF is hand-written
because no PDF writer is installed here and the format's text-drawing subset is
small enough to emit directly; pypdf reads it the same way it reads any other.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from kip.artifacts import PipelineError, RunContext
from kip.normalize import build_locator_map, normalize_sources, source_id_for

pypdf = pytest.importorskip("pypdf")
docx = pytest.importorskip("docx")
pptx = pytest.importorskip("pptx")
openpyxl = pytest.importorskip("openpyxl")


@pytest.fixture
def ctx(tmp_path: Path) -> RunContext:
    return RunContext(run_id="run-rich", root=tmp_path / "ws")


def write_pdf(path: Path, pages: list[list[str]]) -> None:
    """A minimal, valid, text-bearing PDF. Only the drawing subset is needed."""
    body: list[str] = []
    font_object = 3 + 2 * len(pages)
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(len(pages)))
    body.append("<< /Type /Catalog /Pages 2 0 R >>")
    body.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>")
    for index, lines in enumerate(pages):
        content = (
            "BT /F1 12 Tf 72 720 Td 14 TL\n"
            + "\n".join(f"({line}) Tj T*" for line in lines)
            + "\nET"
        )
        body.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Contents {4 + 2 * index} 0 R "
            f"/Resources << /Font << /F1 {font_object} 0 R >> >> >>"
        )
        body.append(f"<< /Length {len(content)} >>\nstream\n{content}\nendstream")
    body.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    out = "%PDF-1.4\n"
    offsets: list[int] = []
    for number, obj in enumerate(body, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n{obj}\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(body) + 1}\n0000000000 65535 f \n"
    out += "".join(f"{offset:010d} 00000 n \n" for offset in offsets)
    out += f"trailer\n<< /Size {len(body) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    path.write_bytes(out.encode("latin-1"))


def only(registry: list[dict]) -> dict:
    assert len(registry) == 1, registry
    return registry[0]


def normalized_text(ctx: RunContext, record: dict) -> str:
    return (ctx.run_dir / record["normalized_path"]).read_text(encoding="utf-8")


def test_pdf_normalizes_with_page_markers(ctx: RunContext, tmp_path: Path):
    source = tmp_path / "report.pdf"
    write_pdf(source, [["Latency fell to 12 ms after the rebuild."], ["Second page body."]])

    record = only(normalize_sources(ctx, [source]))
    assert record["normalization_status"] == "success", record["warnings"]
    assert record["normalizer"] == "rich_v1"
    assert record["media_type"] == "application/pdf"

    text = normalized_text(ctx, record)
    assert "[[PAGE 1]]" in text and "[[PAGE 2]]" in text
    assert "Latency fell to 12 ms after the rebuild." in text
    assert "Second page body." in text


def test_pdf_locators_round_trip_to_the_right_page(ctx: RunContext, tmp_path: Path):
    """Spec §8.6: an excerpt must resolve back to a page, by exact offsets."""
    source = tmp_path / "report.pdf"
    write_pdf(source, [["Page one sentence."], ["Page two sentence."]])
    record = only(normalize_sources(ctx, [source]))
    text = normalized_text(ctx, record)

    locators = build_locator_map(
        record["source_id"], record["normalized_path"], text, {}
    )
    for entry in locators:
        start, end = entry["normalized_char_start"], entry["normalized_char_end"]
        assert text[start:end].strip() == text.splitlines()[entry["normalized_line_start"] - 1]

    from kip.artifacts import read_jsonl

    stored = read_jsonl(ctx.normalized_dir / record["source_id"] / "locator_map.jsonl")
    pages = {entry["original_locator_start"].get("page") for entry in stored}
    assert pages == {1, 2}


def test_docx_keeps_paragraphs_and_tables(ctx: RunContext, tmp_path: Path):
    """Spec §8.5: tables are preserved rather than dropped."""
    document = docx.Document()
    document.add_paragraph("The pilot cut median latency.")
    document.add_paragraph("Follow-up ran for four weeks.")
    table = document.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "metric"
    table.cell(0, 1).text = "value"
    table.cell(1, 0).text = "latency"
    table.cell(1, 1).text = "12 ms"
    source = tmp_path / "memo.docx"
    document.save(str(source))

    record = only(normalize_sources(ctx, [source]))
    assert record["normalization_status"] == "success", record["warnings"]
    text = normalized_text(ctx, record)
    assert "The pilot cut median latency." in text
    assert "Follow-up ran for four weeks." in text
    assert "metric | value" in text
    assert "latency | 12 ms" in text


def test_pptx_keeps_slide_order_and_speaker_notes(ctx: RunContext, tmp_path: Path):
    presentation = pptx.Presentation()
    blank = presentation.slide_layouts[6]
    for index, body in enumerate(["Adoption reached 40%.", "Churn fell to 3%."], start=1):
        slide = presentation.slides.add_slide(blank)
        box = slide.shapes.add_textbox(
            pptx.util.Inches(1), pptx.util.Inches(1),
            pptx.util.Inches(6), pptx.util.Inches(2),
        )
        box.text_frame.text = body
        slide.notes_slide.notes_text_frame.text = f"Speaker note {index}."
    source = tmp_path / "deck.pptx"
    presentation.save(str(source))

    record = only(normalize_sources(ctx, [source]))
    assert record["normalization_status"] == "success", record["warnings"]
    text = normalized_text(ctx, record)
    assert text.index("[[SLIDE 1]]") < text.index("[[SLIDE 2]]")
    assert "Adoption reached 40%." in text
    assert "[[NOTES]] Speaker note 2." in text


def test_xlsx_keeps_every_sheet_with_its_name(ctx: RunContext, tmp_path: Path):
    workbook = openpyxl.Workbook()
    first = workbook.active
    first.title = "Q1"
    first.append(["metric", "value"])
    first.append(["revenue", 5000])
    second = workbook.create_sheet("Q2")
    second.append(["metric", "value"])
    second.append(["revenue", 7200])
    source = tmp_path / "book.xlsx"
    workbook.save(str(source))

    record = only(normalize_sources(ctx, [source]))
    assert record["normalization_status"] == "success", record["warnings"]
    text = normalized_text(ctx, record)
    assert "[[SHEET Q1]]" in text and "[[SHEET Q2]]" in text
    assert "revenue | 5000" in text
    assert "revenue | 7200" in text


def test_a_rich_format_with_no_parser_is_quarantined_not_dropped(
    ctx: RunContext, tmp_path: Path, monkeypatch
):
    """The dangerous path: a parser failure must show up in the registry.

    `normalize_sources` catches PipelineError and quarantines, so nothing
    crashes -- which is exactly why a silent drop here would never be noticed.
    """
    from kip import normalize as normalize_module

    def no_parser(path: Path):
        raise PipelineError(f"{path.name}: Docling not installed")

    monkeypatch.setattr(normalize_module, "_docling", no_parser)
    monkeypatch.setattr(normalize_module, "_pdf_lite", no_parser)

    source = tmp_path / "report.pdf"
    write_pdf(source, [["Anything at all."]])
    record = only(normalize_sources(ctx, [source]))

    assert record["normalization_status"] == "quarantined"
    assert record["warnings"]
    assert not (ctx.normalized_dir / record["source_id"] / "normalized.txt").exists()


def test_a_multipart_email_keeps_its_attachment_inventory(ctx: RunContext, tmp_path: Path):
    """Spec §8.5: attachments are inventoried even though they are not parsed."""
    source = tmp_path / "thread.eml"
    source.write_text(
        "From: analyst@example.com\n"
        "To: team@example.com\n"
        "Subject: Q1 numbers\n"
        'Content-Type: multipart/mixed; boundary="B"\n'
        "\n"
        "--B\n"
        "Content-Type: text/plain\n"
        "\n"
        "Revenue rose 12% quarter over quarter.\n"
        "--B\n"
        "Content-Type: text/csv\n"
        'Content-Disposition: attachment; filename="q1.csv"\n'
        "\n"
        "metric,value\n"
        "--B--\n",
        encoding="utf-8",
    )

    record = only(normalize_sources(ctx, [source]))
    assert record["normalization_status"] == "success", record["warnings"]
    text = normalized_text(ctx, record)
    assert "Subject: Q1 numbers" in text
    assert "Revenue rose 12% quarter over quarter." in text
    assert "[[ATTACHMENTS q1.csv]]" in text


def test_a_binary_file_with_a_text_extension_is_quarantined(ctx: RunContext, tmp_path: Path):
    """Decoding with errors="replace" turned any binary into plausible prose.

    It was registered `success` with no warning and sent straight to the
    expensive extractor. Spec §8.7 says unsupported sources are quarantined and
    never treated as valid, and garbage that merely survived decoding is that.
    """
    source = tmp_path / "blob.md"
    source.write_bytes(bytes(range(256)))

    record = only(normalize_sources(ctx, [source]))
    assert record["normalization_status"] == "quarantined"
    assert record["warnings"]


# --- Source identity ----------------------------------------------------------


def test_two_files_with_the_same_stem_get_different_source_ids(
    ctx: RunContext, tmp_path: Path
):
    """The collision that silently deleted a document.

    `notes.md` and `notes.txt` both slugified to `src-notes`, so they shared one
    normalized.txt and one unit_id namespace: the second overwrote the first
    before Pass 1 ever read it, and `kip validate` reported a clean run.
    """
    (tmp_path / "pilot.md").write_text("The Apollo pilot cut latency to 12 ms.\n", encoding="utf-8")
    (tmp_path / "pilot.txt").write_text(
        "The Borealis pilot raised error rate to 4%.\n", encoding="utf-8"
    )
    sources = sorted(tmp_path.glob("pilot.*"))

    registry = normalize_sources(ctx, sources)
    ids = [r["source_id"] for r in registry]
    assert len(set(ids)) == 2, ids

    texts = {normalized_text(ctx, record) for record in registry}
    assert texts == {
        "The Apollo pilot cut latency to 12 ms.\n",
        "The Borealis pilot raised error rate to 4%.\n",
    }


def test_the_same_file_keeps_the_same_source_id(tmp_path: Path):
    """Content-derived, not positional: adding a source must not renumber the rest."""
    path = tmp_path / "doc.md"
    path.write_text("Stable content.\n", encoding="utf-8")
    first = source_id_for(path)
    (tmp_path / "another.md").write_text("Unrelated.\n", encoding="utf-8")
    assert source_id_for(path) == first


def test_same_name_different_content_in_two_directories_both_survive(
    ctx: RunContext, tmp_path: Path
):
    """Discovery is recursive, so q1/report.md and q2/report.md are two documents."""
    for quarter, body in (("q1", "Q1 revenue was 5,000 USD.\n"), ("q2", "Q2 revenue was 7,200 USD.\n")):
        directory = tmp_path / quarter
        directory.mkdir()
        (directory / "report.md").write_text(body, encoding="utf-8")

    registry = normalize_sources(ctx, sorted(tmp_path.rglob("report.md")))
    assert len({r["source_id"] for r in registry}) == 2
    assert {normalized_text(ctx, r) for r in registry} == {
        "Q1 revenue was 5,000 USD.\n",
        "Q2 revenue was 7,200 USD.\n",
    }


def test_the_same_document_ingested_twice_is_refused(ctx: RunContext, tmp_path: Path):
    """Same name AND same bytes is one document counted twice.

    That inflates every coverage and independence count downstream, and it is
    the only way two sources can still land on one source_id.
    """
    for quarter in ("q1", "q2"):
        directory = tmp_path / quarter
        directory.mkdir()
        (directory / "report.md").write_text("Identical content.\n", encoding="utf-8")

    with pytest.raises(PipelineError, match="duplicate source"):
        normalize_sources(ctx, sorted(tmp_path.rglob("report.md")))
