from pathlib import Path
import shutil
import subprocess
import tempfile
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
    def test_build_uses_only_git_tracked_source_files(self):
        build_script = (ROOT / "release" / "build.sh").read_text(encoding="utf-8")

        self.assertIn('git -C "$ROOT" ls-files --cached -z --', build_script)
        self.assertIn("while IFS= read -r -d '' rel", build_script)
        self.assertNotIn('find "$ROOT"', build_script)
        self.assertNotIn("*.tmp", build_script)

    def test_build_manifest_is_checkout_independent(self):
        build_script = (ROOT / "release" / "build.sh").read_text(encoding="utf-8")

        self.assertIn('source_commit=$(git -C "$ROOT" rev-parse HEAD)', build_script)
        self.assertNotIn("created=$(date", build_script)
        self.assertNotIn("source_root=$ROOT", build_script)

    def test_known_hosts_validation_artifact_is_not_tracked(self):
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z", "--"],
            check=True,
            capture_output=True,
        )
        tracked_files = set(result.stdout.decode("utf-8").split("\0"))

        self.assertNotIn("hioc_known_hosts.tmp", tracked_files)

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
        self.assertIn("--exclude .git", backup)
        self.assertIn("--exclude .git", deployment)
        for exclusion in ("state", "history", "logs", "backups"):
            self.assertIn(f"--exclude {exclusion}", backup)
            self.assertIn(f"--exclude {exclusion}", deployment)
        self.assertIn("--exclude runtime/pe4", backup)
        self.assertIn("--exclude runtime/pe4", deployment)
        self.assertNotIn("--exclude .*", backup)
        self.assertNotIn("--exclude '.*'", backup)
        self.assertNotIn("--delete", backup)
        self.assertNotIn("--delete", deployment)
        self.assertNotIn("--delete-excluded", deployment)

    def test_rollback_copy_contract(self):
        rollback_script = (ROOT / "release" / "rollback.sh").read_text(encoding="utf-8")
        commands = rsync_commands(rollback_script)
        restoration = next(
            command
            for command in commands
            if '"$BACKUP_DIR/current/" "$INSTALL_DIR/"' in command
        )

        self.assertIn("--exclude .git", restoration)
        self.assertIn("--exclude runtime/pe4", restoration)
        self.assertNotIn("--exclude .*", restoration)
        self.assertNotIn("--exclude '.*'", restoration)
        self.assertNotIn("--delete", restoration)
        self.assertNotIn("--delete-excluded", restoration)

    @unittest.skipUnless(shutil.which("rsync"), "rsync is not installed")
    def test_git_exclusion_preserves_legitimate_hidden_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "backup" / "current"
            destination = root / "runtime"
            (source / ".git").mkdir(parents=True)
            (source / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
            (source / ".git" / "config").write_text("[core]\n", encoding="utf-8")
            (source / "nested" / ".git").mkdir(parents=True)
            (source / "nested" / ".git" / "HEAD").write_text("nested\n", encoding="utf-8")
            (source / ".env.example").write_text("safe=true\n", encoding="utf-8")
            (source / ".operator").mkdir()
            (source / ".operator" / "settings").write_text("preserve\n", encoding="utf-8")
            (source / "pi4").mkdir()
            (source / "pi4" / "app.py").write_text("pass\n", encoding="utf-8")

            subprocess.run(
                ["rsync", "-a", "--exclude", ".git", f"{source}/", f"{destination}/"],
                check=True,
            )

            self.assertFalse((destination / ".git").exists())
            self.assertFalse((destination / "nested" / ".git").exists())
            self.assertEqual((destination / ".env.example").read_text(encoding="utf-8"), "safe=true\n")
            self.assertEqual(
                (destination / ".operator" / "settings").read_text(encoding="utf-8"),
                "preserve\n",
            )
            self.assertEqual((destination / "pi4" / "app.py").read_text(encoding="utf-8"), "pass\n")

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
        self.assertIn("--exclude .git", deployment)
        self.assertIn("--exclude '/runtime/pe4/'", deployment)
        self.assertNotIn("--delete", deployment)
        self.assertNotIn("--delete-excluded", deployment)

    def test_validation_boundaries(self):
        release_validator = (ROOT / "release" / "validate.sh").read_text(encoding="utf-8")
        runtime_validator = (ROOT / "pi4" / "validate_pi4.sh").read_text(encoding="utf-8")

        self.assertIn('"$ROOT/tests"', release_validator)
        self.assertNotIn("tests/", runtime_validator)
        self.assertNotIn("/tests", runtime_validator)
        self.assertIn("hioc-validate-mqtt.py", runtime_validator)

    def test_runtime_version_comes_from_version_manifest(self):
        platform_status = (ROOT / "pi4" / "bin" / "hioc-platform-status.py").read_text(
            encoding="utf-8"
        )

        self.assertIn('read_version_manifest(home / "VERSION.yaml")', platform_status)
        self.assertNotIn(".git", platform_status)
        self.assertNotIn("git ", platform_status)

    def test_mqtt_runtime_validator_is_installed_executable(self):
        install_script = (ROOT / "pi4" / "install_pi4.sh").read_text(encoding="utf-8")

        self.assertIn(
            'chmod +x "$INSTALL_DIR/pi4/bin/hioc-validate-mqtt.py"',
            install_script,
        )

    def test_upgrade_invokes_non_executable_installer_through_bash(self):
        upgrade_script = (ROOT / "release" / "upgrade.sh").read_text(encoding="utf-8")

        self.assertIn('bash "$INSTALL_DIR/pi4/install_pi4.sh"', upgrade_script)
        self.assertNotIn('\n"$INSTALL_DIR/pi4/install_pi4.sh"', upgrade_script)


if __name__ == "__main__":
    unittest.main()
