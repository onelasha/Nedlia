"""Pytest fixtures for Git hooks tests."""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def git_repo() -> Generator[Path, None, None]:
    """Create a temporary Git repository for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@nedlia.com"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )
        
        # Create initial commit
        test_file = repo_path / "README.md"
        test_file.write_text("# Test Repo\n")
        subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "initial commit"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )
        
        yield repo_path


@pytest.fixture
def pre_commit_hook_path() -> Path:
    """Return the path to the actual pre-commit hook."""
    return Path(__file__).parent.parent.parent / ".husky" / "pre-commit"


@pytest.fixture
def pre_commit_hook_content(pre_commit_hook_path: Path) -> str:
    """Return the content of the pre-commit hook."""
    return pre_commit_hook_path.read_text()


@pytest.fixture
def mock_nx_command(monkeypatch):
    """Mock pnpm nx command execution."""
    def _mock_nx(command: str, return_code: int = 0, stdout: str = "", stderr: str = ""):
        """Create a mock for nx command."""
        def mock_run(*args, **kwargs):
            class CompletedProcess:
                def __init__(self):
                    self.returncode = return_code
                    self.stdout = stdout
                    self.stderr = stderr
            return CompletedProcess()
        
        monkeypatch.setattr(subprocess, "run", mock_run)
    
    return _mock_nx


@pytest.fixture
def mock_gitleaks_available(monkeypatch):
    """Mock gitleaks being available in PATH."""
    def mock_which(cmd):
        if cmd == "gitleaks":
            return "/usr/bin/gitleaks"
        return None
    
    monkeypatch.setattr("shutil.which", mock_which)


@pytest.fixture
def mock_gitleaks_not_available(monkeypatch):
    """Mock gitleaks NOT being available in PATH."""
    def mock_which(cmd):
        return None
    
    monkeypatch.setattr("shutil.which", mock_which)