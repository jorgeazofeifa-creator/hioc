param(
    [Parameter(Mandatory=$true)]
    [string]$Repo,

    [Parameter(Mandatory=$true)]
    [string]$ExternalWorkspace,

    [Parameter(Mandatory=$true)]
    [ValidatePattern('^[0-9a-f]{40}$')]
    [string]$GovernanceCommit
)

function Invoke-PE3ManufacturerAction1 {
try {
$ErrorActionPreference = 'Stop'
$Stage = 'INITIALIZATION'
$ImplementationCommit = '157ae644dcedcbec7c69cb0d8b054e104335e024'
$ExpectedDatabaseSha256 = '81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1'
$ExpectedManifestSha256 = '10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4'
$ExpectedDatabaseBytes = 8652642
$ExpectedManifestBytes = 1338
$ExpectedPythonImplementation = 'CPython'
$ExpectedPythonMajorMinor = '3.13'
$PythonSupportPath = 'governance/python-runtime-support.json'
$Git = 'git'
$PythonProbeCode = 'import platform,sys;print(platform.python_implementation(),str(sys.version_info.major)+chr(46)+str(sys.version_info.minor),sep=chr(32))'
$PriorHiocHome = [Environment]::GetEnvironmentVariable('HIOC_HOME', 'Process')
$PriorAutomaticInstall = [Environment]::GetEnvironmentVariable('PYTHON_MANAGER_AUTOMATIC_INSTALL', 'Process')
$PriorLauncherAllowInstall = [Environment]::GetEnvironmentVariable('PYLAUNCHER_ALLOW_INSTALL', 'Process')

if ([string]::IsNullOrWhiteSpace($Repo) -or
    [string]::IsNullOrWhiteSpace($ExternalWorkspace) -or
    $ExpectedDatabaseSha256 -cnotmatch '^[0-9a-f]{64}$' -or
    $ExpectedManifestSha256 -cnotmatch '^[0-9a-f]{64}$' -or
    $ImplementationCommit -cnotmatch '^[0-9a-f]{40}$' -or
    $GovernanceCommit -cnotmatch '^[0-9a-f]{40}$' -or
    $ExpectedPythonMajorMinor -cnotmatch '^3\.[0-9]+$' -or
    -not $PythonProbeCode.Contains('python_implementation') -or
    -not $PythonProbeCode.Contains('sys.version_info')) {
    Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'
    Write-Output 'ERROR_CODE=ACTION1_BLOCK_INTEGRITY_FAILED'
    return
}

$Stage = 'REPOSITORY_CHECK'
if (-not (Test-Path -LiteralPath $Repo -PathType Container)) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=REPOSITORY_MISSING'; return }
if (-not (Test-Path -LiteralPath $ExternalWorkspace -PathType Container)) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=EXTERNAL_WORKSPACE_MISSING'; return }
if ((Get-Item -LiteralPath $ExternalWorkspace).Attributes -band [IO.FileAttributes]::ReparsePoint) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=EXTERNAL_WORKSPACE_REPARSE_POINT'; return }
$Branch = & $Git -C $Repo branch --show-current 2>$null
if ($LASTEXITCODE -ne 0) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=GIT_BRANCH_CHECK_FAILED'; return }
if ($Branch -ne 'main') { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=WRONG_BRANCH'; return }
$Head = & $Git -C $Repo rev-parse HEAD 2>$null
if ($LASTEXITCODE -ne 0) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=GIT_HEAD_CHECK_FAILED'; return }
$Origin = & $Git -C $Repo rev-parse origin/main 2>$null
if ($LASTEXITCODE -ne 0) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=GIT_ORIGIN_CHECK_FAILED'; return }
if ($Head -ne $GovernanceCommit -or $Origin -ne $GovernanceCommit) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=GOVERNANCE_COMMIT_MISMATCH'; return }

$Stage = 'SCRIPT_IDENTITY'
$ExpectedScriptPath = [IO.Path]::GetFullPath((Join-Path $Repo 'tools/hioc-pe3-action1.ps1'))
$ActualScriptPath = [IO.Path]::GetFullPath($PSCommandPath)
if (-not $ActualScriptPath.Equals($ExpectedScriptPath, [StringComparison]::OrdinalIgnoreCase)) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=ACTION1_SCRIPT_IDENTITY_MISMATCH'; return }
$ScriptSpec = '{0}:tools/hioc-pe3-action1.ps1' -f $GovernanceCommit
$ExpectedScriptBlob = & $Git -C $Repo rev-parse $ScriptSpec 2>$null
if ($LASTEXITCODE -ne 0 -or $ExpectedScriptBlob -cnotmatch '^[0-9a-f]{40}$') { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=ACTION1_SCRIPT_IDENTITY_MISMATCH'; return }
$ActualScriptBlob = & $Git -C $Repo hash-object --path=tools/hioc-pe3-action1.ps1 -- $ActualScriptPath 2>$null
if ($LASTEXITCODE -ne 0 -or $ActualScriptBlob -ne $ExpectedScriptBlob) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=ACTION1_SCRIPT_IDENTITY_MISMATCH'; return }
& $Git -C $Repo diff --quiet $GovernanceCommit -- tools/hioc-pe3-action1.ps1
if ($LASTEXITCODE -ne 0) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=ACTION1_SCRIPT_IDENTITY_MISMATCH'; return }

$RepositoryStatus = @(& $Git -C $Repo status --porcelain 2>$null)
if ($LASTEXITCODE -ne 0) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=GIT_STATUS_CHECK_FAILED'; return }
if ($RepositoryStatus.Count -ne 0) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=REPOSITORY_DIRTY'; return }

& $Git -C $Repo merge-base --is-ancestor $ImplementationCommit $GovernanceCommit
if ($LASTEXITCODE -ne 0) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=IMPLEMENTATION_ANCESTRY_FAILED'; return }

$Stage = 'PYTHON_SUPPORT_STATE'
$SupportSpec = '{0}:{1}' -f $GovernanceCommit, $PythonSupportPath
$SupportText = & $Git -C $Repo show $SupportSpec 2>$null
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace(($SupportText -join "`n"))) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=PYTHON_SUPPORT_STATE_INVALID'; return }
try { $PythonSupport = ($SupportText -join "`n") | ConvertFrom-Json } catch { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=PYTHON_SUPPORT_STATE_INVALID'; return }
if ($PythonSupport.schema_version -ne 1 -or
    $PythonSupport.implementation -cne $ExpectedPythonImplementation -or
    $PythonSupport.language_floor -cne '3.10' -or
    $PythonSupport.windows_operator.major_minor -cne $ExpectedPythonMajorMinor -or
    $PythonSupport.production.runtime_source -cne 'distribution_managed') {
    Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'
    Write-Output 'ERROR_CODE=PYTHON_SUPPORT_STATE_INVALID'
    return
}
if ($PythonSupport.windows_operator.status -cne 'supported' -or
    $PythonSupport.windows_operator.validated_patch -cnotmatch '^3\.13\.[0-9]+$') {
    Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'
    Write-Output 'ERROR_CODE=PYTHON_RUNTIME_SUPPORT_PENDING'
    return
}

$Stage = 'PYTHON_RESOLUTION'
$ManagerCommand = Get-Command -Name 'pymanager' -CommandType Application -ErrorAction SilentlyContinue
if ($null -eq $ManagerCommand) { Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=PYTHON_INSTALL_MANAGER_NOT_RESOLVABLE'; return }
$PythonExecutable = ''
$PythonPrefix = @()
[Environment]::SetEnvironmentVariable('PYTHON_MANAGER_AUTOMATIC_INSTALL', 'false', 'Process')
[Environment]::SetEnvironmentVariable('PYLAUNCHER_ALLOW_INSTALL', $null, 'Process')
$PriorResolutionPreference = $ErrorActionPreference
try {
    $ErrorActionPreference = 'Continue'
    $PythonExecutableOutput = @(& $ManagerCommand.Source list --one --format=exe --only-managed $ExpectedPythonMajorMinor 2>$null)
    $PythonManagerExitCode = $LASTEXITCODE
} finally {
    $ErrorActionPreference = $PriorResolutionPreference
}
$PythonExecutable = [string]($PythonExecutableOutput | Select-Object -First 1)
$PythonExecutable = $PythonExecutable.Trim()
if ($PythonManagerExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($PythonExecutable) -or -not [IO.Path]::IsPathRooted($PythonExecutable) -or -not (Test-Path -LiteralPath $PythonExecutable -PathType Leaf)) {
    Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=PYTHON313_MANAGED_RUNTIME_NOT_FOUND'; return
}
$PriorProbePreference = $ErrorActionPreference
try {
    $ErrorActionPreference = 'Continue'
    $Probe = & $PythonExecutable -c $PythonProbeCode 2>$null
    $PythonProbeExitCode = $LASTEXITCODE
} finally {
    $ErrorActionPreference = $PriorProbePreference
}
$ProbeLine = $Probe | Select-Object -First 1
if ($PythonProbeExitCode -ne 0 -or $ProbeLine -cne "$ExpectedPythonImplementation $ExpectedPythonMajorMinor") {
    Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'; Write-Output 'ERROR_CODE=PYTHON_VERSION_UNSUPPORTED'; return
}
$PythonResolverName = 'pymanager list --one --format=exe --only-managed 3.13'

$Stage = 'BUILD_PAIR_DISCOVERY'
$MatchingPairs = @(
    foreach ($CandidateDatabase in Get-ChildItem -LiteralPath $ExternalWorkspace -Filter 'manufacturer-db.json' -File -Recurse) {
        if ($CandidateDatabase.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
        $CandidateManifestPath = Join-Path $CandidateDatabase.DirectoryName 'manufacturer-db.manifest.json'
        if (-not (Test-Path -LiteralPath $CandidateManifestPath -PathType Leaf)) { continue }
        $CandidateManifest = Get-Item -LiteralPath $CandidateManifestPath
        if ($CandidateManifest.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
        if ($CandidateDatabase.Length -ne $ExpectedDatabaseBytes -or $CandidateManifest.Length -ne $ExpectedManifestBytes) { continue }
        $DatabaseHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $CandidateDatabase.FullName).Hash.ToLowerInvariant()
        $ManifestHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $CandidateManifest.FullName).Hash.ToLowerInvariant()
        if ($DatabaseHash -eq $ExpectedDatabaseSha256 -and $ManifestHash -eq $ExpectedManifestSha256) {
            [pscustomobject]@{ Database = $CandidateDatabase.FullName; Manifest = $CandidateManifest.FullName }
        }
    }
)
if ($MatchingPairs.Count -eq 0) {
    Write-Output 'RESULT=INPUT_OR_PRECONDITION_ERROR'
    Write-Output 'ERROR_CODE=VALIDATED_BUILD_PAIR_NOT_FOUND'
    return
}
$SelectedPair = $MatchingPairs | Sort-Object -Property Database | Select-Object -First 1
$Database = $SelectedPair.Database
$Manifest = $SelectedPair.Manifest
$Stage = 'BUILD_PAIR_CONTAINMENT'
$DirectorySeparators = [char[]]@([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
$WorkspacePrefix = [IO.Path]::GetFullPath($ExternalWorkspace).TrimEnd($DirectorySeparators) + [IO.Path]::DirectorySeparatorChar
$SelectedDirectory = [IO.Path]::GetFullPath((Split-Path -Parent $Database))
if (-not $SelectedDirectory.StartsWith($WorkspacePrefix, [StringComparison]::OrdinalIgnoreCase)) { Write-Output 'RESULT=VALIDATION_FAIL'; Write-Output 'ERROR_CODE=SELECTED_PAIR_OUTSIDE_WORKSPACE'; return }
$SelectedBuildDirectory = $SelectedDirectory.Substring($WorkspacePrefix.Length).Replace([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
if ([string]::IsNullOrWhiteSpace($SelectedBuildDirectory)) { $SelectedBuildDirectory = '.' }

$Stage = 'MANUFACTURER_VALIDATION'
$env:HIOC_HOME = $Repo
& $PythonExecutable @PythonPrefix (Join-Path $Repo 'pi4/bin/hioc-validate-manufacturer.py') database --database $Database --manifest $Manifest --json
if ($LASTEXITCODE -ne 0) { Write-Output 'RESULT=VALIDATION_FAIL'; Write-Output 'ERROR_CODE=MANUFACTURER_VALIDATION_FAILED'; return }
$Stage = 'FINAL_REPORT'
[ordered]@{ result='PASS'; repository_head=$Head; implementation_commit=$ImplementationCommit; script_blob=$ActualScriptBlob; python_resolver=$PythonResolverName; python_major_minor=$ExpectedPythonMajorMinor; selected_build_directory=$SelectedBuildDirectory; matching_pair_count=$MatchingPairs.Count; database_sha256=$ExpectedDatabaseSha256; manifest_sha256=$ExpectedManifestSha256; database_bytes=$ExpectedDatabaseBytes; manifest_bytes=$ExpectedManifestBytes } | ConvertTo-Json -Compress
return
}
catch {
    Write-Output 'RESULT=VALIDATION_FAIL'
    Write-Output 'ERROR_CODE=ACTION1_UNEXPECTED_ERROR'
    Write-Output "FAILURE_STAGE=$Stage"
    return
}
finally {
    [Environment]::SetEnvironmentVariable('HIOC_HOME', $PriorHiocHome, 'Process')
    [Environment]::SetEnvironmentVariable('PYTHON_MANAGER_AUTOMATIC_INSTALL', $PriorAutomaticInstall, 'Process')
    [Environment]::SetEnvironmentVariable('PYLAUNCHER_ALLOW_INSTALL', $PriorLauncherAllowInstall, 'Process')
}
}
Invoke-PE3ManufacturerAction1
