param(
    [Parameter(Mandatory=$true)]
    [string]$Repo,

    [Parameter(Mandatory=$true)]
    [ValidatePattern('^[0-9a-f]{40}$')]
    [string]$GovernanceCommit
)

function Invoke-HIOCProcessDiagnostic {
try {
$ErrorActionPreference = 'Stop'
$Stage = 'INITIALIZATION'
$MaxCaptureChars = 1048576
$ScriptPath = 'tools/hioc-python313-process-diagnostic.ps1'
$PriorLocation = Get-Location
$PriorPycachePrefix = [Environment]::GetEnvironmentVariable('PYTHONPYCACHEPREFIX', 'Process')
$TempRoot = $null

function Write-DiagnosticFailure([string]$Code) {
    Write-Output 'RESULT=VALIDATION_FAIL'
    Write-Output "ERROR_CODE=$Code"
    Write-Output "FAILURE_STAGE=$Stage"
}

function ConvertTo-NativeArgument([string]$Value) {
    if ($null -eq $Value -or $Value.Length -eq 0) { return '""' }
    if ($Value -notmatch '[\s"]') { return $Value }
    $Builder = New-Object System.Text.StringBuilder
    [void]$Builder.Append('"')
    $Backslashes = 0
    foreach ($Character in $Value.ToCharArray()) {
        if ($Character -eq '\') { $Backslashes++ }
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

function Limit-Output([string]$Value) {
    if ($null -eq $Value) { return '' }
    if ($Value.Length -le $MaxCaptureChars) { return $Value }
    return $Value.Substring($Value.Length - $MaxCaptureChars)
}

function Invoke-ProcessStartInfo([string]$FilePath, [string[]]$ArgumentList) {
    $StartInfo = New-Object System.Diagnostics.ProcessStartInfo
    $StartInfo.FileName = $FilePath
    $StartInfo.Arguments = (($ArgumentList | ForEach-Object { ConvertTo-NativeArgument $_ }) -join ' ')
    $StartInfo.UseShellExecute = $false
    $StartInfo.CreateNoWindow = $true
    $StartInfo.RedirectStandardOutput = $true
    $StartInfo.RedirectStandardError = $true
    $Process = New-Object System.Diagnostics.Process
    $Process.StartInfo = $StartInfo
    $Started = $false
    try {
        $Started = $Process.Start()
        if (-not $Started) {
            return [pscustomobject]@{ Started=$false; Completed=$false; ExitCode=-1; Stdout=''; Stderr=''; StdoutLength=0; StderrLength=0; StdoutTask='NOT_STARTED'; StderrTask='NOT_STARTED' }
        }
        $StdoutTask = $Process.StandardOutput.ReadToEndAsync()
        $StderrTask = $Process.StandardError.ReadToEndAsync()
        $Process.WaitForExit()
        $ExitCode = $Process.ExitCode
        $Stdout = $StdoutTask.GetAwaiter().GetResult()
        $Stderr = $StderrTask.GetAwaiter().GetResult()
        return [pscustomobject]@{
            Started=$true; Completed=$Process.HasExited; ExitCode=$ExitCode
            Stdout=Limit-Output $Stdout; Stderr=Limit-Output $Stderr
            StdoutLength=$Stdout.Length; StderrLength=$Stderr.Length
            StdoutTask=$StdoutTask.Status.ToString(); StderrTask=$StderrTask.Status.ToString()
        }
    }
    finally { $Process.Dispose() }
}

function Invoke-DirectPowerShell([string]$FilePath, [string[]]$ArgumentList, [string]$OutputRoot) {
    $StdoutPath = Join-Path $OutputRoot ([guid]::NewGuid().ToString('N') + '.stdout')
    $StderrPath = Join-Path $OutputRoot ([guid]::NewGuid().ToString('N') + '.stderr')
    $PriorPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        & $FilePath @ArgumentList 1> $StdoutPath 2> $StderrPath
        $ExitCode = $LASTEXITCODE
        $Stdout = if (Test-Path $StdoutPath) { [IO.File]::ReadAllText($StdoutPath) } else { '' }
        $Stderr = if (Test-Path $StderrPath) { [IO.File]::ReadAllText($StderrPath) } else { '' }
        return [pscustomobject]@{ ExitCode=$ExitCode; Stdout=Limit-Output $Stdout; Stderr=Limit-Output $Stderr; StdoutLength=$Stdout.Length; StderrLength=$Stderr.Length }
    }
    finally {
        $ErrorActionPreference = $PriorPreference
        Remove-Item -LiteralPath $StdoutPath,$StderrPath -Force -ErrorAction SilentlyContinue
    }
}

function Get-Summary([string]$Stdout, [string]$Stderr) {
    $Text = $Stdout + "`n" + $Stderr
    $Ran = [regex]::Match($Text, 'Ran ([0-9]+) tests?')
    $Skipped = [regex]::Match($Text, 'OK \(skipped=([0-9]+)\)')
    return [pscustomobject]@{ Ran=if($Ran.Success){$Ran.Groups[1].Value}else{'UNPARSED'}; Skipped=if($Skipped.Success){$Skipped.Groups[1].Value}else{'UNPARSED'}; Success=($Text -match '(?m)^OK(?: \(skipped=[0-9]+\))?\s*$') }
}

function Test-ExecutionEquivalence($DirectMinimal, $WrapperMinimal, $DirectArgv, $WrapperArgv, [string]$ExpectedArgv, $DirectFull, $WrapperFull, $DirectSummary, $WrapperSummary) {
    return ($DirectMinimal.ExitCode -eq 0 -and $WrapperMinimal.ExitCode -eq 0 -and
        $DirectArgv.Stdout.Trim() -eq $ExpectedArgv -and $WrapperArgv.Stdout.Trim() -eq $ExpectedArgv -and
        $DirectFull.ExitCode -eq 0 -and $WrapperFull.ExitCode -eq 0 -and
        $DirectSummary.Success -and $WrapperSummary.Success)
}

$Stage = 'REPOSITORY_CHECK'
if (-not (Test-Path -LiteralPath $Repo -PathType Container)) { Write-DiagnosticFailure 'REPOSITORY_MISSING'; return }
$Git = Get-Command git -CommandType Application -ErrorAction SilentlyContinue
if ($null -eq $Git) { Write-DiagnosticFailure 'GIT_NOT_RESOLVABLE'; return }
$Branch = (& $Git.Source -C $Repo branch --show-current).Trim()
$Head = (& $Git.Source -C $Repo rev-parse HEAD).Trim()
$Origin = (& $Git.Source -C $Repo rev-parse origin/main).Trim()
$Dirty = & $Git.Source -C $Repo status --porcelain
if ($LASTEXITCODE -ne 0 -or $Branch -ne 'main' -or $Head -ne $GovernanceCommit -or $Origin -ne $GovernanceCommit -or -not [string]::IsNullOrWhiteSpace(($Dirty -join "`n"))) { Write-DiagnosticFailure 'REPOSITORY_STATE_INVALID'; return }

$Stage = 'SCRIPT_IDENTITY'
$ExpectedPath = [IO.Path]::GetFullPath((Join-Path $Repo $ScriptPath))
$ActualPath = [IO.Path]::GetFullPath($PSCommandPath)
$ExpectedBlob = (& $Git.Source -C $Repo rev-parse ('{0}:{1}' -f $GovernanceCommit,$ScriptPath)).Trim()
$ActualBlob = (& $Git.Source -C $Repo hash-object ('--path=' + $ScriptPath) -- $ActualPath).Trim()
if ($LASTEXITCODE -ne 0 -or -not $ActualPath.Equals($ExpectedPath,[StringComparison]::OrdinalIgnoreCase) -or $ExpectedBlob -cnotmatch '^[0-9a-f]{40}$' -or $ActualBlob -ne $ExpectedBlob) { Write-DiagnosticFailure 'PROCESS_DIAGNOSTIC_SCRIPT_IDENTITY_MISMATCH'; return }

$Stage = 'PYTHON_RESOLUTION'
$Python = Get-Command py -CommandType Application -ErrorAction SilentlyContinue
if ($null -eq $Python) { Write-DiagnosticFailure 'PYTHON313_LAUNCHER_NOT_RESOLVABLE'; return }
$TempRoot = Join-Path ([IO.Path]::GetTempPath()) ('hioc-python-wrapper-' + [guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($TempRoot) | Out-Null
[Environment]::SetEnvironmentVariable('PYTHONPYCACHEPREFIX', (Join-Path $TempRoot 'pycache'), 'Process')
Set-Location -LiteralPath $Repo

$Stage = 'MINIMAL_COMPARISON'
$MinimalArgs = @('-3.13','-c','import sys;print("HIOC_WRAPPER_MINIMAL");sys.stderr.write("HIOC_WRAPPER_STDERR\n")')
$DirectMinimal = Invoke-DirectPowerShell $Python.Source $MinimalArgs $TempRoot
$WrapperMinimal = Invoke-ProcessStartInfo $Python.Source $MinimalArgs

$Stage = 'ARGV_COMPARISON'
$SyntheticArgs = @('plain','path with spaces','quote"inside','backslash\before"quote','trailing\','')
$ArgvCode = 'import json,sys;print(json.dumps(sys.argv[1:],ensure_ascii=True,separators=(",",":")))'
$ExpectedArgv = ConvertTo-Json -Compress -InputObject $SyntheticArgs
$DirectArgv = Invoke-DirectPowerShell $Python.Source (@('-3.13','-c',$ArgvCode) + $SyntheticArgs) $TempRoot
$WrapperArgv = Invoke-ProcessStartInfo $Python.Source (@('-3.13','-c',$ArgvCode) + $SyntheticArgs)

$Stage = 'FULL_REGRESSION_COMPARISON'
$RegressionArgs = @('-3.13','-m','unittest','discover','-s','tests')
$DirectFull = Invoke-DirectPowerShell $Python.Source $RegressionArgs $TempRoot
$WrapperFull = Invoke-ProcessStartInfo $Python.Source $RegressionArgs
$DirectSummary = Get-Summary $DirectFull.Stdout $DirectFull.Stderr
$WrapperSummary = Get-Summary $WrapperFull.Stdout $WrapperFull.Stderr

$EquivalencePassed = Test-ExecutionEquivalence $DirectMinimal $WrapperMinimal $DirectArgv $WrapperArgv $ExpectedArgv $DirectFull $WrapperFull $DirectSummary $WrapperSummary
Write-Output 'DIAGNOSTIC_EXECUTION=PASS'
Write-Output "EQUIVALENCE_RESULT=$($(if($EquivalencePassed){'PASS'}else{'FAIL'}))"
Write-Output "DIRECT_MINIMAL_EXIT=$($DirectMinimal.ExitCode)"
Write-Output "WRAPPER_MINIMAL_STARTED=$($WrapperMinimal.Started.ToString().ToUpperInvariant())"
Write-Output "WRAPPER_MINIMAL_COMPLETED=$($WrapperMinimal.Completed.ToString().ToUpperInvariant())"
Write-Output "WRAPPER_MINIMAL_EXIT=$($WrapperMinimal.ExitCode)"
Write-Output "WRAPPER_MINIMAL_STDOUT_TASK=$($WrapperMinimal.StdoutTask)"
Write-Output "WRAPPER_MINIMAL_STDERR_TASK=$($WrapperMinimal.StderrTask)"
Write-Output "DIRECT_ARGV_MATCH=$((($DirectArgv.Stdout.Trim() -eq $ExpectedArgv)).ToString().ToUpperInvariant())"
Write-Output "WRAPPER_ARGV_MATCH=$((($WrapperArgv.Stdout.Trim() -eq $ExpectedArgv)).ToString().ToUpperInvariant())"
Write-Output "DIRECT_FULL_EXIT=$($DirectFull.ExitCode)"
Write-Output "DIRECT_FULL_STDOUT_LENGTH=$($DirectFull.StdoutLength)"
Write-Output "DIRECT_FULL_STDERR_LENGTH=$($DirectFull.StderrLength)"
Write-Output "DIRECT_FULL_TESTS=$($DirectSummary.Ran)"
Write-Output "DIRECT_FULL_SKIPS=$($DirectSummary.Skipped)"
Write-Output "DIRECT_FULL_SUMMARY_OK=$($DirectSummary.Success.ToString().ToUpperInvariant())"
Write-Output "WRAPPER_FULL_STARTED=$($WrapperFull.Started.ToString().ToUpperInvariant())"
Write-Output "WRAPPER_FULL_COMPLETED=$($WrapperFull.Completed.ToString().ToUpperInvariant())"
Write-Output "WRAPPER_FULL_EXIT=$($WrapperFull.ExitCode)"
Write-Output "WRAPPER_FULL_STDOUT_LENGTH=$($WrapperFull.StdoutLength)"
Write-Output "WRAPPER_FULL_STDERR_LENGTH=$($WrapperFull.StderrLength)"
Write-Output "WRAPPER_FULL_STDOUT_TASK=$($WrapperFull.StdoutTask)"
Write-Output "WRAPPER_FULL_STDERR_TASK=$($WrapperFull.StderrTask)"
Write-Output "WRAPPER_FULL_TESTS=$($WrapperSummary.Ran)"
Write-Output "WRAPPER_FULL_SKIPS=$($WrapperSummary.Skipped)"
Write-Output "WRAPPER_FULL_SUMMARY_OK=$($WrapperSummary.Success.ToString().ToUpperInvariant())"
Write-Output "EXIT_CODES_MATCH=$((($DirectFull.ExitCode -eq $WrapperFull.ExitCode)).ToString().ToUpperInvariant())"
}
catch { Write-DiagnosticFailure 'PROCESS_DIAGNOSTIC_UNEXPECTED_ERROR' }
finally {
    Set-Location -LiteralPath $PriorLocation -ErrorAction SilentlyContinue
    [Environment]::SetEnvironmentVariable('PYTHONPYCACHEPREFIX', $PriorPycachePrefix, 'Process')
    if ($null -ne $TempRoot -and (Test-Path -LiteralPath $TempRoot)) { Remove-Item -LiteralPath $TempRoot -Recurse -Force -ErrorAction SilentlyContinue }
}
}

Invoke-HIOCProcessDiagnostic
