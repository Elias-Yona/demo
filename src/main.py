import argparse
import subprocess
import os
import datetime
import secrets
import csv
from pathlib import Path
from pymongo import MongoClient
import xlwt
from PIL import Image

random_hash = secrets.token_hex

# create the argument parser
parser = argparse.ArgumentParser(description='Extract frames from a video.')
parser.add_argument('video_path', help='path to the input video file')
parser.add_argument('start_timecode', help='start timecode of the frame range')
parser.add_argument('num_frames', type=int, help='number of frames to extract')
parser.add_argument('-o', '--output', default=Path(f'./output/frames/output_%03d_{random_hash(16)}.jpg'),
                    help='output filename pattern')
parser.add_argument('-e', '--export', default=None,
                    help='export data to CSV or XLS file')

# parse the arguments
args = parser.parse_args()

# construct the FFmpeg command to extract the frames in the timecode range
ffmpeg_cmd = ["ffmpeg", "-i", args.video_path, "-ss", args.start_timecode,
              "-vframes", str(args.num_frames), "-q:v", "2", "-y", args.output]

# execute the command using subprocess
subprocess.call(ffmpeg_cmd)

# get the list of extracted frames
frames_list = sorted(os.listdir(Path('./output/frames/')))

# get the middle frame and resize it
middle_frame_idx = len(frames_list) // 2
middle_frame_path = frames_list[middle_frame_idx]
middle_frame = Image.open(Path(f'./output/frames/{middle_frame_path}'))
resized_middle_frame = middle_frame.resize((96, 74))

# save the resized middle frame
thumbnail = Path(f'./output/thumbnails/{middle_frame_idx}_{random_hash(16)}.jpg')
resized_middle_frame.save(thumbnail)
thumbnail_path = thumbnail

# connect to the MongoDB server
client = MongoClient()
db = client['project2']
collection = db['file_uploads']

if args.export:
    # export data to CSV or XLS file
    file_ext = args.export.split('.')[-1]
    if file_ext == 'csv':
        with open(args.export, mode='w', newline='') as csv_file:
            fieldnames = ['file_name', 'file_type', 'file_size', 'upload_date', 'uploaded_by',
                          'description', 'tags', 'file_url', 'frame_range', 'start_timecode', 'thumbnail_path']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for doc in collection.find():
                writer.writerow(doc)
    elif file_ext == 'xls':
        book = xlwt.Workbook(encoding='utf-8')
        sheet = book.add_sheet('Sheet 1')
        row_idx = 0
        for doc in collection.find():
            for col_idx, key in enumerate(doc.keys()):
                sheet.write(row_idx, col_idx, str(doc[key]))
            row_idx += 1
        book.save(Path(f'./output/csv_xls/{random_hash(16)}_{args.export}'))
else:
    # create a document with the metadata
    doc = {
        'file_name': os.path.basename(args.video_path),
        'file_type': 'video',
        'file_size': os.path.getsize(args.video_path),
        'upload_date': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        'uploaded_by': os.getlogin(),
        'description': 'Video file uploaded on ' + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        'tags': ['video', 'metadata'],
        'file_url': args.video_path,
        'frame_range': {'start_timecode': args.start_timecode, 'num_frames': args.num_frames},
        'start_timecode': args.start_timecode,
        'thumbnail_path': thumbnail_path,
    }

    # insert the document into the collection
    result = collection.insert_one(doc, True)
    
    
    print('Inserted document with ID:', result.inserted_id)

# get a list of all the frame files in the current directory
frames = [f for f in os.listdir(Path('./output/frames/')) if f.endswith('.jpg')]

# sort the frames in ascending order
frames.sort()

frame_dir = Path('./output/frames/')
# construct the FFmpeg command to combine the frames into a video
ffmpeg_cmd = ["ffmpeg", "-framerate", "30", "-pattern_type", "glob", "-i", str(frame_dir/'%*.jpg'), "-c:v", "libx264", "-pix_fmt", "yuv420p", Path(f"./output/rendered_shots/{random_hash(16)}.mp4")]
# execute the command using subprocess
subprocess.call(ffmpeg_cmd)