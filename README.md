# Face Recognition Attendance System with Geolocation (Backend API)

A backend API for automatic attendance using face recognition and location validation. Built with **Python, Flask, and InsightFace** (Buffalo_L, ArcFace-based). Developed as my capstone project at Universitas Diponegoro, replacing manual attendance with an accurate, measurable solution.

> **Demo / Portfolio:** https://aufatsaqief.github.io/TA-facerecog-Qash/

<!-- Add a screenshot or GIF of the registration/attendance flow here:
![Demo](docs/demo.gif) -->

## Key Features

- **Guided face registration:** captures 5 photos from different angles (front, left, right, up, down).
- **Quality and pose validation:** each registered photo must pass an image-quality threshold (85%) and the correct pose check (can be enabled/disabled).
- **Anti-duplication:** prevents registering a name or face that already exists in the dataset.
- **High-accuracy attendance:** requires a 98% face similarity for attendance to be accepted.
- **Geolocation validation:** attendance is accepted only within a configured radius of the target location.
- **Automatic retraining:** embeddings are recomputed after every successful registration, with no server restart.
- **Modular logging:** attendance is saved to CSV or MySQL by changing a single configuration line.

## Results

<!-- Fill in with your own evaluation results (from evaluate_accuracy.py). Do not add numbers you have not measured. -->

| Metric | Value |
|---|---|
| ROC AUC | _add_ |
| Chosen similarity threshold | 98% |
| Number of test subjects / images | _add_ |

![ROC curve](docs/roc_curve.png)

## Architecture

```
Frontend (browser: photo + geolocation)
   -> POST request -> Flask API (face_api.py)
   -> face_recognize_service.py (face match + location check)
   -> attendance_logger.py (CSV / MySQL)
   -> JSON response -> Frontend shows the result
```

| File | Responsibility |
|---|---|
| `face_api.py` | Main API server that receives HTTP requests |
| `face_register_service.py` | Face registration: pose validation, image quality, duplicate check |
| `face_recognize_service.py` | Attendance logic: compares faces against the dataset and validates location |
| `main.py` | Recomputes embeddings after a new registration |
| `geolocation_service.py` | Target location settings and distance calculation |
| `attendance_logger.py` | Stores successful attendance (CSV by default, MySQL optional) |
| `evaluate_accuracy.py` | Quantitative evaluation of recognition accuracy |

The frontend (Laravel + JavaScript) shows the camera preview, sends the image and data to this API, and displays the response.

## Tech Stack

Python 3.8+, Flask, InsightFace (Buffalo_L / ArcFace), MySQL (optional), Laravel + JavaScript (frontend integration).

## Getting Started

**Prerequisites:** Python 3.8 or newer, Git.

```bash
# 1. Clone
git clone https://github.com/aufatsaqief/TA-facerecog-Qash.git
cd TA-facerecog-Qash

# 2. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1      # Windows (PowerShell)
# source .venv/bin/activate       # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the API server (http://127.0.0.1:5000)
python face_api.py
```

### Configure the attendance location

1. Run `python get_coords.py` to get the approximate latitude/longitude of your location.
2. In `geolocation_service.py`, set `TARGET_LATITUDE`, `TARGET_LONGITUDE`, and `ACCEPTABLE_RADIUS_METERS`.

### Optional: use MySQL instead of CSV

By default, attendance is saved to `absensi.csv`. To use MySQL:

1. Create a database named `qash_demo`.
2. In `attendance_logger.py`, change `LOGGING_MODE = 'CSV'` to `LOGGING_MODE = 'MYSQL'`.
3. Fill in your MySQL username and password in `DB_CONFIG` (never commit real credentials).

## API Reference

Base URL: `http://127.0.0.1:5000`

### `POST /register` (multipart/form-data)

| Field | Type | Description |
|---|---|---|
| `name` | string | Full name of the employee |
| `image` | file | Face image from the camera |
| `frame_index` | integer | Frame order (0 to 4) |
| `total_frames` | integer | Total frames (always 5) |
| `required_pose` | integer | Requested pose index (0 = straight, 1 = left, ...) |

### `POST /recognize` (multipart/form-data)

| Field | Type | Description |
|---|---|---|
| `image` | file | Face image from the camera |
| `latitude` | string | User's current latitude |
| `longitude` | string | User's current longitude |

### Response

Always JSON with `status` and `message`.

<!-- Verify the exact status values against face_api.py before publishing. -->

- `success` / `finished`: operation succeeded.
- `skip`: registration failed (e.g., low image quality); ask the user to retry.
- `error`: fatal error or failed validation (e.g., duplicate face).

<details>
<summary>Example: calling /recognize from JavaScript</summary>

```javascript
const API_URL_RECOGNIZE = 'http://127.0.0.1:5000/recognize';

async function sendToRecognize() {
  const imageBlob = await captureImage(); // get a blob from the canvas
  const formData = new FormData();
  formData.append('image', imageBlob, 'photo.jpg');

  const position = await new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 10000 });
  });
  formData.append('latitude', position.coords.latitude);
  formData.append('longitude', position.coords.longitude);

  const response = await fetch(API_URL_RECOGNIZE, { method: 'POST', body: formData });
  const result = await response.json();
  console.log(result.status, result.message);
}
```

</details>

## Troubleshooting

- **Connection refused:** make sure `face_api.py` is running in a separate terminal.
- **ModuleNotFoundError:** activate the virtual environment (`.venv`) before installing or running.
- **Geolocation error:** the user must grant location permission in the browser.

## Author

Muhammad Aufa Tsaqief — Computer Engineering, Universitas Diponegoro
[LinkedIn](https://linkedin.com/in/muhammad-aufa-tsaqief-61b50b401/) · [GitHub](https://github.com/aufatsaqief)
