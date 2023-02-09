from __future__ import annotations

import os
import subprocess
import threading

from lektor.pluginsystem import Plugin
from pytailwindcss import install, get_bin_path

__version__ = "0.1.2"
GRACEFUL_TIMEOUT = 5


class TailwindPlugin(Plugin):
    name = "lektor-tailwind"
    description = "Beautify your Lektor project with Tailwind CSS"

    def __init__(self, env, id):
        super().__init__(env, id)
        config = self.get_config()
        self.tailwind_bin = str(get_bin_path())
        self.watch = False
        self.css_path = config.get("css_path", "static/style.css")
        self.input_css = os.path.join(self.env.root_path, "assets", self.css_path)
        self.tailwind: threading.Thread | None = None

    def on_setup_env(self, **extra):
        self.init_tailwindcss()

    def init_tailwindcss(self):
        if not os.path.exists(self.tailwind_bin):
            install(bin_path=self.tailwind_bin)
        filename = "tailwind.config.js"
        if not os.path.exists(os.path.join(self.env.root_path, filename)):
            subprocess.run(
                [self.tailwind_bin, "init"], check=True, cwd=self.env.root_path
            )

    def _run_watcher(self, output_path: str):
        if not self.input_exists():
            return
        self.tailwind = subprocess.Popen(
            [
                self.tailwind_bin,
                "-i",
                self.input_css,
                "-o",
                os.path.join(output_path, self.css_path),
                "-w",
            ],
            cwd=self.env.root_path,
        )

    def input_exists(self) -> bool:
        return os.path.exists(self.input_css)

    def compile_css(self, output_path: str):
        subprocess.run(
            [
                self.tailwind_bin,
                "-i",
                self.input_css,
                "-o",
                os.path.join(output_path, self.css_path),
                "--minify",
            ],
            check=True,
        )

    def on_server_spawn(self, **extra):
        self.watch = True

    def on_server_stop(self, **extra):
        self.watch = False
        if self.tailwind is not None:
            self.tailwind.terminate()
            try:
                self.tailwind.communicate(GRACEFUL_TIMEOUT)
            except subprocess.TimeoutExpired:
                self.tailwind.kill()
            self.tailwind = None

    def on_before_build_all(self, builder, **extra):
        if not self.input_exists() or self.tailwind is not None or not self.watch:
            return
        self._run_watcher(builder.destination_path)

    def on_before_build(self, builder, source, prog, **extra):
        if source.source_filename != self.input_css:
            return

        # The input stylesheet is being built.  We don't want to let
        # Lektor "build" it (i.e. copy it to the output directory),
        # since that will potentially overwrite any Tailwind-compiled
        # output that is already there.

        # Here we monkey-patch Lektor's build program to disable it
        prog.build_artifact = lambda artifact: None

        # Instead, we run tailwind to compile the self.input_css to
        # the output directory.  (We skip this if we're already
        # running tailwind in --watch mode, since, in that case, it
        # will rebuild the CSS on it's own.)
        if self.tailwind is None:
            self.compile_css(builder.destination_path)
