# Move down a directory into the main folder
$Dir = ".."

Get-ChildItem "$Dir\*.html" -Recurse | ForEach-Object {
    Remove-Item $_.FullName
}