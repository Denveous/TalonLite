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

if ($env:MEIPASS) {
    $scriptPath = Join-Path -Path $env:MEIPASS -ChildPath "Win11Debloat\Win11Debloat.ps1"
} else {
    $scriptPath = Join-Path -Path (Get-Location) -ChildPath "Win11Debloat\Win11Debloat.ps1"
}

if (-Not (Test-Path $scriptPath)) {
    Write-Host "Error: Win11Debloat.ps1 not found." -ForegroundColor Red
    Exit
} else {
    Write-Host "Found Win11Debloat.ps1 at: $scriptPath"
}

Write-Output "> Running Win11Debloat..."

$arguments = $($PSBoundParameters.GetEnumerator() | ForEach-Object {
    if ($_.Value -eq $true) {
        "-$($_.Key)"
    } 
    else {
         "-$($_.Key) ""$($_.Value)"
    }
})

$debloatProcess = Start-Process powershell.exe -PassThru -ArgumentList "-executionpolicy bypass -File `"$scriptPath`" $arguments" -Verb RunAs

if ($null -ne $debloatProcess) {
    $debloatProcess.WaitForExit()
}

Write-Output "-------------------------------------------------------------------------------------------"
Write-Output " Raphi's Win11Debloat process completed."
