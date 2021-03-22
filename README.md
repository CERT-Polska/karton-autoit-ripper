# AutoIt-Ripper karton service

Uses [AutoIt-Ripper](https://github.com/nazywam/AutoIt-Ripper) to automatically extract embedded AutoIt scripts and resources from compiled binaries.

**Author**: CERT.pl

**Maintainers**: nazywam

**Consumes:**
```json
{
    "type": "sample",
    "stage": "recognized",
    "kind": "runnable",
    "platform": "win32"
}, {
    "type": "sample",
    "stage": "recognized",
    "kind": "runnable",
    "platform": "win64"
}
```

**Produces:**
```json
{
    "type": "sample",
    "kind": "raw"
}, {
    "type": "sample",
    "kind": "script",
    "stage": "analyzed",
    "extension": "au3",
}
```

## Usage

First of all, make sure you have setup the core system: https://github.com/CERT-Polska/karton

Then install karton-autoit-ripper from PyPi:

```shell
$ pip install karton-autoit-ripper

$ karton-autoit-ripper
```

![Co-financed by the Connecting Europe Facility by of the European Union](https://www.cert.pl/wp-content/uploads/2019/02/en_horizontal_cef_logo-1.png)
