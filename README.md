<div align="center">

# 🎙️ Piper Local TTS Web UI

**[🇷🇺 Русский](#-русский) | [🇬🇧 English](#-english)**

Fast, local, and private neural text-to-speech web interface with CPU & GPU (NVIDIA CUDA) acceleration and public Gradio share support.

</div>

---

<a name="-русский"></a>
## 🇷🇺 Русский

Локальный веб-интерфейс для нейросетевого синтеза речи (Text-to-Speech) на базе движка **Piper** (архитектура **VITS** + **ONNX Runtime**).

Работает полностью автономно на вашем компьютере, без отправки данных на сторонние серверы. Поддерживает инференс как на процессоре (**CPU**), так и с аппаратным ускорением на видеокартах **NVIDIA (CUDA)**.

### ✨ Основные возможности
* **Быстрый старт в 1 клик**: `start.bat` сам создаёт виртуальное окружение `.venv`, ставит зависимости и запускает веб-сервер.
* **Переключение CPU / GPU**: удобный переключатель прямо в интерфейсе с автоматическим fallback на CPU при отсутствии CUDA.
* **Публичная ссылка (Gradio Share)**: возможность мгновенно открыть доступ к веб-интерфейсу с телефона или для друзей по безопасной ссылке `https://xxxx.gradio.live`.
* **Автозагрузка моделей**: выбор любого голоса из списка автоматически скачивает нужные веса с Hugging Face.
* **Тонкая настройка**: ползунки скорости, вариативности интонации (`noise_scale`) и длительности пауз (`noise_w_scale`).

---

### 🚀 Быстрый старт

Просто дважды кликните по файлу:

```text
start.bat
```

Скрипт автоматически:
1. Проверит наличие Python в системе (требуется 3.9+).
2. Создаст изолированное виртуальное окружение (`.venv`).
3. Установит все необходимые библиотеки из `requirements.txt`.
4. Скачает базовую русскую модель голоса (`ru_RU-dmitri-medium`), если она отсутствует.
5. Запустит веб-сервер, создаст **публичную ссылку Gradio** (`https://xxxx.gradio.live`) и откроет страницу в браузере.

---

### 🗂️ Структура проекта

```text
Piper/
├── start.bat          # Скрипт запуска и первоначальной настройки
├── app.py             # Приложение веб-интерфейса на Gradio
├── requirements.txt   # Зависимости Python (piper-tts, onnxruntime-gpu, gradio)
├── README.md          # Документация проекта (RU / EN)
├── .venv/             # Изолированное виртуальное окружение Python
└── voices/            # Папка с моделями голосов (.onnx и .json)
    ├── ru_RU-dmitri-medium.onnx
    ├── ru_RU-dmitri-medium.onnx.json
    └── ...
```

---

### 🗣️ Поддерживаемые голоса

В интерфейсе предустановлены:
* **Русские голоса**:
  * `ru_RU-dmitri-medium` (мужской)
  * `ru_RU-irina-medium` (женский)
  * `ru_RU-ruslan-medium` (мужской)
  * `ru_RU-denis-medium` (мужской)
* **Английский голос**:
  * `en_US-lessac-medium` (женский)

> 💡 **Добавление других языков:** вы можете скачать любые из 170+ голосов на 40+ языках из официального каталога [rhasspy/piper-voices на Hugging Face](https://huggingface.co/rhasspy/piper-voices/tree/main). Достаточно положить два файла (`.onnx` и `.onnx.json`) в папку `voices/`.

---

### 💻 Ручной запуск через консоль

```powershell
# Запуск с созданием публичной ссылки (по умолчанию)
.\.venv\Scripts\python.exe app.py --share

# Запуск только локально (без публичной ссылки)
.\.venv\Scripts\python.exe app.py --no-share
```

---

<br>

<a name="-english"></a>
## 🇬🇧 English

A local web interface for neural text-to-speech (TTS) powered by **Piper** (**VITS** architecture + **ONNX Runtime**).

Runs completely locally on your machine with zero cloud telemetry. Supports both **CPU** execution and hardware acceleration with **NVIDIA GPUs (CUDA)**.

### ✨ Key Features
* **1-Click Quickstart**: `start.bat` automatically creates an isolated `.venv`, installs requirements, and launches the app.
* **CPU / GPU Toggle**: seamless runtime switching between CPU and NVIDIA CUDA right inside the UI.
* **Gradio Public Share Link**: instantly share your running web UI over the internet or access it from mobile via a secure temporary `https://xxxx.gradio.live` link.
* **On-Demand Voice Download**: selecting a new voice automatically fetches the required ONNX models from Hugging Face.
* **Customizable Synthesis**: adjustable sliders for speaking rate, pitch variation (`noise_scale`), and phoneme duration variation (`noise_w_scale`).

---

### 🚀 Quick Start

Simply double-click:

```text
start.bat
```

The script will automatically:
1. Verify Python installation (Python 3.9+ required).
2. Set up an isolated virtual environment (`.venv`).
3. Install dependencies from `requirements.txt`.
4. Download the default Russian voice model (`ru_RU-dmitri-medium`) if missing.
5. Launch the server, generate a **public Gradio URL** (`https://xxxx.gradio.live`), and open the local interface in your browser.

---

### 🗂️ Project Structure

```text
Piper/
├── start.bat          # Launch & auto-setup script for Windows
├── app.py             # Gradio web interface implementation
├── requirements.txt   # Python dependencies (piper-tts, onnxruntime-gpu, gradio)
├── README.md          # Project documentation (RU / EN)
├── .venv/             # Isolated Python virtual environment
└── voices/            # Voice model directory (.onnx and .json)
    ├── ru_RU-dmitri-medium.onnx
    ├── ru_RU-dmitri-medium.onnx.json
    └── ...
```

---

### 🗣️ Supported Voices

Preconfigured in the UI:
* **Russian voices**:
  * `ru_RU-dmitri-medium` (male)
  * `ru_RU-irina-medium` (female)
  * `ru_RU-ruslan-medium` (male)
  * `ru_RU-denis-medium` (male)
* **English voices**:
  * `en_US-lessac-medium` (female)

> 💡 **Adding more voices:** download any of the 170+ voices across 40+ languages from [rhasspy/piper-voices on Hugging Face](https://huggingface.co/rhasspy/piper-voices/tree/main). Simply place both files (`.onnx` and `.onnx.json`) into the `voices/` directory.

---

### 💻 Manual Command Line Launch

```powershell
# Run with a public Gradio tunnel (default)
.\.venv\Scripts\python.exe app.py --share

# Run locally only (no public tunnel)
.\.venv\Scripts\python.exe app.py --no-share
```
