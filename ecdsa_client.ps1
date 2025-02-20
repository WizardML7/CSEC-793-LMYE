# Create a new TCP client to connect to the ECDSA signing server
$client = New-Object System.Net.Sockets.TcpClient('localhost', 65432)
$stream = $client.GetStream()
$writer = New-Object System.IO.StreamWriter($stream)
$writer.AutoFlush = $true

# Send a message to be signed
$message = "Hello, World!"
$writer.WriteLine($message)
Write-Host "Sent message: $message"

# Read the response (signature) - modify to read until the end of the signature block
$reader = New-Object System.IO.StreamReader($stream)

# Initialize an empty string to hold the signature
$signature = ""
$insideSignatureBlock = $false

# Read the signature line by line until the end of the PGP signature block
while ($true) {
    $line = $reader.ReadLine()
    if ($null -eq $line) { break }  # Exit the loop if there's no more data

    # Check for the beginning and end of the signature block
    if ($line -eq "-----BEGIN PGP SIGNATURE-----") {
        $insideSignatureBlock = $true  # Start capturing the signature
        continue  # Skip the begin line
    }
    if ($line -eq "-----END PGP SIGNATURE-----") {
        break  # Stop capturing at the end line
    }

    # Capture the base64-encoded signature data
    if ($insideSignatureBlock) {
        $signature += "$line`r`n"  # Append the line and add a newline character
    }
}

# Output the received signature and additional information
if ($signature) {
    # Trim whitespace and newlines from the signature
    $trimmedSignature = $signature.Trim()

    Write-Host "Received signature: $trimmedSignature"
    Write-Host "Signature Length: $($trimmedSignature.Length) characters"

    # Convert the trimmed signature to bytes for further use if needed
    [byte[]]$signatureBytes = [System.Text.Encoding]::UTF8.GetBytes($trimmedSignature)
    Write-Host "Signature (bytes): $signatureBytes"
} else {
    Write-Host "No signature received from the server."
}

# Clean up resources
$writer.Close()
$reader.Close()
$client.Close()
