# AutoIt-Ripper karton service

Performs initial classification of sample type. Default karton entrypoint for unrecognized samples.

Author: CERT.pl

Maintainers: nazywam

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
