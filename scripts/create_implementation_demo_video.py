from __future__ import annotations

import shutil
import subprocess
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "team_handoff" / "screenshots"
OUT = ROOT / "team_handoff" / "software_supply_chain_attestation_implementation_only.mp4"
BUILD = Path(tempfile.gettempdir()) / "ssc_implementation_only_video_build"
FRAMES = BUILD / "frames"

WIDTH = 1920
HEIGHT = 1080
FPS = 30

BG = (6, 8, 12)
WINDOW = (18, 23, 31)
WINDOW_2 = (12, 16, 22)
BAR = (30, 37, 48)
TEXT = (230, 236, 242)
MUTED = (142, 154, 166)
CYAN = (71, 214, 255)
GREEN = (91, 232, 140)
RED = (255, 88, 104)
YELLOW = (255, 213, 102)
PURPLE = (170, 135, 255)
LINE = (64, 80, 96)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf"),
        Path("C:/Windows/Fonts/cascadiacode.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


FONT_MONO = font(26)
FONT_MONO_SMALL = font(22)
FONT_MONO_BOLD = font(26, True)
FONT_TITLE = font(40, True)
FONT_LABEL = font(24, True)
FONT_SMALL = font(20)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        if not raw:
            lines.append("")
            continue
        current = ""
        for word in raw.split(" "):
            candidate = word if not current else f"{current} {word}"
            if draw.textlength(candidate, font=fnt) <= width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def trim_to_width(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, width: int) -> str:
    if draw.textlength(text, font=fnt) <= width:
        return text
    ellipsis = "..."
    while text and draw.textlength(text + ellipsis, font=fnt) > width:
        text = text[:-1]
    return text + ellipsis


def code_lines(path: Path, start: int | None = None, end: int | None = None) -> list[tuple[int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    first = start or 1
    last = end or len(lines)
    return [(i, lines[i - 1]) for i in range(first, min(last, len(lines)) + 1)]


def base(title: str, subtitle: str, accent=CYAN) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    for i in range(-HEIGHT, WIDTH, 160):
        draw.line((i, HEIGHT, i + HEIGHT, 0), fill=(12, 16, 24), width=2)
    draw.text((72, 52), title, font=FONT_TITLE, fill=TEXT)
    draw.text((74, 102), subtitle, font=FONT_LABEL, fill=accent)
    draw.line((72, 138, WIDTH - 72, 138), fill=LINE, width=2)
    return img, draw


def draw_window(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, accent=CYAN) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=18, fill=WINDOW, outline=LINE, width=2)
    draw.rounded_rectangle((x1, y1, x2, y1 + 56), radius=18, fill=BAR)
    draw.rectangle((x1, y1 + 32, x2, y1 + 56), fill=BAR)
    for idx, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse((x1 + 22 + idx * 30, y1 + 20, x1 + 38 + idx * 30, y1 + 36), fill=color)
    draw.text((x1 + 122, y1 + 16), title, font=FONT_SMALL, fill=TEXT)
    draw.line((x1, y1 + 56, x2, y1 + 56), fill=accent, width=2)


def draw_terminal(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, lines: list[str], accent=GREEN) -> None:
    draw_window(draw, box, title, accent)
    x1, y1, x2, y2 = box
    x = x1 + 32
    y = y1 + 82
    max_width = x2 - x1 - 64
    max_y = y2 - 34
    for raw in lines:
        color = TEXT
        if raw.startswith("$") or raw.startswith("PS "):
            color = CYAN
        elif "PASSED" in raw or "Successfully built" in raw or "OK" == raw.strip():
            color = GREEN
        elif "FAILED" in raw or "tampered" in raw.lower():
            color = RED if "FAILED" in raw else YELLOW
        for line in wrap(draw, raw, FONT_MONO, max_width):
            if y > max_y:
                return
            draw.text((x, y), line, font=FONT_MONO, fill=color)
            y += 32
        y += 4


def draw_code(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, lines: list[tuple[int, str]], highlights: set[int]) -> None:
    draw_window(draw, box, title, PURPLE)
    x1, y1, x2, y2 = box
    y = y1 + 78
    for num, text in lines:
        if y > y2 - 36:
            break
        if num in highlights:
            draw.rectangle((x1 + 18, y - 4, x2 - 18, y + 29), fill=(45, 40, 22))
        draw.text((x1 + 26, y), f"{num:>3}", font=FONT_MONO_SMALL, fill=MUTED)
        color = TEXT
        stripped = text.strip()
        if stripped.startswith("def ") or stripped.startswith("class "):
            color = CYAN
        elif "gh" in text or "attestation" in text or "sha256" in text:
            color = GREEN
        elif "tamper" in text or "^=" in text or "FAILED" in text:
            color = RED
        code_width = x2 - (x1 + 108) - 24
        draw.text((x1 + 92, y), trim_to_width(draw, text, FONT_MONO_SMALL, code_width), font=FONT_MONO_SMALL, fill=color)
        y += 30


def fit_image(src_path: Path, box: tuple[int, int, int, int]) -> Image.Image:
    img = Image.open(src_path).convert("RGB")
    x1, y1, x2, y2 = box
    bw = x2 - x1
    bh = y2 - y1
    img.thumbnail((bw, bh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (bw, bh), WINDOW_2)
    canvas.paste(img, ((bw - img.width) // 2, (bh - img.height) // 2))
    return canvas


def draw_image_window(draw: ImageDraw.ImageDraw, canvas: Image.Image, box: tuple[int, int, int, int], title: str, image_name: str, accent=CYAN) -> None:
    draw_window(draw, box, title, accent)
    x1, y1, x2, y2 = box
    target = (x1 + 28, y1 + 82, x2 - 28, y2 - 28)
    fitted = fit_image(SCREENSHOTS / image_name, target)
    canvas.paste(fitted, (target[0], target[1]))


def scene_repo() -> Path:
    img, draw = base("Implementation-Only Demo", "actual files, commands, and verification evidence")
    terminal = [
        "PS > git status --short --branch",
        "## main...origin/main",
        "",
        "PS > repo files used in this demo",
        ".github/workflows/build-and-attest.yml",
        "src/hello_provenance/cli.py",
        "scripts/create_local_manifest.py",
        "scripts/verify_artifact.py",
        "scripts/tamper_demo.py",
        "tests/test_cli.py",
        "team_handoff/screenshots/11_verify_pass_terminal.png",
        "team_handoff/screenshots/12_tamper_fail_terminal.png",
    ]
    draw_terminal(draw, (72, 180, 880, 920), "PowerShell - repository check", terminal)
    draw_code(
        draw,
        (930, 180, 1848, 920),
        "src/hello_provenance/cli.py",
        code_lines(ROOT / "src/hello_provenance/cli.py", 1, 80),
        {12, 13, 14, 15},
    )
    path = FRAMES / "01_repo.png"
    img.save(path)
    return path


def scene_workflow() -> Path:
    img, draw = base("GitHub Actions Workflow", ".github/workflows/build-and-attest.yml")
    draw_code(
        draw,
        (72, 170, 1848, 955),
        ".github/workflows/build-and-attest.yml",
        code_lines(ROOT / ".github/workflows/build-and-attest.yml", 1, 58),
        {8, 9, 10, 28, 31, 34, 40, 44, 51},
    )
    path = FRAMES / "02_workflow.png"
    img.save(path)
    return path


def scene_verify_code() -> Path:
    img, draw = base("Verifier Implementation", "scripts/verify_artifact.py")
    draw_code(
        draw,
        (72, 170, 1848, 955),
        "scripts/verify_artifact.py",
        code_lines(ROOT / "scripts/verify_artifact.py", 31, 95),
        {36, 38, 39, 40, 41, 42, 44, 45, 62, 73, 74, 75, 76},
    )
    path = FRAMES / "03_verify_code.png"
    img.save(path)
    return path


def scene_tamper_code() -> Path:
    img, draw = base("Tamper Test Implementation", "scripts/tamper_demo.py")
    draw_code(
        draw,
        (72, 170, 1848, 955),
        "scripts/tamper_demo.py",
        code_lines(ROOT / "scripts/tamper_demo.py", 10, 90),
        {14, 15, 17, 24, 31, 34, 61, 62, 64, 65, 66, 70, 76},
    )
    path = FRAMES / "04_tamper_code.png"
    img.save(path)
    return path


def scene_local_terminal() -> Path:
    img, draw = base("Local Implementation Run", "real output captured from demo.ps1 -SkipInstall")
    lines = [
        "$ python -m unittest discover -s tests",
        "..",
        "Ran 2 tests in 0.082s",
        "OK",
        "",
        "$ python -m build",
        "Successfully built hello_provenance_demo-0.1.0.tar.gz",
        "Successfully built hello_provenance_demo-0.1.0-py3-none-any.whl",
        "",
        "$ python scripts/create_local_manifest.py",
        "[manifest] artifact = dist/hello_provenance_demo-0.1.0-py3-none-any.whl",
        "[manifest] sha256   = 431a61ffc34f348f9008ce2b76a4df010d4d2236a48569c778c013c99985c461",
        "[manifest] wrote    = .demo/local_provenance.json",
        "",
        "$ python scripts/verify_artifact.py --mode local",
        "[local] expected = 431a61ffc34f348f9008ce2b76a4df010d4d2236a48569c778c013c99985c461",
        "[local] actual   = 431a61ffc34f348f9008ce2b76a4df010d4d2236a48569c778c013c99985c461",
        "[local] verification PASSED: artifact digest matches manifest",
    ]
    draw_terminal(draw, (72, 170, 1848, 955), "PowerShell - local build and verify", lines)
    path = FRAMES / "05_local_terminal.png"
    img.save(path)
    return path


def scene_tamper_terminal() -> Path:
    img, draw = base("Local Tamper Run", "same verifier rejects the modified artifact")
    lines = [
        "$ python scripts/tamper_demo.py --mode local",
        "[tamper] original = dist/hello_provenance_demo-0.1.0-py3-none-any.whl",
        "[tamper] tampered = .demo/tampered/hello_provenance_demo-0.1.0-py3-none-any.tampered.whl",
        "[tamper] original sha256 = 431a61ffc34f348f9008ce2b76a4df010d4d2236a48569c778c013c99985c461",
        "[tamper] tampered sha256 = f9361063c7ff170101c359a2121e16b0f6b2dc974be62b6a2993a7213d5d695f",
        "",
        "[tamper] Step 1: verify original artifact. Expected: PASS",
        "[local] verification PASSED: artifact digest matches manifest",
        "",
        "[tamper] Step 2: verify tampered artifact. Expected: FAIL",
        "[local] verification FAILED: artifact digest does not match manifest",
        "[tamper] expected result: tampered artifact failed verification",
    ]
    draw_terminal(draw, (72, 170, 1848, 955), "PowerShell - one-byte tamper demo", lines, RED)
    path = FRAMES / "06_tamper_terminal.png"
    img.save(path)
    return path


def scene_github_evidence() -> Path:
    img, draw = base("Formal GitHub Evidence", "Actions run created attestation and verified tamper rejection")
    draw_image_window(draw, img, (72, 170, 930, 955), "GitHub Actions - success", "02_actions_success.png", GREEN)
    draw_image_window(draw, img, (990, 170, 1848, 955), "Workflow attest / verify / tamper", "10_workflow_attestation_verify_code.png", CYAN)
    path = FRAMES / "07_github_evidence.png"
    img.save(path)
    return path


def scene_github_terminal() -> Path:
    img, draw = base("Formal Verification Evidence", "captured GitHub attestation verify output")
    draw_image_window(draw, img, (72, 170, 930, 955), "GitHub verify - PASS", "11_verify_pass_terminal.png", GREEN)
    draw_image_window(draw, img, (990, 170, 1848, 955), "GitHub tamper - FAIL", "12_tamper_fail_terminal.png", RED)
    path = FRAMES / "08_github_terminal.png"
    img.save(path)
    return path


@dataclass(frozen=True)
class Clip:
    path: Path
    duration: float


def concat_file(clips: list[Clip]) -> Path:
    path = BUILD / "video.ffconcat"
    with path.open("w", encoding="utf-8") as f:
        f.write("ffconcat version 1.0\n")
        for clip in clips:
            f.write(f"file '{clip.path.resolve().as_posix()}'\n")
            f.write(f"duration {clip.duration:.3f}\n")
        f.write(f"file '{clips[-1].path.resolve().as_posix()}'\n")
    return path


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    if BUILD.exists():
        shutil.rmtree(BUILD)
    FRAMES.mkdir(parents=True, exist_ok=True)
    clips = [
        Clip(scene_repo(), 9),
        Clip(scene_workflow(), 13),
        Clip(scene_verify_code(), 13),
        Clip(scene_tamper_code(), 12),
        Clip(scene_local_terminal(), 14),
        Clip(scene_tamper_terminal(), 13),
        Clip(scene_github_evidence(), 11),
        Clip(scene_github_terminal(), 12),
    ]
    temp_out = BUILD / "implementation_only.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file(clips)),
            "-vf",
            f"fps={FPS}",
            "-pix_fmt",
            "yuv420p",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            str(temp_out),
        ]
    )
    shutil.copy2(temp_out, OUT)
    print(f"Created: {OUT}")


if __name__ == "__main__":
    main()
