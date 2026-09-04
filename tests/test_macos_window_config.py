from config import config
from ok.device.window_target import (
    WindowCandidate,
    WindowGeometry,
    WindowMatchHints,
    WindowSelectionStatus,
    select_window_candidate,
)


def test_macos_window_config_is_independent_and_does_not_guess_app_identity():
    assert config['macos'] is not config['windows']
    assert config['macos']['bundle_identifiers'] == []
    assert config['macos']['application_names'] == []
    assert config['windows']['exe'] == 'Client-Win64-Shipping.exe'
    assert WindowMatchHints.from_mapping(config['macos']).allowed_layers == (0,)


def test_title_hint_only_requires_explicit_manual_selection():
    hints = WindowMatchHints.from_mapping(config['macos'])
    candidate = WindowCandidate(
        process_id=42,
        window_id=7,
        bundle_identifier='com.example.not-observed',
        application_name='Unverified Application',
        title='Wuthering Waves',
        layer=0,
        outer_geometry=WindowGeometry(0, 0, 1280, 720),
    )

    result = select_window_candidate([candidate], hints)

    assert result.status is WindowSelectionStatus.MANUAL_SELECTION_REQUIRED
    assert result.selected is None


def test_manual_window_choice_produces_only_stable_persistable_fields():
    hints = WindowMatchHints.from_mapping(config['macos'])
    candidate = WindowCandidate(
        process_id=42,
        window_id=7,
        bundle_identifier='com.example.observed',
        application_name='Observed Application',
        title='Wuthering Waves',
        layer=0,
        outer_geometry=WindowGeometry(0, 0, 1280, 720),
    )

    result = select_window_candidate([candidate], hints, manual_window_id=7)

    assert result.status is WindowSelectionStatus.SELECTED
    assert result.stable_hint.to_mapping() == {
        'bundle_identifier': 'com.example.observed',
        'application_name': 'Observed Application',
        'title': 'Wuthering Waves',
    }
    assert 'process_id' not in result.stable_hint.to_mapping()
    assert 'window_id' not in result.stable_hint.to_mapping()
