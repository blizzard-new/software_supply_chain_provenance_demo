from __future__ import annotations

import math
import shutil
import subprocess
import tempfile
import textwrap
import wave
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "team_handoff" / "screenshots"
OUT_DIR = ROOT / "team_handoff" / "demo_video"
BUILD_DIR = Path(tempfile.gettempdir()) / "ssc_attestation_demo_video_build"
FRAMES_DIR = BUILD_DIR / "frames"
AUDIO_DIR = BUILD_DIR / "audio"
VIDEO_OUT = ROOT / "team_handoff" / "software_supply_chain_attestation_demo.mp4"

WIDTH = 1920
HEIGHT = 1080
FPS = 30

BG = (7, 9, 13)
PANEL = (16, 20, 28)
PANEL_2 = (22, 28, 38)
LINE = (58, 75, 88)
TEXT = (238, 244, 248)
MUTED = (166, 179, 190)
GREEN = (184, 241, 106)
CYAN = (81, 218, 255)
RED = (255, 88, 104)
YELLOW = (255, 211, 99)


@dataclass(frozen=True)
class Scene:
    key: str
    title: str
    label: str
    bullets: tuple[str, ...]
    key_message: str
    narration: str
    images: tuple[str, ...] = ()
    accent: tuple[int, int, int] = GREEN


SCENES = [
    Scene(
        key="01",
        title="Software Supply Chain Attestation Demo",
        label="Project Goal",
        bullets=(
            "Build a real Python package artifact.",
            "Generate a GitHub artifact attestation.",
            "Verify the original artifact successfully.",
            "Reject a tampered artifact after a one-byte change.",
        ),
        key_message="We verify the artifact's origin and integrity, not only its file name.",
        narration=(
            "This video demonstrates our software supply chain attestation project. "
            "We build a real Python package artifact, generate a GitHub artifact attestation, "
            "verify the original artifact, and then show that a tampered artifact is rejected."
        ),
        images=("01_repo_home.png",),
        accent=CYAN,
    ),
    Scene(
        key="02",
        title="Implementation Architecture",
        label="Build -> Attest -> Verify",
        bullets=(
            "Target: hello-provenance-demo, a minimal Python CLI package.",
            "Cloud build: GitHub Actions runs tests and builds the wheel.",
            "Attestation: actions/attest@v4 signs the build provenance.",
            "Verification: GitHub CLI checks the artifact against the signed record.",
        ),
        key_message="The important path is source code -> GitHub Actions -> artifact -> attestation -> verification.",
        narration=(
            "Our implementation starts with a minimal Python command line package called hello provenance demo. "
            "GitHub Actions checks out the source, runs tests, and builds the wheel file. "
            "During the same workflow, actions attest version four generates a signed attestation. "
            "Finally, the GitHub CLI verifies that the artifact matches the signed record."
        ),
        images=("06_workflow_code.png",),
        accent=GREEN,
    ),
    Scene(
        key="03",
        title="GitHub Actions Completed Successfully",
        label="Evidence",
        bullets=(
            "The workflow ran in a public GitHub repository.",
            "Tests passed before the package was built.",
            "The artifact was uploaded for later verification.",
            "The same workflow also verified the attestation and tamper rejection.",
        ),
        key_message="This is not a local-only demo; the formal evidence comes from GitHub Actions.",
        narration=(
            "Here we can see the GitHub Actions run completed successfully. "
            "The workflow first runs tests, then builds the package artifact, and uploads the artifact. "
            "The important point is that the formal evidence comes from the GitHub Actions workflow, "
            "not from a handwritten local note."
        ),
        images=("02_actions_success.png",),
        accent=GREEN,
    ),
    Scene(
        key="04",
        title="Attestation and Verification Steps",
        label="Workflow Core",
        bullets=(
            "Generate artifact attestation with actions/attest@v4.",
            "Verify the original artifact with gh attestation verify.",
            "Run a tamper test to confirm modified artifacts are rejected.",
        ),
        key_message="The workflow does more than build; it also proves and checks provenance.",
        narration=(
            "This part is the core of our workflow. "
            "After the build, actions attest version four creates the artifact attestation. "
            "Then our verification script runs the GitHub CLI to verify the original artifact. "
            "The workflow also runs a tamper test to make sure a modified artifact is rejected."
        ),
        images=("10_workflow_attestation_verify_code.png",),
        accent=CYAN,
    ),
    Scene(
        key="05",
        title="Live Demo: Verification Success",
        label="Original Artifact",
        bullets=(
            "Download the original, untouched wheel artifact.",
            "Run: gh attestation verify.",
            "The SHA-256 digest matches the signed attestation.",
            "Result: verification passes.",
        ),
        key_message="The artifact is accepted because its digest and provenance match the signed record.",
        narration=(
            "Now we verify the original artifact. "
            "The verification command calculates the artifact's SHA two fifty six digest and compares it with the signed attestation. "
            "Because the artifact has not been modified, the digest matches the attestation. "
            "The verification passes, so the artifact is accepted according to our policy."
        ),
        images=("11_verify_pass_terminal.png",),
        accent=GREEN,
    ),
    Scene(
        key="06",
        title="Live Demo: Tamper Failure",
        label="One-Byte Attack",
        bullets=(
            "Simulate an attack by modifying exactly one byte.",
            "The file name may look similar, but the digest changes completely.",
            "The digest no longer matches the attestation.",
            "Result: verification fails and the artifact is rejected.",
        ),
        key_message="A one-byte change breaks the cryptographic match.",
        narration=(
            "Next, we simulate an attack by modifying exactly one byte of the artifact. "
            "Even if the file name still looks similar, the content is no longer the same. "
            "Because of the avalanche effect in SHA two fifty six, the digest changes completely. "
            "When we verify again, the digest does not match the attestation, so verification fails."
        ),
        images=("12_tamper_fail_terminal.png",),
        accent=RED,
    ),
    Scene(
        key="07",
        title="Implementation Code",
        label="Verifier and Tamper Script",
        bullets=(
            "verify_artifact.py runs GitHub attestation verification.",
            "tamper_demo.py flips one byte and verifies that the result fails.",
            "The scripts print artifact path, digest, workflow, commit, and result.",
        ),
        key_message="The demo includes real implementation code, not only screenshots.",
        narration=(
            "These are the two main scripts behind the demo. "
            "The verification script runs GitHub attestation verification and prints the artifact digest, workflow, and commit information. "
            "The tamper script copies the artifact, flips one byte, and confirms that the modified file fails verification."
        ),
        images=("07_verify_artifact_code.png", "08_tamper_demo_code.png"),
        accent=CYAN,
    ),
    Scene(
        key="08",
        title="Limitations and Security Scope",
        label="What Attestation Does Not Solve",
        bullets=(
            "Attestation does not prove the code is bug-free.",
            "It does not replace vulnerability scanning or code review.",
            "If the workflow is compromised, provenance can still reflect that compromised workflow.",
            "Consumers must enforce verification policies before execution or deployment.",
        ),
        key_message="Attestation is one security layer; it must be combined with review, testing, and policy enforcement.",
        narration=(
            "Finally, attestation is not magic. "
            "It does not prove that the code is bug free, and it does not replace vulnerability scanning or code review. "
            "It proves origin and integrity of the build process. "
            "To be useful, consumers must actually verify the attestation and enforce strict policies before using or deploying the artifact."
        ),
        images=(),
        accent=YELLOW,
    ),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


FONT_TITLE = font(64, True)
FONT_SUBTITLE = font(34, False)
FONT_LABEL = font(30, True)
FONT_BODY = font(32, False)
FONT_BODY_BOLD = font(32, True)
FONT_SMALL = font(24, False)
FONT_KEY = font(30, True)
FONT_NUM = font(32, True)


def rounded_rect(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def wrap_text(text: str, draw: ImageDraw.ImageDraw, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        words = paragraph.split()
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if draw.textlength(candidate, font=fnt) <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def draw_text_block(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], fnt, fill, max_width: int, line_gap: int = 10) -> int:
    x, y = xy
    for line in wrap_text(text, draw, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def fit_image(path: Path, box: tuple[int, int, int, int]) -> Image.Image:
    src = Image.open(path).convert("RGB")
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    src.thumbnail((bw, bh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (bw, bh), PANEL_2)
    px = (bw - src.width) // 2
    py = (bh - src.height) // 2
    canvas.paste(src, (px, py))
    return canvas


def draw_scene(scene: Scene, idx: int) -> Path:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    # Subtle diagonal bands.
    for i in range(-HEIGHT, WIDTH, 180):
        draw.line((i, HEIGHT, i + HEIGHT, 0), fill=(11, 15, 22), width=2)

    margin = 96
    draw.text((margin, 64), f"{idx:02d} / {len(SCENES):02d}", font=FONT_NUM, fill=scene.accent)
    draw.text((margin + 150, 62), scene.label.upper(), font=FONT_LABEL, fill=scene.accent)
    title_end = draw_text_block(draw, scene.title, (margin, 128), FONT_TITLE, TEXT, 1050, 8)

    left_x = margin
    left_y = max(300, title_end + 26)
    left_w = 720 if scene.images else 1180
    right_x = left_x + left_w + 48
    right_w = WIDTH - right_x - margin

    rounded_rect(draw, (left_x, left_y, left_x + left_w, 760), 28, PANEL, LINE, 2)
    y = left_y + 42
    for bullet in scene.bullets:
        draw.ellipse((left_x + 36, y + 14, left_x + 52, y + 30), fill=scene.accent)
        y = draw_text_block(draw, bullet, (left_x + 78, y), FONT_BODY, TEXT, left_w - 120, 8) + 20

    rounded_rect(draw, (margin, 810, WIDTH - margin, 964), 24, (12, 18, 24), scene.accent, 2)
    draw.text((margin + 34, 838), "Key message", font=FONT_SMALL, fill=scene.accent)
    draw_text_block(draw, scene.key_message, (margin + 34, 876), FONT_KEY, TEXT, WIDTH - 2 * margin - 68, 8)

    if scene.images:
        visual_top = left_y + 6
        visual_bottom = 780
        if len(scene.images) == 1:
            box = (right_x, visual_top, right_x + right_w, visual_bottom)
            rounded_rect(draw, box, 26, PANEL_2, LINE, 2)
            padded = (box[0] + 20, box[1] + 20, box[2] - 20, box[3] - 20)
            frame = fit_image(SCREENSHOTS / scene.images[0], padded)
            img.paste(frame, (padded[0], padded[1]))
        else:
            split = (visual_top + visual_bottom) // 2
            box1 = (right_x, visual_top, right_x + right_w, split - 12)
            box2 = (right_x, split + 12, right_x + right_w, visual_bottom)
            for box, name in [(box1, scene.images[0]), (box2, scene.images[1])]:
                rounded_rect(draw, box, 24, PANEL_2, LINE, 2)
                padded = (box[0] + 16, box[1] + 16, box[2] - 16, box[3] - 16)
                frame = fit_image(SCREENSHOTS / name, padded)
                img.paste(frame, (padded[0], padded[1]))
    else:
        cx = WIDTH - 430
        cy = 400
        for r, color in [(180, (20, 29, 36)), (132, (28, 42, 52)), (82, scene.accent)]:
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=10)
        draw.text((cx - 120, cy - 40), "VERIFY", font=FONT_BODY_BOLD, fill=TEXT)
        draw.text((cx - 106, cy + 4), "BEFORE", font=FONT_BODY_BOLD, fill=scene.accent)
        draw.text((cx - 92, cy + 48), "TRUST", font=FONT_BODY_BOLD, fill=TEXT)

    draw.line((margin, 1000, WIDTH - margin, 1000), fill=LINE, width=2)
    draw.text((margin, 1018), "Software Supply Chain Attestation Demo | GitHub Actions + Artifact Attestation", font=FONT_SMALL, fill=MUTED)

    out = FRAMES_DIR / f"scene_{scene.key}.png"
    img.save(out, quality=95)
    return out


def write_tts_script() -> Path:
    ps1 = BUILD_DIR / "make_audio.ps1"
    lines = [
        "Add-Type -AssemblyName System.Speech",
        "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer",
        "$synth.SelectVoice('Microsoft Zira Desktop')",
        "$synth.Rate = -1",
        "$synth.Volume = 100",
    ]
    for scene in SCENES:
        wav = (AUDIO_DIR / f"scene_{scene.key}.wav").as_posix()
        text = scene.narration.replace("'", "''")
        lines.extend(
            [
                f"$synth.SetOutputToWaveFile('{wav}')",
                f"$synth.Speak('{text}') | Out-Null",
                "$synth.SetOutputToDefaultAudioDevice()",
            ]
        )
    ps1.write_text("\n".join(lines), encoding="utf-8-sig")
    return ps1


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as handle:
        return handle.getnframes() / float(handle.getframerate())


def make_audio_concat() -> Path:
    concat = BUILD_DIR / "audio.ffconcat"
    with concat.open("w", encoding="utf-8") as handle:
        handle.write("ffconcat version 1.0\n")
        for scene in SCENES:
            path = (AUDIO_DIR / f"scene_{scene.key}.wav").resolve().as_posix()
            handle.write(f"file '{path}'\n")
    return concat


def make_video_concat(scene_frames: list[Path], durations: list[float]) -> Path:
    concat = BUILD_DIR / "video.ffconcat"
    with concat.open("w", encoding="utf-8") as handle:
        handle.write("ffconcat version 1.0\n")
        for frame, duration in zip(scene_frames, durations):
            handle.write(f"file '{frame.resolve().as_posix()}'\n")
            handle.write(f"duration {max(duration, 5.0):.3f}\n")
        handle.write(f"file '{scene_frames[-1].resolve().as_posix()}'\n")
    return concat


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, check=True, cwd=ROOT)


def main() -> None:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    frames = [draw_scene(scene, idx + 1) for idx, scene in enumerate(SCENES)]

    ps1 = write_tts_script()
    run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)])

    audio_concat = make_audio_concat()
    narration = BUILD_DIR / "narration.wav"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(audio_concat), "-c", "copy", str(narration)])

    durations = [wav_duration(AUDIO_DIR / f"scene_{scene.key}.wav") for scene in SCENES]
    video_concat = make_video_concat(frames, durations)
    silent = BUILD_DIR / "silent.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(video_concat),
            "-vf",
            f"fps={FPS}",
            "-pix_fmt",
            "yuv420p",
            str(silent),
        ]
    )

    final_temp = BUILD_DIR / "software_supply_chain_attestation_demo.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(silent),
            "-i",
            str(narration),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-shortest",
            str(final_temp),
        ]
    )

    shutil.copy2(final_temp, VIDEO_OUT)
    total = sum(max(duration, 5.0) for duration in durations)
    print(f"Created: {VIDEO_OUT}")
    print(f"Approx duration: {math.ceil(total)} seconds")


if __name__ == "__main__":
    main()
