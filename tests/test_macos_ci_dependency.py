"""The two integration gates must validate the same immutable framework."""
from pathlib import Path
import re


def test_both_ci_gates_pin_the_same_complete_framework_sha():
    workflows = Path(__file__).resolve().parents[1] / '.github' / 'workflows'
    refs = []
    for name in ('test.yml', 'macos-foreground-guardrails.yml'):
        text = (workflows / name).read_text(encoding='utf-8')
        match = re.search(r'repository: Silhouette-my/ok-script\s+ref: ([0-9a-f]{40})\s', text)
        assert match, f'{name} must pin a complete ok-script commit'
        refs.append(match.group(1))
        assert 'OK_SCRIPT_BUILD_VERSION="2.0.7b1+macos.${framework_sha}"' in text
    assert refs[0] == refs[1]
