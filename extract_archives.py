"""
Extract all video archives to VIDEOS folder
Extracts all .zip files from archives/ folder and puts videos in VIDEOS/
"""

import os
import zipfile
import shutil

def extract_all_archives():
    """Extract all zip archives from archives/ folder to VIDEOS/"""
    
    archives_folder = "archives"
    videos_folder = "VIDEOS"
    
    # Create VIDEOS folder if it doesn't exist
    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder)
        print(f"[LOG] Created {videos_folder} folder")
    
    # Check if archives folder exists
    if not os.path.exists(archives_folder):
        print(f"[ERROR] {archives_folder} folder not found!")
        return
    
    # Get all zip files
    zip_files = [f for f in os.listdir(archives_folder) if f.endswith('.zip')]
    
    if not zip_files:
        print(f"[INFO] No zip files found in {archives_folder} folder")
        return
    
    print(f"[LOG] Found {len(zip_files)} archive(s) to extract")
    print(f"[LOG] Extracting all videos to {videos_folder}/\n")
    
    total_extracted = 0
    
    for zip_file in sorted(zip_files):
        zip_path = os.path.join(archives_folder, zip_file)
        print(f"[LOG] Processing: {zip_file}")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Get list of files in the zip
                file_list = zip_ref.namelist()
                video_files = [f for f in file_list if f.endswith('.mp4')]
                
                print(f"  Found {len(video_files)} video(s)")
                
                # Extract each video file
                for video_file in video_files:
                    # Extract to VIDEOS folder
                    zip_ref.extract(video_file, videos_folder)
                    
                    # If the extracted file is in a subdirectory, move it to root of VIDEOS
                    extracted_path = os.path.join(videos_folder, video_file)
                    if os.path.dirname(video_file):  # If file was in a subdirectory
                        final_path = os.path.join(videos_folder, os.path.basename(video_file))
                        if extracted_path != final_path:
                            shutil.move(extracted_path, final_path)
                    
                    total_extracted += 1
                
                print(f"  Extracted {len(video_files)} video(s)\n")
                
        except Exception as e:
            print(f"  Error extracting {zip_file}: {e}\n")
            continue
    
    print("="*60)
    print(f"[SUCCESS] Extraction complete!")
    print(f"Total videos extracted: {total_extracted}")
    print(f"Location: {os.path.abspath(videos_folder)}/")
    print("="*60)
    
    # Clean up any empty subdirectories that might have been created
    for root, dirs, files in os.walk(videos_folder, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):  # If directory is empty
                    os.rmdir(dir_path)
            except:
                pass

if __name__ == "__main__":
    extract_all_archives()
