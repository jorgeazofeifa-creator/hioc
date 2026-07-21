from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ONLY_EXCLUSIONS = (
    "--exclude '/README.md'",
    "--exclude '/ROADMAP.md'",
    "--exclude '/DECISIONS.md'",
    "--exclude '/CHANGELOG.md'",
    "--exclude '/docs/'",
    "--exclude '/tests/'",
)


def rsync_commands(script: str) -> list[str]:
    lines = script.splitlines()
    commands = []
    index = 0
    while index < len(lines):
        if not lines[index].lstrip().startswith("rsync "):
            index += 1
            continue
        command = [lines[index].strip()]
        while command[-1].endswith("\\"):
            index += 1
            command.append(lines[index].strip())
        commands.append("\n".join(command))
        index += 1
    return commands


class ReleaseScriptTests(unittest.TestCase):
    def test_upgrade_copy_contract(self):
        upgrade_script = (ROOT / "release" / "upgrade.sh").read_text(encoding="utf-8")
        commands = rsync_commands(upgrade_script)
        backup = next(command for command in commands if '"$BACKUP_DIR/current/"' in command)
        deployment = next(
            command
            for command in commands
            if '"$ROOT/" "$INSTALL_DIR/"' in command
        )

        for exclusion in SOURCE_ONLY_EXCLUSIONS:
            self.assertIn(exclusion, deployment)
            self.assertNotIn(exclusion, backup)
        for exclusion in ("state", "history", "logs", "backups"):
            self.assertIn(f"--exclude {exclusion}", deployment)
        self.assertNotIn("--delete", deployment)
        self.assertNotIn("--delete-excluded", deployment)

    def test_pi4_install_copy_contract(self):
        install_script = (ROOT / "pi4" / "install_pi4.sh").read_text(encoding="utf-8")
        commands = rsync_commands(install_script)
        deployment = next(
            command
            for command in commands
            if '"$SRC_DIR/" "$INSTALL_DIR/"' in command
        )

        for exclusion in SOURCE_ONLY_EXCLUSIONS:
            self.assertIn(exclusion, deployment)
        self.assertNotIn("--delete", deployment)
        self.assertNotIn("--delete-excluded", deployment)

    def test_validation_boundaries(self):
        release_validator = (ROOT / "release" / "validate.sh").read_text(encoding="utf-8")
        runtime_validator = (ROOT / "pi4" / "validate_pi4.sh").read_text(encoding="utf-8")

        self.assertIn('"$ROOT/tests"', release_validator)
        self.assertNotIn("tests/", runtime_validator)
        self.assertNotIn("/tests", runtime_validator)

    def test_upgrade_invokes_non_executable_installer_through_bash(self):
        upgrade_script = (ROOT / "release" / "upgrade.sh").read_text(encoding="utf-8")

        self.assertIn('bash "$INSTALL_DIR/pi4/install_pi4.sh"', upgrade_script)
        self.assertNotIn('\n"$INSTALL_DIR/pi4/install_pi4.sh"', upgrade_script)


if __name__ == "__main__":
    unittest.main()
