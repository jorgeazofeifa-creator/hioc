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
$SupportPath = 'governance/python-runtime-support.json'
$ScriptPath = 'tools/hioc-python313-validate.ps1'
$ExpectedImplementation = 'CPython'
$ExpectedMajorMinor = '3.13'
$InstallerPackageId = '9NQ7512CXL7T'
$MaxNativeCaptureChars = 1048576
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

function ConvertTo-NativeArgument([string]$Value) {
    if ($null -eq $Value -or $Value.Length -eq 0) { return '""' }
    if ($Value -notmatch '[\s"]') { return $Value }
    $Builder = New-Object System.Text.StringBuilder
    [void]$Builder.Append('"')
    $Backslashes = 0
    foreach ($Character in $Value.ToCharArray()) {
        if ($Character -eq '\') {
            $Backslashes++
        }
        elseif ($Character -eq '"') {
            [void]$Builder.Append(('\' * (($Backslashes * 2) + 1)))
            [void]$Builder.Append('"')
            $Backslashes = 0
        }
        else {
            if ($Backslashes -gt 0) { [void]$Builder.Append(('\' * $Backslashes)) }
            [void]$Builder.Append($Character)
            $Backslashes = 0
        }
    }
    if ($Backslashes -gt 0) { [void]$Builder.Append(('\' * ($Backslashes * 2))) }
    [void]$Builder.Append('"')
    return $Builder.ToString()
}

function Limit-NativeOutput([string]$Value) {
    if ($null -eq $Value) { return '' }
    if ($Value.Length -le $MaxNativeCaptureChars) { return $Value }
    return $Value.Substring(0, $MaxNativeCaptureChars)
}

function Invoke-NativeProcess([string]$FilePath, [string[]]$ArgumentList) {
    $StartInfo = New-Object System.Diagnostics.ProcessStartInfo
    $StartInfo.FileName = $FilePath
    $StartInfo.Arguments = (($ArgumentList | ForEach-Object { ConvertTo-NativeArgument $_ }) -join ' ')
    $StartInfo.UseShellExecute = $false
    $StartInfo.CreateNoWindow = $true
    $StartInfo.RedirectStandardOutput = $true
    $StartInfo.RedirectStandardError = $true
    $Process = New-Object System.Diagnostics.Process
    $Process.StartInfo = $StartInfo
    try {
        if (-not $Process.Start()) {
            return [pscustomobject]@{ ExitCode = -1; Stdout = ''; Stderr = '' }
        }
        $StdoutTask = $Process.StandardOutput.ReadToEndAsync()
        $StderrTask = $Process.StandardError.ReadToEndAsync()
        $Process.WaitForExit()
        return [pscustomobject]@{
            ExitCode = $Process.ExitCode
            Stdout = Limit-NativeOutput $StdoutTask.Result
            Stderr = Limit-NativeOutput $StderrTask.Result
        }
    }
    finally {
        $Process.Dispose()
    }
}

function Invoke-Git([string[]]$Arguments) {
    return Invoke-NativeProcess $GitCommand.Source $Arguments
}

function Get-NativeText($Result) {
    return (($Result.Stdout + "`n" + $Result.Stderr).Trim())
}

function Invoke-PythonCheck([string[]]$Arguments) {
    $Result = Invoke-NativeProcess $PythonCommand.Source (@($PythonPrefix) + $Arguments)
    $Text = Get-NativeText $Result
    $Ran = 0
    $Skipped = 0
    $RanMatch = [regex]::Match($Text, 'Ran ([0-9]+) tests?')
    if ($RanMatch.Success) { $Ran = [int]$RanMatch.Groups[1].Value }
    $SkipMatch = [regex]::Match($Text, 'OK \(skipped=([0-9]+)\)')
    if ($SkipMatch.Success) { $Skipped = [int]$SkipMatch.Groups[1].Value }
    return [pscustomobject]@{ Passed = ($Result.ExitCode -eq 0); Ran = $Ran; Skipped = $Skipped }
}

function Get-Managed313Inventory {
    $Result = Invoke-NativeProcess $ManagerCommand.Source @('list', '--one', '--format=json', '--only-managed', $ExpectedMajorMinor)
    if ($Result.ExitCode -ne 0) {
        return [pscustomobject]@{ Valid = $false; Count = 0 }
    }
    try {
        $Parsed = $Result.Stdout | ConvertFrom-Json
    }
    catch {
        return [pscustomobject]@{ Valid = $false; Count = 0 }
    }
    if ($null -eq $Parsed) { return [pscustomobject]@{ Valid = $true; Count = 0 } }
    $Entries = @($Parsed)
    if ($Entries.Count -gt 1) { return [pscustomobject]@{ Valid = $false; Count = $Entries.Count } }
    return [pscustomobject]@{ Valid = $true; Count = $Entries.Count }
}

if ([string]::IsNullOrWhiteSpace($Repo) -or
    $GovernanceCommit -cnotmatch '^[0-9a-f]{40}$' -or
    $ExpectedMajorMinor -cne '3.13' -or
    $InstallerPackageId -cne '9NQ7512CXL7T') {
    Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_CHECKPOINT_INPUT_INVALID'
    return
}

# Runtime-launch aliases may install a default runtime when none exists. Keep
# that behavior disabled for the complete governed session; only an explicit
# pymanager install command is authorized to install a runtime.
[Environment]::SetEnvironmentVariable('PYTHON_MANAGER_AUTOMATIC_INSTALL', 'false', 'Process')
[Environment]::SetEnvironmentVariable('PYLAUNCHER_ALLOW_INSTALL', $null, 'Process')

$GitCommand = Get-Command -Name 'git' -CommandType Application -ErrorAction SilentlyContinue
if ($null -eq $GitCommand) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'GIT_NOT_RESOLVABLE'; return }

$Stage = 'REPOSITORY_CHECK'
if (-not (Test-Path -LiteralPath $Repo -PathType Container)) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'REPOSITORY_MISSING'; return }
$BranchResult = Invoke-Git @('-C', $Repo, 'branch', '--show-current')
$Branch = $BranchResult.Stdout.Trim()
if ($BranchResult.ExitCode -ne 0 -or $Branch -ne 'main') { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'REPOSITORY_BRANCH_INVALID'; return }
$HeadResult = Invoke-Git @('-C', $Repo, 'rev-parse', 'HEAD')
$Head = $HeadResult.Stdout.Trim()
if ($HeadResult.ExitCode -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'GIT_HEAD_CHECK_FAILED'; return }
$OriginResult = Invoke-Git @('-C', $Repo, 'rev-parse', 'origin/main')
$Origin = $OriginResult.Stdout.Trim()
if ($OriginResult.ExitCode -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'GIT_ORIGIN_CHECK_FAILED'; return }
if ($Head -ne $GovernanceCommit -or $Origin -ne $GovernanceCommit) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'GOVERNANCE_COMMIT_MISMATCH'; return }

$Stage = 'SCRIPT_IDENTITY'
$ExpectedScriptPath = [IO.Path]::GetFullPath((Join-Path $Repo $ScriptPath))
$ActualScriptPath = [IO.Path]::GetFullPath($PSCommandPath)
if (-not $ActualScriptPath.Equals($ExpectedScriptPath, [StringComparison]::OrdinalIgnoreCase)) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_CHECKPOINT_SCRIPT_IDENTITY_MISMATCH'; return }
$ScriptSpec = '{0}:{1}' -f $GovernanceCommit, $ScriptPath
$ExpectedBlobResult = Invoke-Git @('-C', $Repo, 'rev-parse', $ScriptSpec)
$ExpectedScriptBlob = $ExpectedBlobResult.Stdout.Trim()
$ActualBlobResult = Invoke-Git @('-C', $Repo, 'hash-object', ('--path=' + $ScriptPath), '--', $ActualScriptPath)
$ActualScriptBlob = $ActualBlobResult.Stdout.Trim()
if ($ExpectedBlobResult.ExitCode -ne 0 -or $ActualBlobResult.ExitCode -ne 0 -or $ExpectedScriptBlob -cnotmatch '^[0-9a-f]{40}$' -or $ActualScriptBlob -ne $ExpectedScriptBlob) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_CHECKPOINT_SCRIPT_IDENTITY_MISMATCH'; return }
$ScriptDiff = Invoke-Git @('-C', $Repo, 'diff', '--quiet', $GovernanceCommit, '--', $ScriptPath)
if ($ScriptDiff.ExitCode -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_CHECKPOINT_SCRIPT_IDENTITY_MISMATCH'; return }
$StatusResult = Invoke-Git @('-C', $Repo, 'status', '--porcelain')
if ($StatusResult.ExitCode -ne 0 -or -not [string]::IsNullOrWhiteSpace($StatusResult.Stdout)) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'REPOSITORY_DIRTY'; return }

$Stage = 'SUPPORT_STATE_CHECK'
$SupportSpec = '{0}:{1}' -f $GovernanceCommit, $SupportPath
$SupportResult = Invoke-Git @('-C', $Repo, 'show', $SupportSpec)
if ($SupportResult.ExitCode -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_SUPPORT_STATE_INVALID'; return }
try { $Support = $SupportResult.Stdout | ConvertFrom-Json } catch { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_SUPPORT_STATE_INVALID'; return }
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
$WingetList = Invoke-NativeProcess $Winget.Source @('list', '--id', $InstallerPackageId, '--exact', '--accept-source-agreements', '--disable-interactivity')
if ($WingetList.ExitCode -ne 0) {
    $WingetInstall = Invoke-NativeProcess $Winget.Source @('install', '--id', $InstallerPackageId, '--exact', '--source', 'msstore', '--accept-package-agreements', '--accept-source-agreements', '--disable-interactivity')
    if ($WingetInstall.ExitCode -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'OFFICIAL_PYTHON_INSTALL_MANAGER_FAILED'; return }
}

$Stage = 'PYTHON_MANAGER_RESOLUTION'
$ManagerCommand = Get-Command -Name 'pymanager' -CommandType Application -ErrorAction SilentlyContinue
if ($null -eq $ManagerCommand) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_INSTALL_MANAGER_NOT_RESOLVABLE'; return }
$Managed313 = Get-Managed313Inventory
if (-not $Managed313.Valid) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_MANAGED_INVENTORY_INVALID'; return }

if ($Managed313.Count -eq 0) {
    $Stage = 'PYTHON_INSTALLATION'
    $Install313 = Invoke-NativeProcess $ManagerCommand.Source @('install', $ExpectedMajorMinor)
    if ($Install313.ExitCode -ne 0) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'CPYTHON_313_INSTALL_FAILED'; return }
    $Managed313 = Get-Managed313Inventory
    if (-not $Managed313.Valid -or $Managed313.Count -ne 1) { Write-CheckpointFailure 'VALIDATION_FAIL' 'CPYTHON_313_INSTALL_VERIFICATION_FAILED'; return }
}

$Stage = 'PYTHON_PROBE'
$PythonCommand = Get-Command -Name 'py' -CommandType Application -ErrorAction SilentlyContinue
if ($null -eq $PythonCommand) { Write-CheckpointFailure 'VALIDATION_FAIL' 'CPYTHON_313_LAUNCHER_NOT_RESOLVABLE'; return }
$PythonPrefix = @('-3.13')
$ProbeCode = 'import platform,sys; print(platform.python_implementation()+"|"+platform.python_version())'
$Probe = Invoke-NativeProcess $PythonCommand.Source (@($PythonPrefix) + @('-c', $ProbeCode))
$ProbeLine = ($Probe.Stdout -split "`r?`n" | Select-Object -First 1).Trim()
if ($Probe.ExitCode -ne 0 -or $ProbeLine -cnotmatch '^CPython\|3\.13\.[0-9]+$') { Write-CheckpointFailure 'VALIDATION_FAIL' 'CPYTHON_313_PROBE_FAILED'; return }
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
$Compilation = Invoke-NativeProcess $PythonCommand.Source (@($PythonPrefix) + @('-m', 'compileall', '-q', (Join-Path $Repo 'pi4'), (Join-Path $Repo 'tools'), (Join-Path $Repo 'tests')))
if ($Compilation.ExitCode -ne 0) { Write-CheckpointFailure 'VALIDATION_FAIL' 'PYTHON_COMPILATION_FAILED'; return }

$Stage = 'FINAL_REPOSITORY_CHECK'
$FinalHeadResult = Invoke-Git @('-C', $Repo, 'rev-parse', 'HEAD')
$FinalOriginResult = Invoke-Git @('-C', $Repo, 'rev-parse', 'origin/main')
$FinalStatusResult = Invoke-Git @('-C', $Repo, 'status', '--porcelain')
$FinalHead = $FinalHeadResult.Stdout.Trim()
$FinalOrigin = $FinalOriginResult.Stdout.Trim()
if ($FinalHeadResult.ExitCode -ne 0 -or $FinalOriginResult.ExitCode -ne 0 -or $FinalStatusResult.ExitCode -ne 0 -or $FinalHead -ne $GovernanceCommit -or $FinalOrigin -ne $GovernanceCommit -or -not [string]::IsNullOrWhiteSpace($FinalStatusResult.Stdout)) { Write-CheckpointFailure 'VALIDATION_FAIL' 'FINAL_REPOSITORY_STATE_FAILED'; return }

Write-Output 'RESULT=PASS'
Write-Output "PYTHON_IMPLEMENTATION=$ExpectedImplementation"
Write-Output "PYTHON_VERSION=$ExactVersion"
Write-Output 'PYTHON_MANAGER=pymanager'
Write-Output 'PYTHON_RESOLVER=py -3.13'
Write-Output 'SUPPORT_STATE_BEFORE_VALIDATION=validation_pending'
Write-Output 'FULL_SUITE_RESULT=PASS'
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
