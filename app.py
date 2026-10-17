import os
import sys
import time
import wave
import urllib.request
from pathlib import Path

# Автоматическое подключение путей к cuDNN и CUDA DLL в Windows
def setup_cuda_dll_paths():
    if sys.platform == "win32":
        candidates = [
            r"C:\Users\daler\AppData\Local\Programs\Python\Python313\Lib\site-packages\torch\lib",
            r"C:\Users\daler\AppData\Local\Programs\Python\Python313\Lib\site-packages\nvidia\cudnn\bin",
            r"C:\Users\daler\AppData\Local\Programs\Python\Python313\Lib\site-packages\nvidia\cublas\bin",
        ]
        base_sp = Path(sys.base_prefix) / "Lib" / "site-packages"
        candidates.extend([
            str(base_sp / "torch" / "lib"),
            str(base_sp / "nvidia" / "cudnn" / "bin"),
            str(base_sp / "nvidia" / "cublas" / "bin"),
        ])
        for path_str in candidates:
            if os.path.isdir(path_str):
                try:
                    os.add_dll_directory(path_str)
                    os.environ["PATH"] = path_str + os.pathsep + os.environ.get("PATH", "")
                except Exception:
                    pass

setup_cuda_dll_paths()

import gradio as gr

# Директория с голосами
VOICES_DIR = Path(__file__).parent / "voices"
VOICES_DIR.mkdir(exist_ok=True)

# Каталог поддерживаемых популярных голосов и их прямые ссылки на Hugging Face
VOICE_CATALOG = {
    "ru_RU-dmitri-medium (Русский - Дмитрий, мужской)": {
        "id": "ru_RU-dmitri-medium",
        "onnx_url": "https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx",
        "json_url": "https://huggingface.co/rhasspy/piper-voices/raw/main/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx.json",
    },
    "ru_RU-irina-medium (Русский - Ирина, женский)": {
        "id": "ru_RU-irina-medium",
        "onnx_url": "https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx",
        "json_url": "https://huggingface.co/rhasspy/piper-voices/raw/main/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx.json",
    },
    "ru_RU-ruslan-medium (Русский - Руслан, мужской)": {
        "id": "ru_RU-ruslan-medium",
        "onnx_url": "https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx",
        "json_url": "https://huggingface.co/rhasspy/piper-voices/raw/main/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx.json",
    },
    "ru_RU-denis-medium (Русский - Денис, мужской)": {
        "id": "ru_RU-denis-medium",
        "onnx_url": "https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/denis/medium/ru_RU-denis-medium.onnx",
        "json_url": "https://huggingface.co/rhasspy/piper-voices/raw/main/ru/ru_RU/denis/medium/ru_RU-denis-medium.onnx.json",
    },
    "en_US-lessac-medium (English - Lessac, female)": {
        "id": "en_US-lessac-medium",
        "onnx_url": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
        "json_url": "https://huggingface.co/rhasspy/piper-voices/raw/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json",
    },
}

# Кэш загруженных моделей: (voice_key, use_cuda) -> voice
LOADED_VOICES = {}

def is_cuda_available():
    try:
        import onnxruntime as ort
        return "CUDAExecutionProvider" in ort.get_available_providers()
    except Exception:
        return False

def download_voice_if_needed(voice_key: str, progress=gr.Progress()):
    info = VOICE_CATALOG[voice_key]
    voice_id = info["id"]
    onnx_path = VOICES_DIR / f"{voice_id}.onnx"
    json_path = VOICES_DIR / f"{voice_id}.onnx.json"

    if not json_path.exists():
        progress(0.1, desc="Скачивание конфига голоса...")
        urllib.request.urlretrieve(info["json_url"], json_path)

    if not onnx_path.exists():
        progress(0.3, desc=f"Скачивание модели {voice_id} (~60 МБ)... Пожалуйста, подождите.")
        urllib.request.urlretrieve(info["onnx_url"], onnx_path)

    return onnx_path, json_path

def get_piper_voice(voice_key: str, use_cuda: bool = False, progress=gr.Progress()):
    cache_key = (voice_key, use_cuda)
    if cache_key in LOADED_VOICES:
        return LOADED_VOICES[cache_key], ("GPU (CUDA)" if use_cuda else "CPU")

    from piper import PiperVoice

    onnx_path, json_path = download_voice_if_needed(voice_key, progress=progress)
    device_label = "GPU (CUDA)" if use_cuda else "CPU"
    progress(0.9, desc=f"Загрузка модели в память ({device_label})...")

    actual_device = "CPU"
    if use_cuda:
        try:
            voice = PiperVoice.load(str(onnx_path), config_path=str(json_path), use_cuda=True)
            actual_device = "GPU (CUDA)"
        except Exception as e:
            # Fallback на CPU при возникновении ошибки драйвера/CUDA
            voice = PiperVoice.load(str(onnx_path), config_path=str(json_path), use_cuda=False)
            actual_device = f"CPU (GPU fallback: {e})"
    else:
        voice = PiperVoice.load(str(onnx_path), config_path=str(json_path), use_cuda=False)
        actual_device = "CPU"

    LOADED_VOICES[cache_key] = voice
    return voice, actual_device

def synthesize_text(
    text: str,
    voice_key: str,
    device_choice: str,
    speed: float,
    noise_scale: float,
    noise_w_scale: float,
    progress=gr.Progress()
):
    if not text.strip():
        raise gr.Error("Пожалуйста, введите текст для синтеза.")

    use_cuda = (device_choice == "GPU (CUDA)")
    t0 = time.time()
    voice, actual_device = get_piper_voice(voice_key, use_cuda=use_cuda, progress=progress)

    # Piper SynthesisConfig
    from piper.config import SynthesisConfig

    length_scale = 1.0 / max(0.2, speed)

    syn_config = SynthesisConfig(
        length_scale=length_scale,
        noise_scale=noise_scale,
        noise_w_scale=noise_w_scale,
    )

    output_path = VOICES_DIR / "output.wav"
    with wave.open(str(output_path), "wb") as wav_file:
        voice.synthesize_wav(text, wav_file, syn_config=syn_config)

    elapsed = time.time() - t0
    status = f"Готово за **{elapsed:.2f} сек.** | Устройство: **{actual_device}** | Модель: `{VOICE_CATALOG[voice_key]['id']}`"
    return str(output_path), status

cuda_ready = is_cuda_available()
initial_device = "GPU (CUDA)" if cuda_ready else "CPU"

# Создание интерфейса Gradio
with gr.Blocks(title="Piper TTS Local Web UI") as demo:
    gr.Markdown(
        """
        # Piper Local Text-to-Speech (VITS + ONNX)
        Быстрый локальный синтез речи с поддержкой вычислений на **CPU** и **GPU (CUDA)**.
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            text_input = gr.Textbox(
                label="Текст для озвучивания",
                placeholder="Введите текст здесь...",
                value="Привет! Это проверка работы локального синтеза речи Piper через веб-интерфейс.",
                lines=4,
            )

            with gr.Row():
                voice_dropdown = gr.Dropdown(
                    label="Голос",
                    choices=list(VOICE_CATALOG.keys()),
                    value=list(VOICE_CATALOG.keys())[0],
                    scale=3,
                )
                device_radio = gr.Radio(
                    label="Устройство вычислений",
                    choices=["CPU", "GPU (CUDA)"],
                    value=initial_device,
                    scale=2,
                    info="CUDA доступна (NVIDIA RTX)" if cuda_ready else "CUDA не обнаружена",
                )

            with gr.Accordion("Дополнительные настройки", open=False):
                speed_slider = gr.Slider(
                    label="Скорость речи",
                    minimum=0.5,
                    maximum=2.0,
                    value=1.0,
                    step=0.05,
                )
                noise_slider = gr.Slider(
                    label="Вариативность интонации (noise_scale)",
                    minimum=0.1,
                    maximum=1.2,
                    value=0.667,
                    step=0.05,
                )
                noise_w_slider = gr.Slider(
                    label="Вариативность длительности фонем (noise_w_scale)",
                    minimum=0.1,
                    maximum=1.2,
                    value=0.8,
                    step=0.05,
                )

            btn_submit = gr.Button("Озвучить", variant="primary", size="lg")

            gr.Examples(
                examples=[
                    ["Привет! Это проверка работы локального синтеза речи Piper через веб-интерфейс."],
                    ["В недрах тундры выдры в гетрах тырят в вёдра ядра кедров."],
                    ["Модель VITS работает с ускорением на видеокарте RTX 5080."],
                ],
                inputs=[text_input],
            )

        with gr.Column(scale=2):
            audio_output = gr.Audio(label="Результат", type="filepath", autoplay=True)
            status_text = gr.Markdown("Готов к работе.")

    btn_submit.click(
        fn=synthesize_text,
        inputs=[
            text_input,
            voice_dropdown,
            device_radio,
            speed_slider,
            noise_slider,
            noise_w_slider,
        ],
        outputs=[audio_output, status_text],
    )

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Piper TTS Gradio Web UI")
    parser.add_argument("--share", action="store_true", default=True, help="Создать публичную ссылку Gradio (.gradio.live)")
    parser.add_argument("--no-share", action="store_false", dest="share", help="Отключить публичную ссылку (только локально)")
    parser.add_argument("--port", type=int, default=None, help="Порт сервера (по умолчанию динамический)")
    args = parser.parse_args()

    demo.launch(
        server_name="0.0.0.0" if args.share else "127.0.0.1",
        server_port=args.port,
        share=args.share,
        inbrowser=True,
        theme=gr.themes.Soft(),
    )
