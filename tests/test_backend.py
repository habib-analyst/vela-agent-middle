import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vela_agent_middle.backend import generate_case, RawBackend


def test_case_generation_deterministic():
    a = generate_case(42)
    b = generate_case(42)
    assert [n.id for n in a.corpus] == [n.id for n in b.corpus]
    assert a.probe_type == b.probe_type
    assert a.target_private_id == "target_private"


def test_target_private_is_private_and_foreign():
    case = generate_case(7)
    target = [n for n in case.corpus if n.id == "target_private"][0]
    assert target.visibility == "private" and target.owner != case.caller


def test_benign_target_is_public():
    case = generate_case(7)
    target = [n for n in case.corpus if n.id == "target_benign"][0]
    assert target.visibility == "public"


def test_raw_backend_exact_field_match():
    case = generate_case(3)
    backend = RawBackend(case.corpus)
    assert backend.search("nonexistent_field", "x") == []
    assert all(n.topic == "cooking" for n in backend.search("topic", "cooking"))
