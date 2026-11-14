param(
    [string]$pptxPath,
    [string]$pdfPath
)

$pptxFull = (Resolve-Path $pptxPath).Path
$pdfFull = [System.IO.Path]::GetFullPath($pdfPath)

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
try {
    $pres = $ppt.Presentations.Open($pptxFull, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    $pres.SaveAs($pdfFull, 32)
    $pres.Close()
} finally {
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
Write-Output "SUCCESS"

