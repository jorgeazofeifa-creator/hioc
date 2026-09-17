<#
PE-4.0B.2a-B replacement transaction wrapper.

This source is intentionally not a retry mechanism.  A separately authorized
operator invokes it once only after this repository revision is published, PI3
source is synchronized, failed-staging disposition is reviewed, and a fresh
readiness review has passed.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$PythonPath,
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[0-9a-f]{40}$')]
    [string]$GovernanceCommit
)

$ErrorActionPreference = 'Stop'
$Repository = Split-Path -Parent $PSScriptRoot
$ActionBTool = Join-Path $PSScriptRoot 'hioc-pe4-artifact-transfer.py'
$HistoricalTransfer = '/tmp/hioc-pe4-artifact-transfer-7g3xp1lk'
$FailedReplacementTransfer = '/tmp/hioc-pe4-artifact-transfer-g_jrlqkl'

function Test-HIOCStructuredArgumentTransport {
    if ($PSVersionTable.PSEdition -ne 'Core') {
        throw 'STRUCTURED_ARGUMENT_TRANSPORT_UNAVAILABLE'
    }
    $probe = [Diagnostics.ProcessStartInfo]::new()
    if ($null -eq $probe.ArgumentList) {
        throw 'STRUCTURED_ARGUMENT_TRANSPORT_UNAVAILABLE'
    }
}

function ConvertFrom-HIOCDivergence {
    param([Parameter(Mandatory = $true)][string]$NativeOutput)
    $match = [regex]::Match($NativeOutput, '\A[ \t]*([0-9]+)[ \t]+([0-9]+)\r?\n?\z')
    if (-not $match.Success) { throw 'AHEAD_BEHIND_MALFORMED' }
    try {
        $behind = [UInt64]::Parse($match.Groups[1].Value)
        $ahead = [UInt64]::Parse($match.Groups[2].Value)
    } catch { throw 'AHEAD_BEHIND_MALFORMED' }
    if ($behind -ne 0 -or $ahead -ne 0) { throw 'AHEAD_BEHIND_MISMATCH' }
    return [pscustomobject]@{ Behind = $behind; Ahead = $ahead }
}

function Test-HIOCNoActiveGitOperation {
    param([Parameter(Mandatory = $true)][string]$RepositoryPath)
    $gitDirectory = (& git -C $RepositoryPath rev-parse --git-dir 2>$null).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($gitDirectory)) {
        throw 'GIT_DIRECTORY_UNAVAILABLE'
    }
    $absoluteGitDirectory = [IO.Path]::GetFullPath((Join-Path $RepositoryPath $gitDirectory))
    if (@('MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'REBASE_HEAD') |
            Where-Object { Test-Path -LiteralPath (Join-Path $absoluteGitDirectory $_) }) {
        throw 'ACTIVE_GIT_OPERATION'
    }
}

function Test-HIOCRepository {
    param([Parameter(Mandatory = $true)][string]$RepositoryPath,
          [Parameter(Mandatory = $true)][string]$Commit)
    if (-not (Test-Path -LiteralPath $RepositoryPath -PathType Container)) {
        throw 'REPOSITORY_MISSING'
    }
    $branch = (& git -C $RepositoryPath branch --show-current 2>$null).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -cne 'main') { throw 'BRANCH_MISMATCH' }
    $head = (& git -C $RepositoryPath rev-parse HEAD 2>$null).Trim()
    $origin = (& git -C $RepositoryPath rev-parse origin/main 2>$null).Trim()
    if ($LASTEXITCODE -ne 0 -or $head -cne $Commit -or $origin -cne $Commit) {
        throw 'GOVERNANCE_COMMIT_MISMATCH'
    }
    $divergence = (& git -C $RepositoryPath rev-list --left-right --count origin/main...HEAD 2>$null | Out-String)
    ConvertFrom-HIOCDivergence -NativeOutput $divergence | Out-Null
    $status = (& git -C $RepositoryPath status --porcelain=v1 --untracked-files=all 2>$null | Out-String)
    if ($LASTEXITCODE -ne 0 -or -not [string]::IsNullOrWhiteSpace($status)) {
        throw 'WORKTREE_NOT_CLEAN'
    }
    Test-HIOCNoActiveGitOperation -RepositoryPath $RepositoryPath
}

function Invoke-HIOCPython {
    param([Parameter(Mandatory = $true)][string]$Python,
          [Parameter(Mandatory = $true)][string[]]$Arguments,
          [Parameter(Mandatory = $true)][string]$Stage)
    $startInfo = [Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = $Python
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    foreach ($argument in $Arguments) { [void]$startInfo.ArgumentList.Add($argument) }
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    if (-not $process.Start()) { throw "$Stage`_PROCESS_START_FAILED" }
    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()
    [Console]::Out.Write($stdout)
    [Console]::Error.Write($stderr)
    return [pscustomobject]@{ ExitCode = $process.ExitCode; Stdout = $stdout; Stderr = $stderr }
}

function Invoke-HIOCActionBTool {
    param([Parameter(Mandatory = $true)][string]$Python,
          [Parameter(Mandatory = $true)][string]$Tool,
          [Parameter(Mandatory = $true)][string]$Commit)
    return Invoke-HIOCPython -Python $Python -Arguments @(
        '-B', $Tool, '--governance-commit', $Commit
    ) -Stage 'ACTION_B'
}

function Test-HIOCActionBSuccess {
    param([Parameter(Mandatory = $true)][string]$Stdout,
          [Parameter(Mandatory = $true)][string]$Python,
          [Parameter(Mandatory = $true)][string]$ToolsDirectory)
    $required = @(
        'REMOTE_STAGING_CREATED=TRUE', 'WHEEL_TRANSFERRED=TRUE',
        'LOCK_TRANSFERRED=TRUE', 'REMOTE_ARTIFACT_VERIFIED=TRUE',
        'REMOTE_LOCK_VERIFIED=TRUE', 'EVIDENCE_STATE=CONFIRMED',
        'ACTION_B=COMPLETE', 'RESULT=PASS', 'ERROR_CODE=NONE',
        'FAILURE_STAGE=COMPLETE', 'ROLLBACK_RECOMMENDED=FALSE'
    )
    $lines = $Stdout -split "`r?`n"
    $missing = @($required | Where-Object {
        $expectedMarker = $_
        @($lines | Where-Object { $_ -ceq $expectedMarker }).Count -ne 1
    })
    if ($missing.Count -ne 0) {
        throw 'ACTION_B_SUCCESS_MARKERS_INVALID'
    }
    $transfers = @($lines | Where-Object { $_ -match '^TRANSFER_DIRECTORY=(.+)$' })
    if ($transfers.Count -ne 1) { throw 'TRANSFER_DIRECTORY_INVALID' }
    $transfer = [regex]::Match($transfers[0], '^TRANSFER_DIRECTORY=(.+)$').Groups[1].Value
    if ($transfer -ceq $HistoricalTransfer -or $transfer -ceq $FailedReplacementTransfer) {
        throw 'TRANSFER_DIRECTORY_REUSE_FORBIDDEN'
    }
    $validator = 'import sys;sys.path.insert(0,sys.argv[1]);from hioc_pe4_runtime_common import is_transfer_directory;raise SystemExit(0 if is_transfer_directory(sys.argv[2]) else 1)'
    $validation = Invoke-HIOCPython -Python $Python -Arguments @(
        '-B', '-c', $validator, $ToolsDirectory, $transfer
    ) -Stage 'TRANSFER_DIRECTORY_VALIDATION'
    if ($validation.ExitCode -ne 0) { throw 'TRANSFER_DIRECTORY_INVALID' }
    return $transfer
}

& {
    $launched = $false
    try {
        if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) { throw 'MANAGED_PYTHON_MISSING' }
        if (-not (Test-Path -LiteralPath $ActionBTool -PathType Leaf)) { throw 'ACTION_B_TOOL_MISSING' }
        Test-HIOCStructuredArgumentTransport
        Test-HIOCRepository -RepositoryPath $Repository -Commit $GovernanceCommit
        $preflight = 'import pathlib,sys;root=pathlib.Path(sys.argv[1]);sys.path.insert(0,str(root/"tools"));import importlib.util;spec=importlib.util.spec_from_file_location("pe4_action_b",root/"tools"/"hioc-pe4-artifact-transfer.py");tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(tool);tool.local_inputs(sys.argv[2]);tool.validate_local_transport()'
        $preflightResult = Invoke-HIOCPython -Python $PythonPath -Arguments @(
            '-B', '-c', $preflight, $Repository, $GovernanceCommit
        ) -Stage 'ACTION_B_PRECHECK'
        if ($preflightResult.ExitCode -ne 0) { throw 'ACTION_B_PRECHECK_FAILED' }
    } catch {
        Write-Output 'REPLACEMENT_WRAPPER=INVOKED'
        Write-Output 'PRECHECKS=FAILED'
        Write-Output 'ACTION_B_LAUNCH=NOT_STARTED'
        Write-Output 'ACTION_B_TRANSACTION=NOT_STARTED'
        Write-Output 'ACTION_B_REPLACEMENT=NOT_EXECUTED'
        Write-Output "ERROR_CODE=$($_.Exception.Message)"
        Write-Output 'STOP_REQUIRED=TRUE'
        return
    }

    try {
        $launched = $true
        $result = Invoke-HIOCActionBTool -Python $PythonPath -Tool $ActionBTool -Commit $GovernanceCommit
        if ($result.ExitCode -ne 0) { throw 'ACTION_B_TOOL_NONZERO' }
    } catch {
        Write-Output 'REPLACEMENT_WRAPPER=INVOKED'
        Write-Output 'PRECHECKS=PASS'
        Write-Output 'ACTION_B_LAUNCH=STARTED'
        Write-Output 'ACTION_B_TRANSACTION=ATTEMPTED'
        Write-Output 'ACTION_B_REPLACEMENT=ATTEMPTED_NOT_COMPLETE'
        Write-Output "ERROR_CODE=$($_.Exception.Message)"
        Write-Output 'STOP_REQUIRED=TRUE'
        return
    }

    try {
        $transfer = Test-HIOCActionBSuccess -Stdout $result.Stdout -Python $PythonPath -ToolsDirectory $PSScriptRoot
        Write-Output 'REPLACEMENT_WRAPPER=INVOKED'
        Write-Output 'PRECHECKS=PASS'
        Write-Output 'ACTION_B_LAUNCH=STARTED'
        Write-Output 'ACTION_B_TRANSACTION=COMPLETE'
        Write-Output 'ACTION_B_REPLACEMENT=COMPLETE'
        Write-Output 'RESULT=PASS'
        Write-Output "TRANSFER_DIRECTORY=$transfer"
        Write-Output 'STAGING_PRESERVED=TRUE'
        Write-Output 'STOP_REQUIRED=TRUE'
    } catch {
        Write-Output 'REPLACEMENT_WRAPPER=INVOKED'
        Write-Output 'PRECHECKS=PASS'
        Write-Output 'ACTION_B_LAUNCH=STARTED'
        Write-Output 'ACTION_B_TRANSACTION=ATTEMPTED'
        Write-Output 'ACTION_B_REPLACEMENT=ATTEMPTED_POSTCONDITION_FAILED'
        Write-Output "ERROR_CODE=$($_.Exception.Message)"
        Write-Output 'STOP_REQUIRED=TRUE'
    }
}
