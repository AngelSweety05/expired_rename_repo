import time
import os
import asyncio
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, concatenate_videoclips
import time
import os
import requests

import requests
from PIL import Image
from io import BytesIO
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def fix_thumb(thumb):
    width = 0
    height = 0
    try:
        if thumb != None:
            metadata = extractMetadata(createParser(thumb))
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
                Image.open(thumb).convert("RGB").save(thumb)
                img = Image.open(thumb)
                img.resize((320, height))
                img.save(thumb, "JPEG")
    except Exception as e:
        print(e)
        thumb = None 
    return thumb
    
async def take_screen_shot(video_file, output_directory, ttl):
    out_put_file_name = f"{output_directory}/{time.time()}.jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None

async def add_watermark(image_path, output_path):
    try:
        # Download the logo image from the URL
        logo_url = "https://i.ibb.co/2sCD70h/Picsart-24-11-08-15-40-02-118.png"
        response = requests.get(logo_url)
        logo = Image.open(BytesIO(response.content))

        # Open the main image (screenshot)
        img = Image.open(image_path)
        img_width, img_height = img.size

        # Set the new logo size as 80% of the image dimensions
        new_width = int(img_width * 0.7)  # 80% of image width
        new_height = int(img_height * 0.7)  # 30% of image height

        # Maintain the aspect ratio of the logo
        logo_ratio = logo.width / logo.height
        if new_width / logo_ratio > new_height:
            new_width = int(new_height * logo_ratio)  # Adjust width to maintain aspect ratio
        else:
            new_height = int(new_width / logo_ratio)  # Adjust height to maintain aspect ratio

        # Resize the logo
        logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Calculate position (center-bottom)
        x_pos = 20  # put the logo at left bottom
        y_pos = img_height - new_height + 20 # Place the logo 
        # Paste the logo onto the image (with transparency support)
        img.paste(logo, (x_pos, y_pos), logo)  # The third argument is the mask for transparency

        # Save the watermarked image
        img.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error adding logo watermark: {e}")
        return None

async def download_file(url, output_path):
    """Downloads a file from the given URL."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        response = requests.get(url)
        response.raise_for_status()
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded file from {url} to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

# Progress callback function
async def progress_bar(current, total, msg, last_reported=0):
    """Callback to update the progress on Telegram every 10%."""
    percentage = int((current / total) * 100)
    if percentage - last_reported >= 10 or percentage == 100:  # Update only every 10%
        last_reported = percentage
        await msg.edit(f"💘 Adding intro... {percentage}% completed")
    return last_reported

async def add_intro_to_video(main_video_path, output_path, msg):
    try:
        await msg.edit("⚙ Processing to add watermark to video file... \n🧩This may take some time, please be patience \nThank You 💘")
        intro_url = "https://raw.githubusercontent.com/AngelSweety05/expired_rename_repo/main/clips/cc.mp4"
        intro_path = f"{time.time()}/intro.mp4"
        logger.info(intro_path)
        # Download the intro clip
        intro_path = await download_file(intro_url, intro_path)
        if intro_path is None:
            raise Exception("Intro clip could not be downloaded.")

        # Load the videos
        main_video = VideoFileClip(main_video_path)
        intro_clip = VideoFileClip(intro_path)

        # Resize the intro clip to match the main video’s resolution using the resize() method
        intro_clip = intro_clip.resize(newsize=(main_video.w, main_video.h))  # Resize to main video's dimensions

        # Concatenate the intro and main video
        final_video = concatenate_videoclips([intro_clip, main_video])

        await msg.edit("🚾 Adding watermark to video file... \n🧩This may take some time, please be patience \nThank You 💘")
        final_video.write_videofile(
            output_path, codec="libx265", 
            audio_codec="aac", 
            bitrate="1000k", 
            fps=main_video.fps, 
            threads=4, 
            )
        return output_path
    except Exception as e:
        print(f"Error adding intro to video: {e}")
        return None


# ====================
# ====================

# import logging
# from pymediainfo import MediaInfo

# # Set up logging configuration
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# def get_video_metadata(file_path):
#     # Log that we're starting to extract metadata
#     logger.info(f"Extracting metadata from file: {file_path}")
    
#     try:
#         # Extract media information
#         media_info = MediaInfo.parse(file_path)
        
#         # Initialize variables
#         resolution = None
#         languages = []
#         subtitles = []
        
#         # Iterate through the tracks to find the video, audio, and subtitle tracks
#         for track in media_info.tracks:
#             if track.track_type == 'Video':
#                 resolution = f"{track.width}x{track.height}"
#                 logger.info(f"Found resolution: {resolution}")
            
#             if track.track_type == 'Audio' and track.language:
#                 languages.append(track.language)
#                 logger.info(f"Found audio language: {track.language}")
            
#             if track.track_type == 'Text' and track.language:
#                 subtitles.append(track.language)
#                 logger.info(f"Found subtitle language: {track.language}")
        
#         # Return resolution, languages, and subtitles
#         return resolution, languages, subtitles
    
#     except Exception as e:
#         logger.error(f"Error extracting metadata: {e}")
#         return None, [], []
    

# ====================
# ====================

# import ffmpeg
# import json

# def get_video_metadata(file_path):
#     # Use ffmpeg to fetch the file's metadata
#     probe = ffmpeg.probe(file_path, v='error', select_streams='v:0', show_entries='stream=width,height,codec_name,disposition', output_format='json')
    
#     # Parse the metadata
#     metadata = json.loads(probe)
    
#     # Get resolution
#     width = metadata['streams'][0]['width']
#     height = metadata['streams'][0]['height']
#     resolution = f"{width}x{height}"

#     # Get language (from the 'tags' field)
#     languages = []
#     for stream in metadata['streams']:
#         if 'tags' in stream and 'language' in stream['tags']:
#             languages.append(stream['tags']['language'])
    
#     # Get subtitle languages
#     subtitles = []
#     for stream in metadata['streams']:
#         if stream['codec_type'] == 'subtitle':
#             if 'tags' in stream and 'language' in stream['tags']:
#                 subtitles.append(stream['tags']['language'])
    
#     return resolution, languages, subtitles











# =============================================================================
# =============================================================================
# =========================💘DUMMY💘====================================================
# =============================================================================
# =============================================================================
# =============================================================================
# async def download_file(url, output_path):
#     """Downloads a file from the given URL."""
#     try:
#         os.makedirs(os.path.dirname(output_path), exist_ok=True)
#         response = requests.get(url)
#         response.raise_for_status()  # Ensure successful download
#         with open(output_path, 'wb') as file:
#             file.write(response.content)
#         print(f"Downloaded file from {url} to {output_path}")
#         return output_path
#     except Exception as e:
#         print(f"Error downloading file: {e}")
#         return None

# async def add_intro_to_video(main_video_path, output_path, msg):
#     try:
#         await msg.edit("💘")
#         intro_url = "https://raw.githubusercontent.com/criminalCoder/kkk/main/clips/clip.mp4"  # Ensure raw URL
#         intro_path = f"{time.time()}/intro.mp4"

#         # Download the intro clip
#         intro_path = await download_file(intro_url, intro_path)
#         if intro_path is None:
#             raise Exception("Intro clip could not be downloaded.")

#         # Load the videos
#         main_video = VideoFileClip(main_video_path)
#         intro_clip = VideoFileClip(intro_path)

#         fps = main_video.fps 
#         intro_clip = intro_clip.with_fps(fps)
                
#         intro_clip = intro_clip.resize(newsize=(main_video.w, main_video.h))  # Resize to main video's dimensions

#         # intro_clip = intro_clip.with_width(main_video.w)  # Match width
#         # intro_clip = intro_clip.with_height(main_video.h)  # Match height

#         # Print durations for debugging
#         print(f"main_video fps : {fps}")
#         print(f"Intro Video Duration: {intro_clip.duration}")

#         # Concatenate videos: [Intro] + [Main Video]
#         final_video = concatenate_videoclips([main_video, intro_clip])

#         # Save final video
#         final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", bitrate="1000k", fps=fps, threads=4)

#         # final_video.write_videofile(output_path)
#         # final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", bitrate="500k", fps=fps, threads=4)
#         print(f"Final video created successfully at {output_path}")
#         return output_path
#     except Exception as e:
#         print(f"Error adding intro to video: {e}")

import subprocess
import time

# async def add_intro_to_video(main_video_path, output_path, lazy_msg):
#     try:
#         await lazy_msg.edit("⏳Adding watermark to video file... \n🧩This may take some time, please be patience \nThank You 💘")

#         intro_url = "https://raw.githubusercontent.com/criminalCoder/kkk/main/clips/clip.mp4"  # Ensure raw URL
#         intro_path = f"{time.time()}/intro.mp4"

#         # Download the intro clip
#         intro_path = await download_file(intro_url, intro_path)
#         if intro_path is None:
#             raise Exception("Intro clip could not be downloaded.")

#         # Optimized ffmpeg command with faster encoding and hardware acceleration (if available)
#         ffmpeg_command = [
#             "ffmpeg", 
#             "-i", intro_path, 
#             "-i", main_video_path,
#             "-filter_complex", 
#             "[0:v]fps=30,scale=1280:720[v0];[1:v]fps=30,scale=1280:720[v1];[v0][v1]concat=n=2:v=1:a=0[outv];[0:a][1:a]concat=n=2:v=0:a=1[outa]",  # Concatenate video and audio
#             "-map", "[outv]", 
#             "-map", "[outa]",  # Ensure audio is mapped
#             "-c:v", "libx265",  # Use H.264 codec for video
#             "-c:a", "aac",  # Use AAC codec for audio
#             "-preset", "ultrafast",  # Use faster encoding preset
#             "-crf", "31",  # Adjust output quality (lower value = better quality, but slower)
#             "-threads", "4",
#             "-y",  # Overwrite output file if exists
#             output_path
#         ]
        
#         # Run the ffmpeg command to concatenate videos
#         process = await asyncio.create_subprocess_exec(*ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         stdout, stderr = await process.communicate()

#         # Check for errors in ffmpeg process
#         if process.returncode != 0:
#             print(f"FFmpeg error: {stderr.decode()}")
#         else:
#             print(f"Final video saved at {output_path}")
        
#         return output_path

#         # print(f"Final video saved at {output_path}")
#         # return output_path
#     except subprocess.CalledProcessError as e:
#         print(f"Error adding intro to video: {e}")


# Example usage
# video_clip_path = "path_to_main_video.mp4"
# output_video_path = "output_video.mp4"
# final_video = await add_intro_to_video(video_clip_path, output_video_path)

# # Function to download a file from the given URL
# async def download_file(url, output_path):
#     """Downloads a file from the given URL."""
#     try:
#         os.makedirs(os.path.dirname(output_path), exist_ok=True)

#         response = requests.get(url)
#         response.raise_for_status()
#         with open(output_path, 'wb') as file:
#             file.write(response.content)
#         print(f"Downloaded file from {url} to {output_path}")
#         return output_path
#     except Exception as e:
#         print(f"Error downloading file: {e}")
#         return None


# # Function to add an intro to a video
# async def add_intro_to_video(main_video_path, output_path):
#     try:
#         # Correct raw URL for intro clip
#         intro_url = "https://raw.githubusercontent.com/criminalCoder/kkk/main/clips/clip.mp4"
#         intro_path = f"{time.time()}/intro.mp4"

#         # Download the intro clip
#         intro_path = await download_file(intro_url, intro_path)
#         if intro_path is None:
#             raise Exception("Intro clip could not be downloaded.")

#         # Load the main video and intro clip
#         main_video = VideoFileClip(main_video_path)
#         intro_clip = VideoFileClip(intro_path)

#         # Debugging: Check if video files are loaded correctly
#         if main_video.duration <= 0:
#             raise Exception("Main video could not be loaded or is empty.")
#         if intro_clip.duration <= 0:
#             raise Exception("Intro clip could not be loaded or is empty.")
        
#         print(f"Main Video Duration: {main_video.duration}")
#         print(f"Intro Video Duration: {intro_clip.duration}")

#         # Concatenate videos
#         middle_time = main_video.duration / 2
#         # first_half = main_video.subclip(0, middle_time)
#         # second_half = main_video.subclip(middle_time, main_video.duration)
#         final_video = concatenate_videoclips([intro_clip, main_video])

#         # Save final video
#         final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
#         print(f"Final video created successfully at {output_path}")
#         return output_path
#     except Exception as e:
#         print(f"Error adding intro to video: {e}")
#         return None




# async def download_file(url, output_path):
#     """Downloads a file from the given URL."""
#     try:
#         os.makedirs(os.path.dirname(output_path), exist_ok=True)

#         response = requests.get(url)
#         response.raise_for_status()
#         with open(output_path, 'wb') as file:
#             file.write(response.content)
#         print(f"Downloaded file from {url} to {output_path}")
#         return output_path
#     except Exception as e:
#         print(f"Error downloading file: {e}")
#         return None        

# import time
# async def add_intro_to_video(main_video_path, output_path):
#     try:
#         # URL of the intro clip
#         # intro_url = "https://github.com/criminalCoder/kkk/blob/main/clips/clip.mp4"
#         intro_url = "https://raw.githubusercontent.com/criminalCoder/kkk/main/clips/clip.mp4"


#         # Download the intro clip
#         intro_path = f"{time.time()}/intro.mp4"
#         await download_file(intro_url, intro_path)

#         # Load the main video and intro clip
#         main_video = VideoFileClip(main_video_path)
#         intro_clip = VideoFileClip(intro_path)

#         # Calculate the middle point of the main video
#         middle_time = main_video.duration / 2

#         # Split the main video into two parts: before and after the middle point
#         first_half = main_video.subclip(0, middle_time)
#         second_half = main_video.subclip(middle_time, main_video.duration)

#         # Concatenate: [Intro] + [First Half] + [Intro] + [Second Half]
#         final_video = concatenate_videoclips([intro_clip, first_half, intro_clip, second_half])

#         # Write the final video to the output path
#         final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
#         print(f"Final video created successfully at {output_path}")
#         return output_path
#     except Exception as e:
#         print(f"Error adding intro to video: {e}")

# async def add_watermark(image_path, output_path):
#     try:
#         # Download the logo image from the URL
#         logo_url = "https://i.ibb.co/2sCD70h/Picsart-24-11-08-15-40-02-118.png"
#         response = requests.get(logo_url)
#         logo = Image.open(BytesIO(response.content))
#         logw , logh = logo.size

#         # Open the main image (screenshot)
#         img = Image.open(image_path)
#         img_width, img_height = img.size

#         # Adjust max logo size to increase its dimensions
#         max_logo_width = img_width - 300  # Adjust this for larger width
#         max_logo_height = img_height // 2   # Adjust this for larger height

#         # Maintain aspect ratio while resizing the logo
#         logo_ratio = logo.width / logo.height
#         if logo.width > logo.height:
#             new_width = min(max_logo_width, logo.width)  # Ensure logo width does not exceed max width
#             new_height = int(new_width / logo_ratio)  # Adjust height to maintain aspect ratio
#         else:
#             new_height = min(max_logo_height, logo.height)  # Ensure logo height does not exceed max height
#             new_width = int(new_height * logo_ratio)  # Adjust width to maintain aspect ratio

#         # Resize the logo
#         logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)

#         # Calculate position (center-bottom)
#         x_pos = (img_width - new_width) // 2  # Center the logo horizontally
#         y_pos = img_height - new_height - 10  # Place the logo 30px from the bottom

#         # Paste the logo onto the image (with transparency support)
#         img.paste(logo, (x_pos, y_pos), logo)  # The third argument is the mask for transparency

#         # Save the watermarked image
#         img.save(output_path)
#         return output_path
#     except Exception as e:
#         print(f"Error adding logo watermark: {e}")
#         return None

# async def add_watermark(image_path, output_path, watermark_text="TEST"):
#     try:
#         # Open the image
#         img = Image.open(image_path)
#         width, height = img.size
#         draw = ImageDraw.Draw(img)

#         # Use default font (no need to specify a custom font)
#         # font = ImageFont.load_default()
#         # font = ImageFont.load("arial.pil")
#         font = ImageFont.truetype("/usr/local/share/fonts/arial.ttf", 25)


#         # Calculate text size (bounding box)
#         bbox = draw.textbbox((0, 0), watermark_text, font=font)
#         text_width = bbox[2] - bbox[0]
#         text_height = bbox[3] - bbox[1]

#         # Position of watermark (bottom-right corner)
#         x_pos = width - text_width // 2 # center
#         y_pos = height - text_height - 10  # 10 pixels from the bottom edge

#         # Add watermark text to the image
#         draw.text((x_pos, y_pos), watermark_text, font=font, fill="white")

#         # Save the watermarked image
#         img.save(output_path)
#         return output_path
#     except Exception as e:
#         print(f"Error adding watermark: {e}")
#         return None



# async def add_watermark(image_path, output_path, watermark_text="Join @real_MoviesAdda6"):
#     try:
#         img = Image.open(image_path)
#         width, height = img.size
#         draw = ImageDraw.Draw(img)

#         # Load a font
#         # font = ImageFont.truetype("arial.ttf", 40)
#         font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

#         # Calculate text size (bounding box)
#         bbox = draw.textbbox((0, 0), watermark_text, font=font)
#         text_width = bbox[2] - bbox[0]
#         text_height = bbox[3] - bbox[1]

#         # Position of watermark
#         x_pos = width - text_width - 10  # 10 pixels from the right edge
#         y_pos = height - text_height - 10  # 10 pixels from the bottom edge

#         # Add watermark
#         draw.text((x_pos, y_pos), watermark_text, font=font, fill="white")

#         # Save the watermarked image
#         img.save(output_path)
#         return output_path
#     except Exception as e:
#         print(f"Error adding watermark: {e}")
#         return None
