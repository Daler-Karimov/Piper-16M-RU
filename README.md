# Piper-RU

[Русский](#русский) | [English](#english)

---

## Русский

Веб-интерфейс (WebUI) для локального нейросетевого синтеза речи (Text-to-Speech) **Piper** на базе архитектуры **VITS** и **ONNX Runtime** с поддержкой инференса на **CPU** и аппаратного ускорения **GPU (NVIDIA CUDA)**.

### Возможности

- **Выбор голосов и автозагрузка:**
  - Готовые русские голоса: **Dmitri** (мужской), **Irina** (женский), **Ruslan** (мужской), **Denis** (мужской).
  - Английский голос: **Lessac** (женский).
  - Автоматическая загрузка моделей (`.onnx` и `.onnx.json`) с Hugging Face при выборе из списка.
  - Поддержка подключения любых сторонних моделей Piper (более 170 голосов на 40+ языках).
- **Аппаратное ускорение (CPU / GPU):**
  - Поддержка инференса на процессоре (**CPU**) и графических ускорителях **NVIDIA (CUDA)** через `onnxruntime-gpu`.
  - Переключение устройства на лету в интерфейсе с автоматическим fallback на CPU при отсутствии CUDA.
- **Тонкая настройка синтеза:**
  - Скорость речи (длина фонем).
  - Вариативность интонации (`noise_scale`).
  - Вариативность длительности звуков и пауз (`noise_w_scale`).
- **Публичный доступ:**
  - Автоматическое создание публичной ссылки Gradio (share link) для удаленного доступа с мобильных устройств или из сети.
- **Быстрый запуск:**
  - Скрипт `start.bat` для запуска в один клик под Windows с автоматическим созданием виртуального окружения `.venv`, установкой зависимостей и скачиванием базовой модели.

### Быстрый старт (Windows)

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Daler-Karimov/Piper-RU.git
cd Piper-RU
```

2. Запустите батник:
```cmd
start.bat
```
При первом запуске скрипт автоматически создаст виртуальное окружение `.venv`, установит все необходимые зависимости из `requirements.txt`, загрузит базовый русский голос (`ru_RU-dmitri-medium`) и откроет веб-интерфейс в браузере.

3. Веб-интерфейс будет доступен по локальному адресу и по публичной ссылке:
```
Локально: http://127.0.0.1:7860
Публично: https://xxxx.gradio.live (ссылка выводится в окне консоли)
```
Для запуска только локально (без публичной ссылки) используйте:
```cmd
start.bat --no-share
```

### Параметры моделей и производительность

- **Архитектура:** VITS (Variational Inference with adversarial learning for end-to-end Text-to-Speech).
- **Формат весов:** ONNX (FP32).
- **Количество параметров:** ~28-30 млн параметров (качество Medium).
- **Размер файла весов:** ~60-65 МБ на одну модель голоса.
- **Потребление памяти:** ~150-300 МБ RAM / VRAM.
- **Скорость генерации:** ~0.05-0.15 сек на аудиофрагмент (RTF < 0.05 на современных GPU NVIDIA).

### Добавление новых голосов

Вы можете вручную скачать любые голоса из официального репозитория [rhasspy/piper-voices на Hugging Face](https://huggingface.co/rhasspy/piper-voices/tree/main).
Для добавления модели поместите два файла в директорию `voices/`:
- `ru_RU-<имя>-medium.onnx`
- `ru_RU-<имя>-medium.onnx.json`

Они автоматически появятся в веб-интерфейсе.

### Структура проекта

```
Piper-RU/
|-- app.py              # Веб-интерфейс Gradio с переключением CPU/GPU и синтезом речи
|-- start.bat           # Скрипт запуска в один клик под Windows
|-- requirements.txt    # Зависимости Python (piper-tts, onnxruntime-gpu, gradio)
|-- README.md           # Документация проекта (Русский / English)
|-- .gitignore          # Исключения Git (.venv, кэш, аудио)
`-- voices/             # Директория с моделями голосов (.onnx и .json)
```

### Лицензия и первоисточники

- Движок Piper TTS: [rhasspy/piper](https://github.com/rhasspy/piper) (MIT License).
- Модели и датасеты голосов: [rhasspy/piper-voices](https://github.com/rhasspy/piper-voices) (Open Data Commons Public Domain Dedication and License / CC-BY / MIT).

---

## English

WebUI for local neural text-to-speech (TTS) synthesis powered by **Piper**, using the **VITS** architecture and **ONNX Runtime** with support for **CPU** inference and **GPU (NVIDIA CUDA)** hardware acceleration.

### Key Features

- **Voice Selection and Auto-download:**
  - Preconfigured Russian voices: **Dmitri** (male), **Irina** (female), **Ruslan** (male), **Denis** (male).
  - English voice: **Lessac** (female).
  - Automatic download of model files (`.onnx` and `.onnx.json`) from Hugging Face upon selection.
  - Support for any custom Piper voice model (over 170 voices in 40+ languages).
- **Hardware Acceleration (CPU / GPU):**
  - Inference support for **CPU** and **NVIDIA CUDA** GPUs via `onnxruntime-gpu`.
  - On-the-fly device toggle in the interface with automatic CPU fallback when CUDA is unavailable.
- **Fine-grained Synthesis Controls:**
  - Speech rate adjustment.
  - Intonation variability (`noise_scale`).
  - Phoneme and pause length variability (`noise_w_scale`).
- **Public Sharing:**
  - Automatic Gradio public share link creation for remote access from mobile devices or external networks.
- **One-Click Launch:**
  - `start.bat` script for Windows with automatic `.venv` virtual environment setup, dependency installation, and default model download.

### Quick Start (Windows)

1. Clone the repository:
```bash
git clone https://github.com/Daler-Karimov/Piper-RU.git
cd Piper-RU
```

2. Run the batch script:
```cmd
start.bat
```
On first launch, the script will automatically create a `.venv` virtual environment, install all dependencies from `requirements.txt`, download the default Russian voice model (`ru_RU-dmitri-medium`), and open the WebUI in your default browser.

3. The WebUI is accessible locally and via public share link:
```
Local URL:  http://127.0.0.1:7860
Public URL: https://xxxx.gradio.live (displayed in the console window)
```
To run locally only (without public share link):
```cmd
start.bat --no-share
```

### Model Specifications and Performance

- **Architecture:** VITS (Variational Inference with adversarial learning for end-to-end Text-to-Speech).
- **Format:** ONNX (FP32).
- **Parameters:** ~28-30 million parameters (Medium quality).
- **Model Size:** ~60-65 MB per voice model.
- **Memory Footprint:** ~150-300 MB RAM / VRAM.
- **Generation Speed:** ~0.05-0.15s per sentence (RTF < 0.05 on modern NVIDIA GPUs).

### Adding Custom Voices

You can manually download additional voices from the official [rhasspy/piper-voices Hugging Face repository](https://huggingface.co/rhasspy/piper-voices/tree/main).
To add a model, place both files into the `voices/` directory:
- `<model-name>.onnx`
- `<model-name>.onnx.json`

They will be automatically recognized and available in the web interface.

### Project Structure

```
Piper-RU/
|-- app.py              # Gradio WebUI with CPU/GPU toggle and speech synthesis
|-- start.bat           # One-click Windows launch script
|-- requirements.txt    # Python dependencies (piper-tts, onnxruntime-gpu, gradio)
|-- README.md           # Project documentation (Russian / English)
|-- .gitignore          # Git ignore rules (.venv, cache, audio files)
`-- voices/             # Directory for voice models (.onnx and .json)
```

### License and Credits

- Piper TTS engine: [rhasspy/piper](https://github.com/rhasspy/piper) (MIT License).
- Voice models and datasets: [rhasspy/piper-voices](https://github.com/rhasspy/piper-voices) (Open Data Commons Public Domain Dedication and License / CC-BY / MIT).
