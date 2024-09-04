function Add-Font {
    param (
        [string]$Path
    )
    $RegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    $FontName = [System.IO.Path]::GetFileNameWithoutExtension($Path)
    $FontRegKey = Get-ItemProperty -Path $RegPath -Name $FontName -ErrorAction SilentlyContinue
    if (-not $FontRegKey) {
        New-ItemProperty -Path $RegPath -Name $FontName -Value $Path -PropertyType String
        $Shell = New-Object -ComObject Shell.Application
        $Folder = $Shell.Namespace((Get-Item $Path).DirectoryName)
        $Folder.ParseName((Get-Item $Path).Name).InvokeVerb("Install")
    }
}

$FontPath = "$PSScriptRoot\ipaexg.ttf"
Add-Font -Path $FontPath
