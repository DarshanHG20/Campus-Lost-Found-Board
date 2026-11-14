$ppt = New-Object -ComObject PowerPoint.Application
try {
    $pptx = (Resolve-Path "Campus_Lost_Found_Board_Presentation.pptx").Path
    $pres = $ppt.Presentations.Open($pptx, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    $slideDir = Join-Path (Get-Location) "slides_preview"
    if (-not (Test-Path $slideDir)) {
        New-Item -ItemType Directory -Path $slideDir | Out-Null
    }
    $pres.Export($slideDir, "PNG", 1920, 1080)
    $pres.Close()
} finally {
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
Get-ChildItem $slideDir | Select-Object Name, Length

