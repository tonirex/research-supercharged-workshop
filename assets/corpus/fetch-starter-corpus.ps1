<#
  Fetch the open-access starter corpus for Lab 2 (RAG) into this folder (Windows / PowerShell).
  Files are downloaded LOCALLY (git-ignored) — we do NOT commit them: the arXiv papers are under
  arXiv's non-exclusive license (not free to redistribute); the NIST doc is US-Gov public domain.

  Usage:  pwsh assets/corpus/fetch-starter-corpus.ps1   (or run in Windows PowerShell)
#>
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$files = [ordered]@{
  "attention-is-all-you-need.pdf"     = "https://arxiv.org/pdf/1706.03762"
  "bert.pdf"                          = "https://arxiv.org/pdf/1810.04805"
  "resnet-deep-residual-learning.pdf" = "https://arxiv.org/pdf/1512.03385"
  "gpt3-few-shot-learners.pdf"        = "https://arxiv.org/pdf/2005.14165"
  "nist-csf-2.0.pdf"                  = "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf"
}

Write-Host "Fetching starter corpus into $PSScriptRoot ..."
foreach ($name in $files.Keys) {
  if ((Test-Path $name) -and (Get-Item $name).Length -gt 0) {
    Write-Host "  skip  $name (already present)"
    continue
  }
  try {
    curl.exe -fsSL --max-time 120 -o $name $files[$name]
    Write-Host ("  ok    {0} ({1} bytes)" -f $name, (Get-Item $name).Length)
  } catch {
    Write-Warning ("  FAIL  {0} - download it manually from {1}" -f $name, $files[$name])
    Remove-Item $name -ErrorAction SilentlyContinue
  }
}
Write-Host "Done. (These PDFs are git-ignored and stay local.)"
