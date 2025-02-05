ASCII printable format (page 15)

In the 2-byte printable, an "Exception code" is the escape character 5Dh ']'.

Frame
1. 5+ NULs for serial timing
1. SOH - starts the packet ']!'
1. Type code + address
1. Packet (can be nested)
    1. STX - starts the commands, data, and checksums (']"')
    1. command
    1. data field
    1. ETX ']#'
    1. optional checksum defined as the 16-bit hex sum of the packet from STX through ETX, inclusive
1. EOT - closes the frame (`]$')



