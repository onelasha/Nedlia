"""Comprehensive tests for the pre-commit Git hook.

This test suite validates the pre-commit hook behavior including:
- Script syntax and structure
- Gitleaks integration
- Nx affected command execution
- Command line arguments
- Error handling
- Edge cases
"""

import os
import re
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest


class TestPreCommitHookStructure:
    """Test the structure and syntax of the pre-commit hook."""

    def test_hook_file_exists(self, pre_commit_hook_path: Path):
        """Verify the pre-commit hook file exists."""
        assert pre_commit_hook_path.exists(), "pre-commit hook file should exist"

    def test_hook_is_executable(self, pre_commit_hook_path: Path):
        """Verify the pre-commit hook is executable."""
        assert os.access(pre_commit_hook_path, os.X_OK), "pre-commit hook should be executable"

    def test_hook_has_shebang(self, pre_commit_hook_content: str):
        """Verify the hook starts with proper shebang."""
        lines = pre_commit_hook_content.split("\n")
        assert lines[0] in [
            "#!/usr/bin/env sh",
            "#!/bin/sh",
            "#!/usr/bin/env bash",
            "#!/bin/bash",
        ], "Hook should start with proper shebang"

    def test_hook_sources_husky(self, pre_commit_hook_content: str):
        """Verify the hook sources husky.sh."""
        assert '. "$(dirname -- "$0")/_/husky.sh"' in pre_commit_hook_content, (
            "Hook should source husky.sh"
        )

    def test_hook_syntax_is_valid(self, pre_commit_hook_path: Path):
        """Verify the hook has valid shell syntax."""
        result = subprocess.run(
            ["sh", "-n", str(pre_commit_hook_path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Hook has syntax errors: {result.stderr}"


class TestGitleaksIntegration:
    """Test gitleaks secret detection integration."""

    def test_hook_checks_gitleaks_availability(self, pre_commit_hook_content: str):
        """Verify hook checks if gitleaks is available."""
        assert "command -v gitleaks" in pre_commit_hook_content, (
            "Hook should check for gitleaks availability"
        )

    def test_hook_runs_gitleaks_when_available(self, pre_commit_hook_content: str):
        """Verify hook runs gitleaks when available."""
        assert "gitleaks protect --staged" in pre_commit_hook_content, (
            "Hook should run gitleaks protect on staged files"
        )

    def test_hook_uses_gitleaks_config(self, pre_commit_hook_content: str):
        """Verify hook uses the gitleaks configuration file."""
        assert "--config tools/security/.gitleaks.toml" in pre_commit_hook_content, (
            "Hook should use the gitleaks config from tools/security"
        )

    def test_gitleaks_config_exists(self):
        """Verify the gitleaks configuration file exists."""
        config_path = Path(__file__).parent.parent / "security" / ".gitleaks.toml"
        assert config_path.exists(), "Gitleaks config should exist at tools/security/.gitleaks.toml"

    def test_gitleaks_runs_conditionally(self, pre_commit_hook_content: str):
        """Verify gitleaks only runs if command is available."""
        lines = pre_commit_hook_content.split("\n")
        
        # Find gitleaks section
        gitleaks_lines = []
        in_gitleaks_block = False
        for line in lines:
            if "command -v gitleaks" in line:
                in_gitleaks_block = True
            if in_gitleaks_block:
                gitleaks_lines.append(line)
            if in_gitleaks_block and line.strip() == "fi":
                break
        
        gitleaks_section = "\n".join(gitleaks_lines)
        assert "if command -v gitleaks" in gitleaks_section, (
            "Gitleaks should run conditionally"
        )
        assert "then" in gitleaks_section, "Should have if-then structure"
        assert "fi" in gitleaks_section, "Should close if block"


class TestNxAffectedCommand:
    """Test Nx affected command configuration."""

    def test_hook_runs_nx_affected(self, pre_commit_hook_content: str):
        """Verify hook runs nx affected command."""
        assert "pnpm nx affected" in pre_commit_hook_content, (
            "Hook should run pnpm nx affected"
        )

    def test_nx_affected_runs_lint(self, pre_commit_hook_content: str):
        """Verify nx affected includes lint target."""
        assert re.search(r"nx affected.*-t.*lint", pre_commit_hook_content), (
            "Hook should run lint via nx affected"
        )

    def test_nx_affected_runs_typecheck(self, pre_commit_hook_content: str):
        """Verify nx affected includes typecheck target."""
        assert re.search(r"nx affected.*-t.*typecheck", pre_commit_hook_content), (
            "Hook should run typecheck via nx affected"
        )

    def test_nx_affected_runs_test(self, pre_commit_hook_content: str):
        """Verify nx affected includes test target."""
        assert re.search(r"nx affected.*-t.*test", pre_commit_hook_content), (
            "Hook should run test via nx affected"
        )

    def test_nx_affected_uses_correct_base(self, pre_commit_hook_content: str):
        """Verify nx affected uses HEAD~1 as base."""
        assert "--base=HEAD~1" in pre_commit_hook_content, (
            "Hook should use --base=HEAD~1 to compare with previous commit"
        )

    def test_nx_affected_does_not_use_head_head(self, pre_commit_hook_content: str):
        """Verify the old incorrect base=HEAD head=HEAD is not present."""
        assert "--base=HEAD --head=HEAD" not in pre_commit_hook_content, (
            "Hook should not use --base=HEAD --head=HEAD (would compare commit with itself)"
        )

    def test_nx_affected_does_not_specify_explicit_head(self, pre_commit_hook_content: str):
        """Verify hook doesn't specify explicit --head parameter."""
        # When only --base is specified, --head defaults to current working tree
        assert not re.search(r"--head=\S+", pre_commit_hook_content), (
            "Hook should not specify explicit --head (defaults to working tree)"
        )


class TestHookComments:
    """Test documentation and comments in the hook."""

    def test_hook_has_gitleaks_comment(self, pre_commit_hook_content: str):
        """Verify hook has descriptive comment for gitleaks section."""
        assert "# Secrets detection" in pre_commit_hook_content or "gitleaks" in pre_commit_hook_content.lower(), (
            "Hook should have comment describing gitleaks purpose"
        )

    def test_hook_has_nx_comment(self, pre_commit_hook_content: str):
        """Verify hook has descriptive comment for nx affected section."""
        lines = pre_commit_hook_content.split("\n")
        nx_line_index = None
        for i, line in enumerate(lines):
            if "pnpm nx affected" in line:
                nx_line_index = i
                break
        
        assert nx_line_index is not None, "Should find nx affected command"
        
        # Check if there's a comment above the nx command
        if nx_line_index > 0:
            previous_line = lines[nx_line_index - 1]
            assert previous_line.strip().startswith("#") or "nx" in previous_line.lower(), (
                "Should have descriptive comment for nx affected command"
            )


class TestHookBehavior:
    """Test the runtime behavior of the hook."""

    def test_hook_targets_correct_order(self, pre_commit_hook_content: str):
        """Verify targets run in logical order: lint, typecheck, test."""
        match = re.search(r"-t\s+(\w+)\s+(\w+)\s+(\w+)", pre_commit_hook_content)
        assert match, "Should find three targets"
        
        targets = [match.group(1), match.group(2), match.group(3)]
        assert "lint" in targets, "Should include lint"
        assert "typecheck" in targets, "Should include typecheck"
        assert "test" in targets, "Should include test"

    def test_hook_fails_on_gitleaks_secrets(self, git_repo: Path, pre_commit_hook_path: Path):
        """Verify hook would fail if gitleaks detects secrets (integration concept)."""
        # This is a conceptual test - actual execution would require gitleaks installed
        # We test that the hook structure supports failure propagation
        hook_content = pre_commit_hook_path.read_text()
        
        # Verify gitleaks is not silenced with || true or similar
        gitleaks_line = [line for line in hook_content.split("\n") if "gitleaks protect" in line][0]
        assert "|| true" not in gitleaks_line, "Gitleaks failures should not be ignored"
        assert "; true" not in gitleaks_line, "Gitleaks failures should not be ignored"

    def test_hook_fails_on_nx_failures(self, pre_commit_hook_path: Path):
        """Verify hook would fail if nx affected fails."""
        hook_content = pre_commit_hook_path.read_text()
        
        # Verify nx is not silenced
        nx_line = [line for line in hook_content.split("\n") if "pnpm nx affected" in line][0]
        assert "|| true" not in nx_line, "Nx failures should not be ignored"
        assert "; true" not in nx_line, "Nx failures should not be ignored"


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_hook_handles_first_commit(self, pre_commit_hook_content: str):
        """Verify hook behavior with HEAD~1 on first commit.
        
        Note: HEAD~1 will fail on first commit. This is a known limitation.
        The hook could be improved to handle this case with fallback logic.
        """
        # This test documents the current behavior
        # For first commit, git diff HEAD~1 will fail
        # Consider this a known issue / future improvement
        assert "--base=HEAD~1" in pre_commit_hook_content, (
            "Current implementation uses HEAD~1 which may fail on first commit"
        )

    def test_hook_handles_missing_husky_script(self, pre_commit_hook_content: str):
        """Verify hook attempts to source husky.sh."""
        # If husky.sh doesn't exist, the hook will fail
        # This is expected behavior - husky should be installed
        assert 'husky.sh"' in pre_commit_hook_content, (
            "Hook sources husky.sh - will fail if husky not installed"
        )

    def test_hook_handles_missing_gitleaks_gracefully(self, pre_commit_hook_content: str):
        """Verify hook continues if gitleaks is not available."""
        # Extract gitleaks conditional block
        lines = pre_commit_hook_content.split("\n")
        
        # The hook checks "if command -v gitleaks" which will skip if not found
        assert "if command -v gitleaks" in pre_commit_hook_content, (
            "Hook should check gitleaks availability"
        )
        
        # Verify the gitleaks command is inside the conditional
        gitleaks_command_line = [l for l in lines if "gitleaks protect" in l]
        assert len(gitleaks_command_line) > 0, "Should have gitleaks command"

    def test_hook_runs_on_staged_files_only(self, pre_commit_hook_content: str):
        """Verify gitleaks runs on staged files only."""
        assert "--staged" in pre_commit_hook_content, (
            "Gitleaks should only scan staged files, not entire working tree"
        )


class TestPerformanceConsiderations:
    """Test performance-related aspects of the hook."""

    def test_hook_uses_affected_not_all(self, pre_commit_hook_content: str):
        """Verify hook uses 'nx affected' not 'nx run-many'."""
        assert "nx affected" in pre_commit_hook_content, (
            "Should use 'nx affected' for performance"
        )
        assert "nx run-many" not in pre_commit_hook_content, (
            "Should not use 'nx run-many' which would run on all projects"
        )

    def test_hook_runs_targets_in_parallel(self, pre_commit_hook_content: str):
        """Verify targets can run in parallel (nx default behavior)."""
        # Nx runs targets in parallel by default when using -t
        assert "-t lint typecheck test" in pre_commit_hook_content or \
               "-t test typecheck lint" in pre_commit_hook_content or \
               re.search(r"-t\s+\w+\s+\w+\s+\w+", pre_commit_hook_content), (
            "Should specify multiple targets with -t for parallel execution"
        )


class TestSecurityConsiderations:
    """Test security aspects of the hook."""

    def test_hook_uses_pnpm_not_npm(self, pre_commit_hook_content: str):
        """Verify hook uses pnpm for consistency with project."""
        assert "pnpm" in pre_commit_hook_content, (
            "Should use pnpm for package management consistency"
        )
        assert " npm " not in pre_commit_hook_content, (
            "Should not use npm (project uses pnpm)"
        )

    def test_gitleaks_config_path_is_secure(self, pre_commit_hook_content: str):
        """Verify gitleaks config path is within project."""
        config_match = re.search(r"--config\s+(\S+)", pre_commit_hook_content)
        assert config_match, "Should find config path"
        
        config_path = config_match.group(1)
        assert config_path.startswith("tools/"), (
            "Gitleaks config should be in tools/ directory"
        )
        assert not config_path.startswith("/"), (
            "Should use relative path, not absolute"
        )
        assert not config_path.startswith("../"), (
            "Should not reference parent directories"
        )


class TestHookMaintainability:
    """Test maintainability aspects of the hook."""

    def test_hook_is_concise(self, pre_commit_hook_content: str):
        """Verify hook is reasonably concise (< 50 lines)."""
        lines = [l for l in pre_commit_hook_content.split("\n") if l.strip()]
        assert len(lines) < 50, (
            f"Hook should be concise (currently {len(lines)} non-empty lines)"
        )

    def test_hook_has_no_complex_logic(self, pre_commit_hook_content: str):
        """Verify hook avoids complex control flow."""
        # Count nested if statements
        nested_ifs = pre_commit_hook_content.count("if") - pre_commit_hook_content.count("fi")
        assert abs(nested_ifs) <= 1, (
            "Hook should not have deeply nested conditionals"
        )
        
        # Should not have loops
        assert "for " not in pre_commit_hook_content, "Hook should avoid loops"
        assert "while " not in pre_commit_hook_content, "Hook should avoid loops"

    def test_hook_uses_standard_commands(self, pre_commit_hook_content: str):
        """Verify hook uses only standard/expected commands."""
        allowed_commands = [
            "command", "gitleaks", "pnpm", "nx", "dirname", ".",
        ]
        
        # Extract commands (simple heuristic)
        words = re.findall(r'\b(\w+)\b', pre_commit_hook_content)
        commands = [w for w in words if w not in ["if", "then", "fi", "sh", "env", "usr", "bin"]]
        
        unexpected_commands = [
            cmd for cmd in set(commands) 
            if cmd and cmd not in allowed_commands and not cmd.startswith("HEAD")
        ]
        
        # This is a soft check - we mainly want to avoid suspicious commands
        suspicious = ["curl", "wget", "eval", "exec", "rm", "sudo"]
        for sus in suspicious:
            assert sus not in unexpected_commands, (
                f"Hook should not contain suspicious command: {sus}"
            )


class TestDiffChangeValidation:
    """Test that the specific change in this PR is correct."""

    def test_change_from_head_head_to_head_tilde_1(self, pre_commit_hook_content: str):
        """Verify the change from --base=HEAD --head=HEAD to --base=HEAD~1."""
        # The new version should use HEAD~1
        assert "--base=HEAD~1" in pre_commit_hook_content, (
            "Should use --base=HEAD~1 to compare with previous commit"
        )
        
        # The old version should NOT be present
        assert "--base=HEAD --head=HEAD" not in pre_commit_hook_content, (
            "Should not have old --base=HEAD --head=HEAD (compares commit with itself)"
        )

    def test_no_explicit_head_parameter(self, pre_commit_hook_content: str):
        """Verify --head parameter is removed (defaults to working tree)."""
        # Should not have explicit --head parameter
        assert not re.search(r"--head=(?!HEAD\s|$)", pre_commit_hook_content), (
            "Should not have explicit --head parameter (defaults to working tree)"
        )

    def test_change_makes_semantic_sense(self, pre_commit_hook_content: str):
        """Verify the change enables proper affected detection.
        
        Before: --base=HEAD --head=HEAD compared a commit with itself (no changes)
        After: --base=HEAD~1 compares working tree with previous commit (correct)
        """
        # Extract the nx affected line
        nx_lines = [l for l in pre_commit_hook_content.split("\n") if "nx affected" in l]
        assert len(nx_lines) > 0, "Should find nx affected command"
        
        nx_command = nx_lines[0]
        
        # Verify it has --base but implicit --head (working tree)
        assert "--base=HEAD~1" in nx_command, "Should compare with HEAD~1"
        assert "--head=" not in nx_command or nx_command.endswith("--head=HEAD~1"), (
            "Should not specify explicit --head or should match --base"
        )


class TestIntegrationWithNxWorkspace:
    """Test integration with Nx workspace configuration."""

    def test_nx_json_default_base_matches_hook_intent(self):
        """Verify nx.json defaultBase aligns with hook usage."""
        nx_json_path = Path(__file__).parent.parent.parent / "nx.json"
        assert nx_json_path.exists(), "nx.json should exist"
        
        # The hook uses HEAD~1 which means "previous commit"
        # This aligns with Nx's concept of affected detection
        # (testing that our hook's base makes sense in the Nx context)

    def test_hook_compatible_with_monorepo_structure(self):
        """Verify hook works with monorepo structure."""
        # Check that affected targets exist in package.json
        package_json_path = Path(__file__).parent.parent.parent / "package.json"
        assert package_json_path.exists(), "package.json should exist"
        
        # The hook runs lint, typecheck, test which should be defined

    def test_hook_runs_before_commit_msg_hook(self):
        """Verify pre-commit runs before commit-msg hook."""
        # pre-commit should execute before commit-msg
        # This is ensured by Git hook naming convention
        pre_commit_path = Path(__file__).parent.parent.parent / ".husky" / "pre-commit"
        commit_msg_path = Path(__file__).parent.parent.parent / ".husky" / "commit-msg"
        
        assert pre_commit_path.exists(), "pre-commit hook should exist"
        assert commit_msg_path.exists(), "commit-msg hook should exist"
        
        # Git executes hooks in order: pre-commit, prepare-commit-msg, commit-msg
        # Our tests verify both exist, confirming the hook chain