import logging
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional, List, Tuple
import easyocr

logger = logging.getLogger(__name__)


class ImageProcessor:
    def __init__(self, ocr_languages=['en'], use_gpu=False):
        """Initialize OCR reader"""
        self.reader = easyocr.Reader(ocr_languages, gpu=use_gpu)
        self.logger = logger

    def extract_data_from_image(self, image_path: str) -> Optional[pd.DataFrame]:
        """
        Extract tabular data from image using OCR with spatial awareness
        
        Args:
            image_path: Path to image file
            
        Returns:
            DataFrame with extracted data or None if extraction fails
        """
        try:
            image_path = Path(image_path)
            if not image_path.exists():
                self.logger.error(f"Image file not found: {image_path}")
                return None
                
            # Read image
            img = cv2.imread(str(image_path))
            if img is None:
                self.logger.error(f"Failed to read image: {image_path}")
                return None
            
            # Extract text with spatial information
            results = self.reader.readtext(img)
            
            if not results:
                self.logger.warning("No text detected in image")
                return None
            
            # Parse as table using spatial layout
            df = self._parse_spatial_table(results, img.shape)
            
            if df is not None and len(df) > 0:
                self.logger.info(f"Table extracted: {df.shape[0]} rows, {df.shape[1]} columns")
                return df
                
            self.logger.warning("Could not extract structured table from image")
            return None
            
        except Exception as e:
            self.logger.error(f"Error extracting data from image: {e}", exc_info=True)
            return None

    def _parse_spatial_table(self, ocr_results: List, img_shape: Tuple) -> Optional[pd.DataFrame]:
        """
        Parse OCR results into table using spatial layout
        
        OCR results format: [(bbox, text, confidence), ...]
        where bbox = [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        """
        try:
            if not ocr_results:
                return None
            
            # Extract text boxes with positions
            text_boxes = []
            for bbox, text, conf in ocr_results:
                # Get bounding box coordinates
                x_coords = [point[0] for point in bbox]
                y_coords = [point[1] for point in bbox]
                
                x_min, x_max = min(x_coords), max(x_coords)
                y_min, y_max = min(y_coords), max(y_coords)
                x_center = (x_min + x_max) / 2
                y_center = (y_min + y_max) / 2
                
                text_boxes.append({
                    'text': text.strip(),
                    'x_min': x_min,
                    'x_max': x_max,
                    'y_min': y_min,
                    'y_max': y_max,
                    'x_center': x_center,
                    'y_center': y_center,
                    'confidence': conf
                })
            
            # Sort by vertical position (top to bottom)
            text_boxes.sort(key=lambda x: x['y_center'])
            
            # Group into rows by vertical proximity
            rows = self._group_into_rows(text_boxes)
            
            self.logger.info(f"Grouped into {len(rows)} rows")
            for i, row in enumerate(rows[:5]):
                self.logger.info(f"Row {i}: {len(row)} cells")
            
            if not rows or len(rows) < 2:
                # Fallback: create single column DataFrame
                self.logger.warning("Not enough rows, using fallback")
                df = pd.DataFrame({'Data': [box['text'] for box in text_boxes]})
                return df
            
            # Find the row with most cells (likely the header row)
            header_row_idx = max(range(len(rows)), key=lambda i: len(rows[i]))
            header_row = rows[header_row_idx]
            
            # Determine columns from header row
            column_positions = self._detect_columns(header_row)
            
            # Build table using header row and subsequent rows
            # Extract headers
            headers = [box['text'].strip() for box in header_row]
            
            # Build data rows (only rows after header row)
            table_data = []
            for row_idx, row_boxes in enumerate(rows):
                # Skip rows before header row
                if row_idx <= header_row_idx:
                    continue
                    
                row_data = [''] * len(column_positions)
                for box in row_boxes:
                    # Find which column this box belongs to
                    col_idx = self._assign_to_column(box, column_positions)
                    if col_idx < len(row_data):
                        # Append if cell already has content
                        if row_data[col_idx]:
                            row_data[col_idx] += ' ' + box['text']
                        else:
                            row_data[col_idx] = box['text']
                table_data.append(row_data)
            
            # Create DataFrame
            if not table_data:
                return pd.DataFrame({'Data': [box['text'] for box in text_boxes]})
            
            # Clean headers
            headers = [str(h).strip() if h else f'Column_{i}' for i, h in enumerate(headers)]
            
            df = pd.DataFrame(table_data, columns=headers)
            
            # Try to convert numeric columns
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass
            
            return df
            
        except Exception as e:
            self.logger.debug(f"Failed to parse spatial table: {e}")
            # Fallback: single column
            texts = [box['text'] for box in text_boxes]
            return pd.DataFrame({'Data': texts}) if texts else None

    def _group_into_rows(self, text_boxes: List[dict], y_threshold: float = 20) -> List[List[dict]]:
        """Group text boxes into rows based on vertical position"""
        if not text_boxes:
            return []
        
        rows = []
        current_row = [text_boxes[0]]
        current_y = text_boxes[0]['y_center']
        
        for box in text_boxes[1:]:
            # If box is close vertically to current row, add to current row
            if abs(box['y_center'] - current_y) < y_threshold:
                current_row.append(box)
            else:
                # Start new row
                # Sort current row by x position (left to right)
                current_row.sort(key=lambda x: x['x_center'])
                rows.append(current_row)
                current_row = [box]
                current_y = box['y_center']
        
        # Add last row
        if current_row:
            current_row.sort(key=lambda x: x['x_center'])
            rows.append(current_row)
        
        return rows

    def _detect_columns(self, first_row: List[dict]) -> List[float]:
        """Detect column positions from first row"""
        if not first_row:
            return []
        
        # Use x_center of each box in first row as column positions
        column_positions = [box['x_center'] for box in first_row]
        column_positions.sort()
        return column_positions

    def _assign_to_column(self, box: dict, column_positions: List[float]) -> int:
        """Assign a text box to the nearest column"""
        if not column_positions:
            return 0
        
        x = box['x_center']
        
        # Find nearest column
        distances = [abs(x - col_pos) for col_pos in column_positions]
        return distances.index(min(distances))


def extract_data_from_image(image_path: str) -> Optional[pd.DataFrame]:
    """Convenience function"""
    processor = ImageProcessor()
    return processor.extract_data_from_image(image_path)
