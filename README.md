# Avtech-Firmware-Tools
Tools to sign Avtech DVR firmware

## Usage examples

### Sign
`./avfwtools.py sign -i AppImg.img -o AppImg_mod.bin -p H264DVRAV76T -d img -v 1018`

### Unsign
`./avfwtools.py unsign -i AppImg.bin -o AppImg.img`

### Info
`./avfwtools.py info -i AppImg.bin`
