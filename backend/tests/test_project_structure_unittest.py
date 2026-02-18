import unittest
from pathlib import Path


class ProjectStructureTests(unittest.TestCase):
    def test_frontend_core_files_exist(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        required = [
            repo_root / "frontend" / "app" / "page.tsx",
            repo_root / "frontend" / "app" / "layout.tsx",
            repo_root / "frontend" / "components" / "nav.tsx",
            repo_root / "frontend" / "package.json",
        ]

        for file_path in required:
            self.assertTrue(file_path.exists(), f"Missing required file: {file_path}")


if __name__ == "__main__":
    unittest.main()
