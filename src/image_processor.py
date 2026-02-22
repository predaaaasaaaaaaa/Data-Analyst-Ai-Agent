import logging
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional
import easyocr
import pytesseract

logger = logging.getLogger(__name__)


class ImageProcessor:
    def __init__(self, ocr_languages=['en'], use_gpu=False):
        """Initialize OCR reader"""
        self.reader = easyocr.Reader(ocr_languages, gpu=use_gpu)
        self.logger = logger

    def extract_data_from_image(self, image_path: str) -> Optional[pd.DataFrame]:
        """
        Extract tabular data from image using OCR
        
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
            
            # Try table detection first
            df = self._detect_table(img)
            if df is not None and len(df) > 0:
                self.logger.info(f"Table detected: {df.shape[0]} rows, {df.shape[1]} columns")
                return df
            
            # Fallback to OCR-based extraction
            df = self._extract_via_ocr(img)
            if df is not None and len(df) > 0:
                self.logger.info(f"Data extracted via OCR: {df.shape[0]} rows, {df.shape[1]} columns")
                return df
                
            self.logger.warning("No data could be extracted from image")
            return None
            
        except Exception as e:
            self.logger.error(f"Error extracting data from image: {e}", exc_info=True)
            return None

    def _detect_table(self, img) -> Optional[pd.DataFrame]:
        """Detect and extract table from image"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply preprocessing
            blur = cv2.GaussianBlur(gray, (3, 3), 0)
            _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return None
            
            # Find largest contour (likely the table)
            largest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest)
            
            # Extract table region
            table_region = img[y:y+h, x:x+w]
            
            # Use OCR on table region
            results = self.reader.readtext(table_region)
            
            if not results:
                return None
            
            # Convert OCR results to structured data
            text_data = [r[1] for r in results]
            
            # Try to parse as table
            df = self._parse_ocr_as_table(text_data)
            return df
            
        except Exception as e:
            self.logger.debug(f"Table detection failed: {e}")
            return None

    def _extract_via_ocr(self, img) -> Optional[pd.DataFrame]:
        """Extract data using OCR directly"""
        try:
            # Use EasyOCR
            results = self.reader.readtext(img)
            
            if not results:
                return None
            
            # Extract text
            text_data = [r[1] for r in results]
            
            # Parse as table
            df = self._parse_ocr_as_table(text_data)
            return df
            
        except Exception as e:
            self.logger.debug(f"OCR extraction failed: {e}")
            return None

    def _parse_ocr_as_table(self, text_data) -> Optional[pd.DataFrame]:
        """Parse OCR text data into structured DataFrame"""
        try:
            if not text_data:
                return None
            
            # Try to detect headers and rows
            # Simple heuristic: split by common delimiters
            rows = []
            for line in text_data:
                # Try to split by common separators
                cells = [cell.strip() for cell in line.split() if cell.strip()]
                if cells:
                    rows.append(cells)
            
            if not rows or len(rows) < 2:
                # If can't parse, create single column DataFrame
                df = pd.DataFrame({'Data': text_data})
                return df
            
            # Create DataFrame
            # Use first row as header if it looks like headers
            headers = rows[0]
            data = rows[1:]
            
            # Pad rows to same length as headers
            padded_data = []
            for row in data:
                if len(row) < len(headers):
                    row.extend([''] * (len(headers) - len(row)))
                padded_data.append(row[:len(headers)])
            
            df = pd.DataFrame(padded_data, columns=headers)
            
            # Try to convert numeric columns
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass
            
            return df
            
        except Exception as e:
            self.logger.debug(f"Failed to parse OCR data as table: {e}")
            return None


def extract_data_from_image(image_path: str) -> Optional[pd.DataFrame]:
    """Convenience function"""
    processor = ImageProcessor()
    return processor.extract_data_from_image(image_path)
