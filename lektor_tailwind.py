from __future__ import annotations

import os
import subprocess

from lektor.pluginsystem import Plugin
from pytailwindcss import get_bin_path, install

__version__ = "0.2.0"

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
        self.tailwind: subprocess.Popen | None = None

    def on_setup_env(self, **extra):
        self.init_tailwindcss()

    def init_tailwindcss(self):
        if not os.path.exists(self.tailwind_bin):
            install(bin_path=self.tailwind_bin)

    def _get_tailwind_args(self, output_path, *extra_args):
        return [self.tailwind_bin,
                "-i",
                self.input_css,
                "-o",
                os.path.join(output_path, self.css_path),
                *extra_args]

    def input_exists(self) -> bool:
        return os.path.exists(self.input_css)

    def should_minify(self) -> bool:
        return not self.watch or os.environ.get("NODE_ENV") == "production"

    def compile_css(self, output_path: str):
        minify = ["--minify"] if self.should_minify() else []
        subprocess.run(
            self._get_tailwind_args(output_path, *minify),
            check=True,
            cwd=output_path,
        )

    def on_server_spawn(self, **extra):
        self.watch = True

    def on_after_build_all(self, builder, **extra):
        if not self.input_exists():
            return
        self.compile_css(builder.destination_path)
