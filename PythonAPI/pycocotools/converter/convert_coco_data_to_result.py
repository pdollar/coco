"""
Created by Gianluca Guzzetta on 18/09/2024

This script converts data format json 'https://cocodataset.org/#format-data' to 'https://cocodataset.org/#format-results' which is a required step to be able to run coco evaluation scripts.
"""

import json
import argparse
import logging
import os
from collections import defaultdict

"""
This script converts annotations from data format to result format
"""


def setup_logging():
    """Configure logging settings."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )


def load_ground_truth_categories(gt_path):
    """
    Load category mapping from ground truth annotations.

    Parameters:
        gt_path (str): Path to ground truth COCO JSON file.

    Returns:
        dict: Mapping from category names to category IDs.
    """
    with open(gt_path, 'r') as f:
        gt_data = json.load(f)

    category_mapping = {}
    for cat in gt_data.get('categories', []):
        category_mapping[cat['name']] = cat['id']

    logging.info(f"Loaded {len(category_mapping)} categories from ground truth.")
    return category_mapping


def convert_pred_coco(pred_path, gt_path, output_path, score_threshold=0.0):
    """
    Convert `pred_coco.json` to COCO Results Format.

    Parameters:
        pred_path (str): Path to the current `pred_coco.json` file.
        gt_path (str): Path to the ground truth COCO JSON file.
        output_path (str): Path to save the converted COCO Results JSON file.
        score_threshold (float): Minimum confidence score to include detections.
    """
    # Load category mapping from ground truth
    category_mapping = load_ground_truth_categories(gt_path)

    # Load predictions
    with open(pred_path, 'r') as f:
        pred_data = json.load(f)

    # Check if pred_data is a dictionary containing 'annotations'
    if isinstance(pred_data, dict):
        if 'annotations' in pred_data:
            anns = pred_data['annotations']
            logging.info("Extracted 'annotations' from prediction data.")
        else:
            raise ValueError("Prediction JSON is a dictionary but does not contain 'annotations' key.")
    elif isinstance(pred_data, list):
        anns = pred_data
        logging.info("Prediction JSON is a list of annotations.")
    else:
        raise ValueError("Invalid format for prediction JSON. Must be a list or a dictionary containing 'annotations'.")

    # Initialize the list for COCO Results Format
    coco_results = []

    # Process each annotation
    for idx, ann in enumerate(anns):
        # Optional: Apply score threshold
        score = ann.get('score', 1.0)  # Default score to 1.0 if not present
        if score < score_threshold:
            continue  # Skip detections below the threshold

        # Map class name to category_id
        category_name = ann.get('category', None)
        if category_name is None:
            category_id = ann.get('category_id', None)
            if category_id is None:
                logging.warning(f"Annotation at index {idx} missing 'category' and 'category_id'. Skipping.")
                continue
        else:
            category_id = category_mapping.get(category_name, None)
            if category_id is None:
                logging.warning(f"Unknown category name '{category_name}' at index {idx}. Skipping.")
                continue

        # Extract image_id
        image_id = ann.get('image_id', None)
        if image_id is None:
            logging.warning(f"Annotation at index {idx} missing 'image_id'. Skipping.")
            continue

        # Extract and format bbox
        bbox = ann.get('bbox', None)
        if bbox is None:
            # Attempt to convert from [x1, y1, x2, y2] to [x, y, width, height]
            bbox_x1 = ann.get('x1', None)
            bbox_y1 = ann.get('y1', None)
            bbox_x2 = ann.get('x2', None)
            bbox_y2 = ann.get('y2', None)
            if None in [bbox_x1, bbox_y1, bbox_x2, bbox_y2]:
                logging.warning(f"Annotation at index {idx} missing bounding box information. Skipping.")
                continue
            bbox = [bbox_x1, bbox_y1, bbox_x2 - bbox_x1, bbox_y2 - bbox_y1]

        # Ensure bbox has four elements
        if not isinstance(bbox, list) or len(bbox) != 4:
            logging.warning(f"Annotation at index {idx} has invalid 'bbox'. Skipping.")
            continue

        # Create the COCO Result annotation
        coco_det = {
            "image_id": image_id,
            "category_id": category_id,
            "bbox": [round(float(coord), 1) for coord in bbox],  # Round to nearest tenth
            "score": float(score)
        }

        # If segmentation is present, include it
        if 'segmentation' in ann:
            coco_det["segmentation"] = ann['segmentation']

        # If keypoints are present, include them
        if 'keypoints' in ann:
            coco_det["keypoints"] = ann['keypoints']
            coco_det["num_keypoints"] = sum(1 for v in ann['keypoints'][2::3] if v > 0)

        # Append to results
        coco_results.append(coco_det)

    # Validate the results
    if not coco_results:
        logging.error("No valid detections found after conversion. Please check your input files and parameters.")
        return

    # Save the converted results
    with open(output_path, 'w') as f:
        json.dump(coco_results, f)

    logging.info(f"Converted {len(coco_results)} detections to COCO Results Format.")
    logging.info(f"Saved COCO Results to '{output_path}'.")


  ######### EXAMPLE USAGE in external script #########
        # import converter
        # 
        # converter.setup_logging()
        # converter.convert_pred_coco('path/to/pred_coco.json', 'path/to/output.json')
