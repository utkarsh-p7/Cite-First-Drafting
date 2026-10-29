"""Wraps the dissertation's 71-assertion scoring-harness self-test as a pytest test."""

from cite_first_drafting.evaluation import harness

from .conftest import FIXTURES


def test_harness_selftest_passes(capsys):
    rc = harness.selftest(FIXTURES)
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "SELFTEST PASS" in out and "71 assertions" in out, out


def test_harness_version_is_frozen():
    assert harness.HARNESS_VERSION.startswith("eval-harness v1.2.1")
