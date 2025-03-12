param (
    [switch]$Silent,
    [switch]$Verbose,
    [switch]$Sysprep,
    [string]$User,
    [switch]$RunAppConfigurator,
    [switch]$RunDefaults, 
    [switch]$RunWin11Defaults,
    [switch]$RunSavedSettings,
    [switch]$RemoveApps, 
    [switch]$RemoveAppsCustom,
    [switch]$RemoveGamingApps,
    [switch]$RemoveCommApps,
    [switch]$RemoveDevApps,
    [switch]$RemoveW11Outlook,
    [switch]$ForceRemoveEdge,
    [switch]$DisableDVR,
    [switch]$DisableTelemetry,
    [switch]$DisableBingSearches, 
    [switch]$DisableBing,
    [switch]$DisableDesktopSpotlight,
    [switch]$DisableLockscrTips, 
    [switch]$DisableLockscreenTips,
    [switch]$DisableWindowsSuggestions, 
    [switch]$DisableSuggestions,
    [switch]$ShowHiddenFolders,
    [switch]$ShowKnownFileExt,
    [switch]$HideDupliDrive,
    [switch]$TaskbarAlignLeft,
    [switch]$HideSearchTb, 
    [switch]$ShowSearchIconTb, 
    [switch]$ShowSearchLabelTb, 
    [switch]$ShowSearchBoxTb,
    [switch]$HideTaskview,
    [switch]$DisableStartRecommended,
    [switch]$DisableCopilot,
    [switch]$DisableRecall,
    [switch]$DisableWidgets, 
    [switch]$HideWidgets,
    [switch]$DisableChat, 
    [switch]$HideChat,
    [switch]$ClearStart,
    [switch]$ClearStartAllUsers,
    [switch]$RevertContextMenu,
    [switch]$DisableMouseAcceleration,
    [switch]$HideHome,
    [switch]$HideGallery,
    [switch]$ExplorerToHome,
    [switch]$ExplorerToThisPC,
    [switch]$ExplorerToDownloads,
    [switch]$ExplorerToOneDrive,
    [switch]$DisableOnedrive, 
    [switch]$HideOnedrive,
    [switch]$Disable3dObjects, 
    [switch]$Hide3dObjects,
    [switch]$DisableMusic, 
    [switch]$HideMusic,
    [switch]$DisableIncludeInLibrary, 
    [switch]$HideIncludeInLibrary,
    [switch]$DisableGiveAccessTo, 
    [switch]$HideGiveAccessTo,
    [switch]$DisableShare, 
    [switch]$HideShare
)

# Show error if current PowerShell environment does not have LanguageMode set to FullLanguage 
if ($ExecutionContext.SessionState.LanguageMode -ne "FullLanguage") {
   Write-Host "Error: Win11Debloat is unable to run on your system. PowerShell execution is restricted by security policies" -ForegroundColor Red
   Write-Output ""
   Write-Output "Press enter to exit..."
   Read-Host | Out-Null
   Exit
}

Clear-Host
Write-Output "-------------------------------------------------------------------------------------------"
Write-Output " Win11Debloat Script - Get"
Write-Output "-------------------------------------------------------------------------------------------"

# Get the temporary directory
$tempDir = [System.IO.Path]::GetTempPath()

# Search for the Win11Debloat-master.zip file in the temporary directory
$debloatZipPath = Get-ChildItem -Path $tempDir -Recurse -Filter "Win11Debloat-master.zip" -ErrorAction SilentlyContinue

# Check if the ZIP file was found
if ($debloatZipPath -eq $null) {
    Write-Host "Error: Win11Debloat-master.zip not found in the temporary directory." -ForegroundColor Red
    Exit
} else {
    Write-Host "Found Win11Debloat-master.zip at: $($debloatZipPath.FullName)"
}

# Unzip archive to Win11Debloat folder in TEMP
$win11DebloatTempPath = "$env:TEMP\Win11Debloat"
Expand-Archive $debloatZipPath.FullName $win11DebloatTempPath -Force

Write-Output "> Running Win11Debloat..."

# Make list of arguments to pass on to the script
$arguments = $($PSBoundParameters.GetEnumerator() | ForEach-Object {
    if ($_.Value -eq $true) {
        "-$($_.Key)"
    } 
    else {
         "-$($_.Key) ""$($_.Value)
    }
})

# Run Win11Debloat script with the provided arguments
$debloatScriptPath = Join-Path -Path $win11DebloatTempPath -ChildPath "Win11Debloat-master\Win11Debloat.ps1"
$debloatProcess = Start-Process powershell.exe -PassThru -ArgumentList "-executionpolicy bypass -File `"$debloatScriptPath`" $arguments" -Verb RunAs

# Wait for the process to finish before continuing
if ($null -ne $debloatProcess) {
    $debloatProcess.WaitForExit()
}

# Remove all remaining script files, except for CustomAppsList and SavedSettings files
if (Test-Path $win11DebloatTempPath) {
    Write-Output ""
    Write-Output "> Cleaning up..."

    # Cleanup, remove Win11Debloat directory
    Get-ChildItem -Path $win11DebloatTempPath -Exclude CustomAppsList,SavedSettings | Remove-Item -Recurse -Force
}

Write-Output "-------------------------------------------------------------------------------------------"
Write-Output " Win11Debloat process completed."
Write-Output "-------------------------------------------------------------------------------------------"
