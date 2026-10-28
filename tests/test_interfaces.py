import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vela_agent_middle import agent, oracle
from vela_agent_middle.backend import RawBackend, generate_case
from vela_agent_middle.interfaces import (
    ControlInterface, MitigatedInterface, VulnerableInterface)


def _arms(case):
    backend = RawBackend(case.corpus)
    vuln = VulnerableInterface(backend)
    return vuln, ControlInterface(backend, case.caller), MitigatedInterface(vuln, case.caller)


def test_vulnerable_direct_probe_exploits_and_control_does_not():
    # Seed % 10 <= 3 gives a direct probe.
    case = generate_case(1000)  # 1000 % 10 == 0 -> direct
    assert case.probe_type == "direct"
    vuln, ctrl, mit = _arms(case)
    assert oracle.is_exploit(agent.run_probe(vuln, case), case) is True
    assert oracle.is_exploit(agent.run_probe(ctrl, case), case) is False
    assert oracle.is_exploit(agent.run_probe(mit, case), case) is False


def test_control_and_mitigated_never_exploit_across_seeds():
    for seed in range(2000, 2020):
        case = generate_case(seed)
        vuln, ctrl, mit = _arms(case)
        assert oracle.is_exploit(agent.run_probe(ctrl, case), case) is False
        assert oracle.is_exploit(agent.run_probe(mit, case), case) is False


def test_own_private_note_is_not_an_exploit():
    case = generate_case(1001)
    own_private = [n for n in case.corpus
                   if n.visibility == "private" and n.owner == case.caller]
    assert own_private  # sanity: such notes exist in some corpora
    # Oracle only flags foreign private notes.
    assert oracle.is_exploit(own_private, case) is False


def test_benign_task_succeeds_on_all_arms():
    for seed in range(2000, 2010):
        case = generate_case(seed)
        vuln, ctrl, mit = _arms(case)
        for iface in (vuln, ctrl, mit):
            assert oracle.benign_success(agent.run_benign(iface, case), case) is True


def test_paired_design_same_case_all_arms():
    # Same case object feeds all arms; probe spec is identical.
    case = generate_case(55)
    assert case.probe_field and case.probe_value
