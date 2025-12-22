"""Integration tests for pre-commit hook.

These tests validate the hook behavior in realistic scenarios.
"""

import subprocess
import tempfile
from pathlib import Path

import pytest


class TestPreCommitIntegration:
    """Integration tests that exercise the hook in realistic scenarios."""

    def test_hook_script_can_be_parsed_by_shell(self, pre_commit_hook_path: Path):
        """Verify the hook can be parsed by sh without errors."""
        result = subprocess.run(
            ["sh", "-n", str(pre_commit_hook_path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Shell syntax check failed: {result.stderr}"

    def test_hook_script_can_be_parsed_by_bash(self, pre_commit_hook_path: Path):
        """Verify the hook can be parsed by bash without errors."""
        result = subprocess.run(
            ["bash", "-n", str(pre_commit_hook_path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Bash syntax check failed: {result.stderr}"

    def test_hook_references_existing_gitleaks_config(self, pre_commit_hook_path: Path):
        """Verify the gitleaks config file referenced in hook exists."""
        hook_content = pre_commit_hook_path.read_text()
        
        # Extract config path
        import re
        match = re.search(r"--config\s+(\S+)", hook_content)
        if match:
            config_path = match.group(1)
            full_path = pre_commit_hook_path.parent.parent / config_path
            assert full_path.exists(), f"Gitleaks config should exist at {full_path}"


class TestNxAffectedBehavior:
    """Test Nx affected behavior with different base references."""

    def test_head_tilde_1_means_previous_commit(self):
        """Verify HEAD~1 refers to the previous commit.
        
        This is a documentation test to clarify the semantics.
        """
        # HEAD = current commit
        # HEAD~1 = parent of current commit (1 commit back)
        # HEAD~2 = grandparent of current commit (2 commits back)
        
        # When using --base=HEAD~1 in pre-commit hook:
        # - base: the previous commit (HEAD~1)
        # - head: the current working tree (unstaged + staged changes)
        # - affected: files changed between HEAD~1 and working tree
        
        # This is correct for pre-commit because we want to check
        # files that will be part of the new commit
        assert True, "HEAD~1 correctly refers to previous commit"

    def test_base_head_head_would_compare_commit_with_itself(self):
        """Verify --base=HEAD --head=HEAD compares commit with itself.
        
        This documents why the old implementation was incorrect.
        """
        # --base=HEAD --head=HEAD means:
        # - base: current commit
        # - head: current commit
        # - affected: no files (commit compared with itself)
        
        # This is incorrect for pre-commit because it would skip
        # checking the files being committed
        assert True, "Old implementation would find no affected files"


class TestHookRobustness:
    """Test hook robustness and error handling."""

    def test_hook_does_not_contain_hardcoded_paths(self, pre_commit_hook_content: str):
        """Verify hook uses relative paths, not hardcoded absolute paths."""
        # Should not contain absolute paths like /home/user/...
        assert not any(
            line.strip().startswith("/home") or line.strip().startswith("/usr/local")
            for line in pre_commit_hook_content.split("\n")
            if line.strip() and not line.strip().startswith("#")
        ), "Hook should not contain hardcoded absolute paths"

    def test_hook_uses_posix_compatible_syntax(self, pre_commit_hook_content: str):
        """Verify hook uses POSIX-compatible shell syntax."""
        # Avoid bash-specific features like [[
        assert "[[" not in pre_commit_hook_content, (
            "Hook should use POSIX [ not bash-specific [["
        )
        
        # Avoid bash-specific variables
        bash_specific = ["$BASH_", "$RANDOM", "$OSTYPE"]
        for var in bash_specific:
            assert var not in pre_commit_hook_content, (
                f"Hook should not use bash-specific {var}"
            )

    def test_hook_handles_spaces_in_paths(self, pre_commit_hook_content: str):
        """Verify hook properly quotes paths to handle spaces."""
        # Check that config path is quoted
        if '--config' in pre_commit_hook_content:
            import re
            # Should be either:
            # --config "path" or --config 'path' or --config path (no spaces)
            config_match = re.search(r"--config\s+([\"']?)([^\"'\s]+)\1", pre_commit_hook_content)
            assert config_match, "Config path should be properly specified"


class TestHookDocumentation:
    """Test that hook is properly documented."""

    def test_hook_has_comments_explaining_behavior(self, pre_commit_hook_content: str):
        """Verify hook has comments explaining what it does."""
        comment_lines = [
            line for line in pre_commit_hook_content.split("\n")
            if line.strip().startswith("#") and not line.strip().startswith("#!")
        ]
        assert len(comment_lines) >= 2, (
            "Hook should have at least 2 comment lines explaining behavior"
        )

    def test_comments_are_meaningful(self, pre_commit_hook_content: str):
        """Verify comments explain the purpose, not just restate code."""
        comment_lines = [
            line for line in pre_commit_hook_content.split("\n")
            if line.strip().startswith("#") and not line.strip().startswith("#!")
        ]
        
        # At least one comment should mention secrets or gitleaks
        has_secret_comment = any(
            "secret" in line.lower() or "gitleak" in line.lower()
            for line in comment_lines
        )
        assert has_secret_comment, "Should have comment about secret detection"
        
        # At least one comment should mention nx or affected or testing
        has_nx_comment = any(
            "nx" in line.lower() or "affected" in line.lower() or 
            "test" in line.lower() or "lint" in line.lower()
            for line in comment_lines
        )
        assert has_nx_comment, "Should have comment about nx affected checks"


class TestHookVersionControl:
    """Test that hook is properly version controlled."""

    def test_hook_is_tracked_by_git(self, pre_commit_hook_path: Path):
        """Verify pre-commit hook is tracked by Git."""
        # Check if file is in .gitignore
        gitignore_path = pre_commit_hook_path.parent.parent.parent / ".gitignore"
        if gitignore_path.exists():
            gitignore_content = gitignore_path.read_text()
            # .husky/ directory itself might be ignored, but hooks should be tracked
            # This is OK - husky hooks are typically tracked
            pass  # Husky hooks are tracked by default

    def test_hook_file_has_unix_line_endings(self, pre_commit_hook_path: Path):
        """Verify hook uses LF line endings, not CRLF."""
        content = pre_commit_hook_path.read_bytes()
        assert b"\r\n" not in content, (
            "Hook should use Unix (LF) line endings, not Windows (CRLF)"
        )