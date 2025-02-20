# COCO Annotation Converter

## Description

**COCO Annotation Converter** is a Python script designed to convert annotations from the `pred_coco.json` format to the COCO Results Format. This tool is useful for those working with COCO datasets who need to transform predictions into a compatible format for analysis and evaluation.

## Features

- **Support for Various Annotation Structures:** Handles annotations as dictionaries containing the `annotations` key as well as lists of annotations.
- **Confidence Score Filtering:** Allows setting a minimum score threshold to include only relevant detections.
- **Category Management:** Maps category names to their respective IDs based on ground truth annotations.
- **Support for Segmentations and Keypoints:** Includes segmentation and keypoint information if present in the annotations.

## Requirements

- Python 3.6 or higher

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/gguzzy/coco-annotation-converter.git
    cd coco-annotation-converter
    ```

2. **Create a Virtual Environment (Optional but Recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *If the `requirements.txt` file is not present, you can install dependencies manually:*

    ```bash
    pip install argparse
    ```

## Usage

Run the `converter.py` script via the command line, specifying the paths to the necessary files.

```bash
python converter.py --pred PATH_TO_PRED_COCO_JSON --output OUTPUT_PATH [--score_thresh THRESHOLD]
```

Or as external pip package as:

```bash
import converter
converter.setup_logging()
converter.convert_pred_coco('path/to/pred_coco.json', 'path/to/result_format_coco.json')
```
