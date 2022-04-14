# Lektor 💛 Tailwind CSS

A Lektor plugin that adds Tailwind CSS to your project seamlessly.

[![Build Status](https://github.com/frostming/lektor-tailwind/actions/workflows/testing.yaml/badge.svg)][gha]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lektor-tailwind)][pypi]
[![PyPI](https://img.shields.io/pypi/v/lektor-tailwind)][pypi]

[gha]: https://github.com/frostming/lektor-tailwind/actions/workflows/testing.yaml
[pypi]: https://pypi.org/project/lektor-tailwind

## Get Started

1. Add plugin to your project

   ```bash
   $ lektor plugin add lektor-tailwind
   $ lektor plugin list
   ```

2. Configure your template paths

   In `tailwindcss.config.js`:

   ```javascript
   module.exports = {
     content: ['./templates/**/*.{html,j2}'],
     theme: {
       extend: {},
     },
     plugins: [],
   }
   ```

3. Add the Tailwind directives to your CSS

   In `assets/static/style.css`:

   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

4. Start lektor build or server:

   ```bash
   $ lektor build
   $ lektor server
   ```

You got it. Please refer to [official Tailwind documentation](https://tailwindcss.com/docs/installation) for more information on using Tailwind CSS and its CLI.

## Configuration

By default, the input CSS file in `assets/static/style.css`, while it can be changed by `css_path` plugin config.
