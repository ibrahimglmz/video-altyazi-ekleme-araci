#!/usr/bin/env python3
"""
Grunge Brush Stroke Subtitle Background Generator
=================================================

Creates dynamic grunge-style brush stroke backgrounds for subtitles
with the following features:
- Hand-painted acrylic brush stroke appearance
- Red grunge textured background
- Irregular, wavy edges
- Transparent background outside the brush stroke
- SEPARATE brush stroke for EACH line
- Adjustable width based on text length
- Rounded sans-serif font support
"""

import os
import random
import math
from pathlib import Path
from typing import Tuple, List
import numpy as np

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    # Create dummy classes for type hints when PIL is not available
    class Image:
        class Image:
            pass
    class ImageDraw:
        pass
    class ImageFont:
        pass
    class ImageFilter:
        pass

class GrungeSubtitleGenerator:
    def __init__(self, assets_dir: str = "assets"):
        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(exist_ok=True)
        
        if not PIL_AVAILABLE:
            raise ImportError("PIL/Pillow is required. Install with: pip install Pillow")
        
        # Color palette for grunge red brush stroke - darker, more vibrant reds
        self.red_colors = [
            (200, 16, 46),    # Deep crimson
            (180, 20, 50),    # Rich red
            (190, 30, 45),    # Vibrant crimson
            (170, 25, 40),    # Dark red
            (195, 28, 52),    # Bold red
        ]
        
        # Font settings - Dynamic sizing based on video dimensions
        self.base_font_size = 24  # Base size for 1920x1080 video
        self.font_color = (255, 255, 255, 255)  # White
        
    def get_system_font(self) -> str:
        """Get best available rounded sans-serif font"""
        import platform
        
        system = platform.system()
        
        # Try to find rounded/friendly fonts first
        preferred_fonts = []
        
        if system == "Darwin":  # macOS
            preferred_fonts = [
                "Arial Rounded MT Bold",  # Bold rounded font like in image
                "Avenir Next Rounded",
                "SF Pro Rounded",
                "Avenir Next",
                "Helvetica Neue",
                "Helvetica",
                "Arial"
            ]
        elif system == "Windows":
            preferred_fonts = [
                "Arial Rounded MT Bold",  # Bold rounded font like in image
                "Segoe UI",
                "Calibri",
                "Arial",
                "Tahoma"
            ]
        else:  # Linux
            preferred_fonts = [
                "Ubuntu",
                "DejaVu Sans",
                "Liberation Sans",
                "Arial",
                "FreeSans"
            ]
        
        # Try to load fonts in order of preference
        for font_name in preferred_fonts:
            try:
                # Try different font sizes to test availability
                ImageFont.truetype(font_name, 16)
                return font_name
            except (OSError, IOError):
                continue
        
        # Fallback to default
        return "Arial"

    def create_noise_pattern(self, width: int, height: int, intensity: float = 0.3) -> Image.Image:
        """Create a grunge noise pattern for texture"""
        # Create noise
        noise_array = np.random.random((height, width)) * 255
        
        # Apply intensity
        noise_array = noise_array * intensity
        
        # Convert to PIL Image
        noise_img = Image.fromarray(noise_array.astype(np.uint8), mode='L')
        
        # Add some blur for organic feel
        noise_img = noise_img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        return noise_img

    def create_brush_stroke_mask(self, width: int, height: int, horizontal: bool = True) -> Image.Image:
        """Create a highly organic, natural brush stroke mask with irregular edges"""
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        if horizontal:
            # Horizontal brush stroke
            center_y = height // 2
            stroke_height = height * 0.80  # 80% of total height
            
            # Create highly irregular, natural edges
            top_points = []
            bottom_points = []
            
            # Use multiple sine waves with different frequencies for natural variation
            phase_top = random.uniform(0, math.pi * 2)
            phase_bottom = random.uniform(0, math.pi * 2)
            
            # Random starting and ending heights for taper effect
            start_taper = random.uniform(0.7, 1.0)
            end_taper = random.uniform(0.7, 1.0)
            
            for x in range(0, width, 1):  # Smaller step for smoother curves
                # Calculate taper (brush strokes often start/end thinner)
                progress = x / width
                taper = 1.0
                if progress < 0.15:  # Beginning taper
                    taper = start_taper + (1.0 - start_taper) * (progress / 0.15)
                elif progress > 0.85:  # Ending taper
                    taper = end_taper + (1.0 - end_taper) * ((1.0 - progress) / 0.15)
                
                # Multiple wave frequencies for natural look
                wave1 = math.sin(x * 0.03 + phase_top) * stroke_height * 0.12
                wave2 = math.sin(x * 0.08 + phase_top * 1.5) * stroke_height * 0.08
                wave3 = math.sin(x * 0.15 + phase_top * 0.7) * stroke_height * 0.05
                
                wave_bottom1 = math.sin(x * 0.035 + phase_bottom) * stroke_height * 0.12
                wave_bottom2 = math.sin(x * 0.09 + phase_bottom * 1.3) * stroke_height * 0.08
                wave_bottom3 = math.sin(x * 0.16 + phase_bottom * 0.8) * stroke_height * 0.05
                
                # Random organic variation with Perlin-like noise
                noise_scale = 10
                top_noise = (math.sin(x * 0.2) * math.cos(x * 0.15)) * stroke_height * 0.15
                bottom_noise = (math.sin(x * 0.18) * math.cos(x * 0.13)) * stroke_height * 0.15
                
                # Additional random jitter for texture
                top_jitter = random.uniform(-stroke_height * 0.08, stroke_height * 0.08)
                bottom_jitter = random.uniform(-stroke_height * 0.08, stroke_height * 0.08)
                
                # Combine all variations
                top_wave = wave1 + wave2 + wave3 + top_noise + top_jitter
                bottom_wave = wave_bottom1 + wave_bottom2 + wave_bottom3 + bottom_noise + bottom_jitter
                
                # Apply taper
                current_stroke = stroke_height * taper
                
                top_y = center_y - current_stroke/2 + top_wave
                bottom_y = center_y + current_stroke/2 + bottom_wave
                
                # Ensure points stay within bounds
                top_y = max(1, min(height-2, top_y))
                bottom_y = max(1, min(height-2, bottom_y))
                
                top_points.append((x, int(top_y)))
                bottom_points.append((x, int(bottom_y)))
            
            # Create polygon from points
            polygon_points = top_points + list(reversed(bottom_points))
            draw.polygon(polygon_points, fill=255)
            
            # Add irregular spots and splatters for paint texture
            num_spots = random.randint(5, 12)
            for _ in range(num_spots):
                spot_x = random.randint(int(width * 0.1), int(width * 0.9))
                spot_y = random.randint(int(height * 0.2), int(height * 0.8))
                spot_size = random.randint(2, 6)
                opacity = random.randint(180, 255)
                draw.ellipse([spot_x-spot_size, spot_y-spot_size, 
                            spot_x+spot_size, spot_y+spot_size], fill=opacity)
            
            # Add some brush bristle marks (thin lines)
            num_bristles = random.randint(3, 7)
            for _ in range(num_bristles):
                bristle_x = random.randint(0, width)
                bristle_length = random.randint(3, 8)
                bristle_y_start = random.randint(int(height * 0.3), int(height * 0.7))
                bristle_y_end = bristle_y_start + random.choice([-bristle_length, bristle_length])
                draw.line([(bristle_x, bristle_y_start), (bristle_x, bristle_y_end)], 
                         fill=random.randint(150, 255), width=1)
        
        # Apply variable blur for more natural, painted edge
        # Use stronger blur in some areas, lighter in others
        mask_array = np.array(mask)
        
        # Apply graduated blur for paint-like softness
        blurred_light = mask.filter(ImageFilter.GaussianBlur(radius=0.8))
        blurred_medium = mask.filter(ImageFilter.GaussianBlur(radius=1.5))
        
        # Blend different blur levels
        mask_array = np.array(mask)
        blur_light_array = np.array(blurred_light)
        blur_medium_array = np.array(blurred_medium)
        
        # Random blend for organic feel
        blend_factor = np.random.random(mask_array.shape) * 0.5 + 0.5
        final_array = (mask_array * 0.3 + blur_light_array * 0.4 + blur_medium_array * 0.3).astype(np.uint8)
        
        mask = Image.fromarray(final_array)
        
        return mask

    def wrap_text_smart(self, text: str, max_chars_per_line: int) -> List[str]:
        """Smart text wrapping that respects word boundaries and Turkish text"""
        text = text.strip()
        if len(text) <= max_chars_per_line:
            return [text]

        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            word_length = len(word)
            
            # If word itself is too long, split it
            if word_length > max_chars_per_line:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = []
                    current_length = 0
                
                # Split the long word
                parts = [word[i:i + max_chars_per_line] for i in range(0, word_length, max_chars_per_line)]
                lines.extend(parts[:-1])
                current_line = [parts[-1]]
                current_length = len(parts[-1])
                continue

            # Check if adding this word would exceed the limit
            space_needed = 1 if current_line else 0
            if current_length + word_length + space_needed > max_chars_per_line:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length + space_needed

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def create_single_line_background(self, text: str, font: ImageFont.FreeTypeFont, padding: int = 20) -> Image.Image:
        """Create grunge brush stroke background for a SINGLE line of text"""
        
        # Calculate text dimensions for this line
        temp_img = Image.new('RGBA', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        
        line_bbox = temp_draw.textbbox((0, 0), text, font=font)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]
        
        # Background dimensions with padding
        bg_width = line_width + padding * 2
        bg_height = line_height + padding
        
        # Ensure minimum dimensions
        bg_width = max(bg_width, 100)
        bg_height = max(bg_height, 40)
        
        # Create brush stroke mask
        brush_mask = self.create_brush_stroke_mask(bg_width, bg_height, horizontal=True)
        
        # Create noise texture
        noise = self.create_noise_pattern(bg_width, bg_height, intensity=0.2)
        
        # Create base red background - random color for each line with transparency
        base_red = random.choice(self.red_colors)
        # Alpha between 200-230 for slight transparency (255 is fully opaque)
        alpha = random.randint(200, 230)
        background = Image.new('RGBA', (bg_width, bg_height), (*base_red, alpha))
        
        # Apply color variations for grunge effect
        bg_array = np.array(background)
        noise_array = np.array(noise)
        
        # Add noise to color channels
        for channel in range(3):  # RGB channels
            variation = (noise_array.astype(float) - 127) * 0.3
            bg_array[:, :, channel] = np.clip(
                bg_array[:, :, channel].astype(float) + variation, 
                0, 255
            ).astype(np.uint8)
        
        # Create final background with variations
        textured_bg = Image.fromarray(bg_array)
        
        # Apply brush stroke mask
        final_bg = Image.new('RGBA', (bg_width, bg_height), (0, 0, 0, 0))
        final_bg.paste(textured_bg, mask=brush_mask)
        
        return final_bg

    def create_subtitle_with_background(self, text: str, output_path: str, video_width: int = 1920, video_height: int = 1080) -> str:
        """Create a complete subtitle image with SEPARATE grunge background for EACH line"""
        
        # Calculate dynamic font size based on video dimensions and text length
        scale_factor = min(video_width / 1920, video_height / 1080)
        base_font_size = int(self.base_font_size * scale_factor)
        
        # Adjust font size based on text length to ensure readability
        text_length = len(text)
        if text_length > 100:
            font_size = max(int(base_font_size * 0.8), 14)
        elif text_length > 50:
            font_size = max(int(base_font_size * 0.9), 16)
        else:
            font_size = max(base_font_size, 16)
        
        # Get font
        font_name = self.get_system_font()
        try:
            font = ImageFont.truetype(font_name, font_size)
        except (OSError, IOError):
            font = ImageFont.load_default()
        
        # Smart text wrapping based on video width
        max_chars_per_line = max(20, int(video_width * 0.08))
        wrapped_lines = self.wrap_text_smart(text, max_chars_per_line)
        
        # Calculate dimensions for each line
        temp_img = Image.new('RGBA', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        
        line_info = []
        max_line_width = 0
        total_height = 0
        
        padding = 20
        line_spacing = 2  # Space between lines - reduced for tighter spacing
        
        for line in wrapped_lines:
            line_bbox = temp_draw.textbbox((0, 0), line, font=font)
            line_width = line_bbox[2] - line_bbox[0]
            line_height = line_bbox[3] - line_bbox[1]
            
            bg_width = line_width + padding * 2
            bg_height = line_height + padding
            
            line_info.append({
                'text': line,
                'width': line_width,
                'height': line_height,
                'bg_width': max(bg_width, 100),
                'bg_height': max(bg_height, 40)
            })
            
            max_line_width = max(max_line_width, line_info[-1]['bg_width'])
            total_height += line_info[-1]['bg_height']
        
        # Add spacing between lines
        if len(wrapped_lines) > 1:
            total_height += (len(wrapped_lines) - 1) * line_spacing
        
        # Create final canvas
        canvas_width = min(max_line_width, int(video_width * 0.85))
        canvas_height = min(total_height, int(video_height * 0.4))
        
        final_image = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        
        # Draw each line with its own background
        current_y = 0
        
        for info in line_info:
            # Create background for this line
            line_bg = self.create_single_line_background(info['text'], font, padding)
            
            # Calculate position to center the line background
            x_offset = (canvas_width - info['bg_width']) // 2
            
            # Paste the line background
            final_image.paste(line_bg, (x_offset, current_y), line_bg)
            
            # Draw text on top of the background
            draw = ImageDraw.Draw(final_image)
            text_x = x_offset + padding
            text_y = current_y + padding // 2
            
            draw.text(
                (text_x, text_y),
                info['text'],
                font=font,
                fill=self.font_color
            )
            
            # Move to next line position
            current_y += info['bg_height'] + line_spacing
        
        # Save the image
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final_image.save(str(output_path), 'PNG')
        
        return str(output_path)

    def create_dynamic_backgrounds_for_segments(self, segments: List[dict], output_dir: str, video_width: int = 1920, video_height: int = 1080) -> List[str]:
        """Create grunge backgrounds for all subtitle segments"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        background_files = []
        
        for i, segment in enumerate(segments):
            text = segment.get('text', '').strip()
            if not text:
                continue
            
            # Create filename
            output_file = output_dir / f"subtitle_bg_{i:04d}.png"
            
            # Create subtitle with background
            bg_path = self.create_subtitle_with_background(
                text, 
                str(output_file),
                video_width=video_width,
                video_height=video_height
            )
            background_files.append(bg_path)
        
        return background_files

# Test function
def test_grunge_generator():
    """Test the grunge subtitle generator"""
    generator = GrungeSubtitleGenerator()
    
    # Test with sample texts including long Turkish text
    test_texts = [
        "valizler alınmayacak!",
        "Hello World!",
        "Bu bir test altyazısıdır",
        "Multi-line subtitle\nwith two lines",
        "Bu çok uzun bir altyazı metnidir ve otomatik olarak alt satıra geçmesi gerekiyor çünkü video genişliğini aşmaması lazım",
        "Bugün metro istanbul'dan yeni bir açıklama geldi ve bu açıklama çok önemli bilgiler içeriyor",
        "Very long English text that should wrap to multiple lines automatically and fit within the video frame without overflowing"
    ]
    
    for i, text in enumerate(test_texts):
        output_path = f"test_output/grunge_subtitle_{i}.png"
        result = generator.create_subtitle_with_background(text, output_path)
        print(f"Created: {result}")

if __name__ == "__main__":
    test_grunge_generator()