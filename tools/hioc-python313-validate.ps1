param(
    [Parameter(Mandatory=$true)]
    [string]$Repo,

    [Parameter(Mandatory=$true)]
    [ValidatePattern('^[0-9a-f]{40}$')]
    [string]$GovernanceCommit
)

function Invoke-HIOCPython313Validation {
try {
$ErrorActionPreference = 'Stop'
$Stage = 'INITIALIZATION'
$Git = 'git'
$SupportPath = 'governance/python-runtime-support.json'
$ScriptPath = 'tools/hioc-python313-validate.ps1'
$ExpectedImplementation = 'CPython'
$ExpectedMajorMinor = '3.13'
$InstallerPackageId = '9NQ7512CXL7T'
$PriorPycachePrefix = [Environment]::GetEnvironmentVariable('PYTHONPYCACHEPREFIX', 'Process')
$PriorAutomaticInstall = [Environment]::GetEnvironmentVariable('PYTHON_MANAGER_AUTOMATIC_INSTALL', 'Process')
$PriorLauncherAllowInstall = [Environment]::GetEnvironmentVariable('PYLAUNCHER_ALLOW_INSTALL', 'Process')
$PriorLocation = Get-Location
$TempRoot = $null

function Write-CheckpointFailure([string]$Result, [string]$Code) {
    Write-Output "RESULT=$Result"
    Write-Output "ERROR_CODE=$Code"
    Write-Output "FAILURE_STAGE=$Stage"
    Write-Output 'ROLLBACK_RECOMMENDED=FALSE'
}

function Invoke-PythonCheck([string[]]$Arguments) {
    $Output = @(& $PythonCommand.Source @PythonPrefix @Arguments 2>&1)
    $Code = $LASTEXITCODE
    $Text = $Output -join "`n"
    $Ran = 0
    $Skipped = 0
    $RanMatch = [regex]::Match($Text, 'Ran ([0-9]+) tests?')
    if ($RanMatch.Success) { $Ran = [int]$RanMatch.Groups[1].Value }
    $SkipMatch = [regex]::Match($Text, 'OK \(skipped=([0-9]+)\)')
    if ($SkipMatch.Success) { $Skipped = [int]$SkipMatch.Groups[1].Value }
    [pscustomobject]@{ Passed = ($Code -eq 0); Ran = $Ran; Skipped = $Skipped }
}

if ([string]::IsNullOrWhiteSpace($Repo) -or
    $GovernanceCommit -cnotmatch '^[0-9a-f]{40}$' -or
    $ExpectedMajorMinor -cne '3.13' -or
    $InstallerPackageId -cne '9NQ7512CXL7T') {
    Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_CHECKPOINT_INPUT_INVALID'
    return
}

$Stage = 'REPOSITORY_CHECK'
if (-not (Test-Path -LiteralPath $Repo -PathType Container)) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'REPOSITORY_MISSING'; return }
$Branch = & $Git -C $Repo branch --show-current 2>$null
if ($LASTEXITCODE -ne 0 -or $Branch -ne 'main') { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'REPOSITORY_BRANCH_INVALID'; return }
$Head = & $Git -C $Repo rev-parse HEAD 2>$null
if ($LASTEXITCODE -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'GIT_HEAD_CHECK_FAILED'; return }
$Origin = & $Git -C $Repo rev-parse origin/main 2>$null
if ($LASTEXITCODE -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'GIT_ORIGIN_CHECK_FAILED'; return }
if ($Head -ne $GovernanceCommit -or $Origin -ne $GovernanceCommit) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'GOVERNANCE_COMMIT_MISMATCH'; return }

$Stage = 'SCRIPT_IDENTITY'
$ExpectedScriptPath = [IO.Path]::GetFullPath((Join-Path $Repo $ScriptPath))
$ActualScriptPath = [IO.Path]::GetFullPath($PSCommandPath)
if (-not $ActualScriptPath.Equals($ExpectedScriptPath, [StringComparison]::OrdinalIgnoreCase)) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_CHECKPOINT_SCRIPT_IDENTITY_MISMATCH'; return }
$ScriptSpec = '{0}:{1}' -f $GovernanceCommit, $ScriptPath
$ExpectedScriptBlob = & $Git -C $Repo rev-parse $ScriptSpec 2>$null
$ActualScriptBlob = & $Git -C $Repo hash-object --path=$ScriptPath -- $ActualScriptPath 2>$null
if ($LASTEXITCODE -ne 0 -or $ExpectedScriptBlob -cnotmatch '^[0-9a-f]{40}$' -or $ActualScriptBlob -ne $ExpectedScriptBlob) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_CHECKPOINT_SCRIPT_IDENTITY_MISMATCH'; return }
& $Git -C $Repo diff --quiet $GovernanceCommit -- $ScriptPath
if ($LASTEXITCODE -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_CHECKPOINT_SCRIPT_IDENTITY_MISMATCH'; return }
$RepositoryStatus = @(& $Git -C $Repo status --porcelain 2>$null)
if ($LASTEXITCODE -ne 0 -or $RepositoryStatus.Count -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'REPOSITORY_DIRTY'; return }

$Stage = 'SUPPORT_STATE_CHECK'
$SupportSpec = '{0}:{1}' -f $GovernanceCommit, $SupportPath
$SupportText = & $Git -C $Repo show $SupportSpec 2>$null
if ($LASTEXITCODE -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_SUPPORT_STATE_INVALID'; return }
try { $Support = ($SupportText -join "`n") | ConvertFrom-Json } catch { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_SUPPORT_STATE_INVALID'; return }
if ($Support.schema_version -ne 1 -or
    $Support.implementation -cne $ExpectedImplementation -or
    $Support.language_floor -cne '3.10' -or
    $Support.windows_operator.major_minor -cne $ExpectedMajorMinor -or
    $Support.windows_operator.status -cne 'validation_pending' -or
    $null -ne $Support.windows_operator.validated_patch) {
    Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_SUPPORT_STATE_NOT_PENDING'
    return
}

$Stage = 'INSTALL_MANAGER'
$Winget = Get-Command -Name 'winget' -CommandType Application -ErrorAction SilentlyContinue
if ($null -eq $Winget) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'OFFICIAL_PYTHON_INSTALL_MANAGER_UNAVAILABLE'; return }
& $Winget.Source list --id $InstallerPackageId --exact --accept-source-agreements --disable-interactivity *> $null
$InstallManagerPresent = ($LASTEXITCODE -eq 0)
if (-not $InstallManagerPresent) {
    & $Winget.Source install --id $InstallerPackageId --exact --source msstore --accept-package-agreements --accept-source-agreements --disable-interactivity *> $null
    if ($LASTEXITCODE -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'OFFICIAL_PYTHON_INSTALL_MANAGER_FAILED'; return }
}

$Stage = 'PYTHON_INSTALLATION'
$PythonCommand = Get-Command -Name 'py' -CommandType Application -ErrorAction SilentlyContinue
if ($null -eq $PythonCommand) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_INSTALL_MANAGER_NOT_RESOLVABLE'; return }
& $PythonCommand.Source install $ExpectedMajorMinor *> $null
if ($LASTEXITCODE -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'CPYTHON_313_INSTALL_FAILED'; return }

$Stage = 'PYTHON_PROBE'
$PythonPrefix = @('-3.13')
[Environment]::SetEnvironmentVariable('PYTHON_MANAGER_AUTOMATIC_INSTALL', 'false', 'Process')
[Environment]::SetEnvironmentVariable('PYLAUNCHER_ALLOW_INSTALL', $null, 'Process')
$ProbeCode = 'import platform,sys; print(platform.python_implementation()+"|"+platform.python_version())'
$Probe = @(& $PythonCommand.Source @PythonPrefix -c $ProbeCode 2>$null)
$ProbeLine = $Probe | Select-Object -First 1
if ($LASTEXITCODE -ne 0 -or $ProbeLine -cnotmatch '^CPython\|3\.13\.[0-9]+$') { Write-CheckpointFailure 'VALIDATION_FAIL' 'CPYTHON_313_PROBE_FAILED'; return }
$ExactVersion = $ProbeLine.Substring('CPython|'.Length)

$TempRoot = Join-Path ([IO.Path]::GetTempPath()) ('hioc-python313-' + [guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($TempRoot) | Out-Null
[Environment]::SetEnvironmentVariable('PYTHONPYCACHEPREFIX', (Join-Path $TempRoot 'pycache'), 'Process')
Set-Location -LiteralPath $Repo

$Stage = 'FULL_REGRESSION'
$Full = Invoke-PythonCheck @('-m', 'unittest', 'discover', '-s', 'tests')
if (-not $Full.Passed -or $Full.Ran -le 0) { Write-CheckpointFailure 'VALIDATION_FAIL' 'FULL_REGRESSION_FAILED'; return }

$Stage = 'PYTHON_POLICY_TESTS'
$Policy = Invoke-PythonCheck @('-m', 'unittest', 'tests.test_python_runtime_compatibility')
if (-not $Policy.Passed -or $Policy.Ran -le 0) { Write-CheckpointFailure 'VALIDATION_FAIL' 'PYTHON_POLICY_TESTS_FAILED'; return }

$Stage = 'ACTION1_GOVERNANCE_TESTS'
$Action1 = Invoke-PythonCheck @('-m', 'unittest', 'tests.test_pe3_action1_runbook')
if (-not $Action1.Passed -or $Action1.Ran -le 0) { Write-CheckpointFailure 'VALIDATION_FAIL' 'ACTION1_GOVERNANCE_TESTS_FAILED'; return }

$Stage = 'MANUFACTURER_TESTS'
$Manufacturer = Invoke-PythonCheck @('-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_manufacturer_*.py')
if (-not $Manufacturer.Passed -or $Manufacturer.Ran -le 0) { Write-CheckpointFailure 'VALIDATION_FAIL' 'MANUFACTURER_TESTS_FAILED'; return }

$Stage = 'PYTHON_COMPILATION'
& $PythonCommand.Source @PythonPrefix -m compileall -q (Join-Path $Repo 'pi4') (Join-Path $Repo 'tools') (Join-Path $Repo 'tests') *> $null
if ($LASTEXITCODE -ne 0) { Write-CheckpointFailure 'VALIDATION_FAIL' 'PYTHON_COMPILATION_FAILED'; return }

$Stage = 'FINAL_REPOSITORY_CHECK'
$FinalHead = & $Git -C $Repo rev-parse HEAD 2>$null
$FinalOrigin = & $Git -C $Repo rev-parse origin/main 2>$null
$FinalStatus = @(& $Git -C $Repo status --porcelain 2>$null)
if ($LASTEXITCODE -ne 0 -or $FinalHead -ne $GovernanceCommit -or $FinalOrigin -ne $GovernanceCommit -or $FinalStatus.Count -ne 0) { Write-CheckpointFailure 'VALIDATION_FAIL' 'FINAL_REPOSITORY_STATE_FAILED'; return }

Write-Output 'RESULT=PASS'
Write-Output "PYTHON_IMPLEMENTATION=$ExpectedImplementation"
Write-Output "PYTHON_VERSION=$ExactVersion"
Write-Output 'PYTHON_RESOLVER=py -3.13'
Write-Output 'SUPPORT_STATE_BEFORE_VALIDATION=validation_pending'
Write-Output "FULL_SUITE_RESULT=PASS"
Write-Output "FULL_SUITE_TESTS=$($Full.Ran)"
Write-Output "FULL_SUITE_SKIPS=$($Full.Skipped)"
Write-Output "PYTHON_POLICY_TESTS=PASS:$($Policy.Ran)"
Write-Output "ACTION1_GOVERNANCE_TESTS=PASS:$($Action1.Ran)"
Write-Output "MANUFACTURER_TESTS=PASS:$($Manufacturer.Ran)"
Write-Output 'PYTHON_COMPILATION=PASS'
Write-Output "REPOSITORY_HEAD=$FinalHead"
Write-Output 'WORKING_TREE_CLEAN=TRUE'
Write-Output 'PROMOTE_TO_SUPPORTED=TRUE'
Write-Output 'ROLLBACK_RECOMMENDED=FALSE'
return
}
catch {
    Write-Output 'RESULT=VALIDATION_FAIL'
    Write-Output 'ERROR_CODE=PYTHON_CHECKPOINT_UNEXPECTED_ERROR'
    Write-Output "FAILURE_STAGE=$Stage"
    Write-Output 'ROLLBACK_RECOMMENDED=FALSE'
    return
}
finally {
    Set-Location -LiteralPath $PriorLocation -ErrorAction SilentlyContinue
    [Environment]::SetEnvironmentVariable('PYTHONPYCACHEPREFIX', $PriorPycachePrefix, 'Process')
    [Environment]::SetEnvironmentVariable('PYTHON_MANAGER_AUTOMATIC_INSTALL', $PriorAutomaticInstall, 'Process')
    [Environment]::SetEnvironmentVariable('PYLAUNCHER_ALLOW_INSTALL', $PriorLauncherAllowInstall, 'Process')
    if ($null -ne $TempRoot -and (Test-Path -LiteralPath $TempRoot -PathType Container)) {
        Remove-Item -LiteralPath $TempRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}
}

Invoke-HIOCPython313Validation
