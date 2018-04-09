# Avtech-Firmware-Tools
Tools to sign Avtech DVR firmware

---

## Usage examples

### Sign
`./avfwtools.py sign -i AppImg.img -o AppImg_mod.bin -p H264DVRAV76T -d img -v 1018`

### Unsign
`./avfwtools.py unsign -i AppImg.bin -o AppImg.img`

### Info
`./avfwtools.py info -i AppImg.bin`

---

## Header structure
The header is 200 byte long

| Size (byte)  | Type | Name | Comment |
| :----------: | ---- | ---- | ------- |
| 4  | Unsigned Int  | Magic | Header length used as magic number |
| 64 | Char array | Product | Product name (e.g. H264DVRAV76T) |
| 64 | Char array | Description | File description (e.g. img) |
| 64 | Char array | Version | File version (e.g. 1018) |
| 4  | Unsigned Int  | Checksum | Checksum of body |

---

## Checksum
The checksum is the sum of the content of all bytes in the file as integer

## Firmware download
https://sites.google.com/site/firmwarerelease/firmware-list/dvr-2/h264-dvr
