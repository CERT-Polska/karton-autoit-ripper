from pathlib import Path

from autoit_ripper import AutoItVersion, extract  # type: ignore
from karton.core import Karton, Resource, Task
from malduck.yara import Yara  # type: ignore

from .__version__ import __version__
from .extract_drop import extract_binary


class AutoItRipperKarton(Karton):
    """
    Extracts embedded AutoIt scripts from binaries and additionaly
    tries to extract some binary drops from scripts
    """

    identity = "karton.autoit-ripper"
    version = __version__
    persistent = True
    filters = [
        {
            "type": "sample",
            "stage": "recognized",
            "kind": "runnable",
            "platform": "win32",
        },
        {
            "type": "sample",
            "stage": "recognized",
            "kind": "runnable",
            "platform": "win64",
        },
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        yara_path = Path(__file__).parent / "autoit.yar"
        self.yara = Yara(rule_paths={"autoit": yara_path.as_posix()})

    def process(self, task: Task) -> None:  # type: ignore
        sample = task.get_resource("sample")
        resources = None

        m = self.yara.match(data=sample.content)
        if "autoit_v3_00" in m:
            self.log.info("Found a possible autoit v3.00 binary")
            resources = extract(data=sample.content, version=AutoItVersion.EA05)
        elif "autoit_v3_26" in m:
            self.log.info("Found a possible autoit v3.26+ binary")
            resources = extract(data=sample.content, version=AutoItVersion.EA06)

        if resources:
            self.log.info("Found embedded data, reporting!")

            for res_name, res_data in resources:
                if res_name.endswith(".dll") or res_name.endswith(".exe"):
                    task_params = {
                        "type": "sample",
                        "kind": "raw",
                    }
                elif res_name == "script.au3":
                    task_params = {
                        "type": "sample",
                        "kind": "script",
                        "stage": "analyzed",
                        "extension": "au3",
                    }
                else:
                    continue

                self.log.info("Sending a task with %s", res_name)
                script = Resource(res_name, res_data)
                self.send_task(
                    Task(
                        task_params,
                        payload={
                            "sample": script,
                            "parent": sample,
                            "tags": ["script:win32:au3"],
                        },
                    )
                )
                if res_name == "script.au3":
                    self.log.info("Looking for a binary embedded in the script")
                    drop = extract_binary(res_data.decode())
                    if drop:
                        self.log.info("Found an embedded binary")
                        self.send_task(
                            Task(
                                {"type": "sample", "kind": "raw"},
                                payload={
                                    "sample": Resource(
                                        name="autoit_drop.exe", content=drop
                                    ),
                                    "parent": script,
                                },
                            )
                        )
