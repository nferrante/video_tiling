import os
import cv2
import numpy as np

# Build our video path list. Input the path and video name information. Each row corresponds to a row in the output video
video_directory = "vids"
video_path_out = os.path.join(video_directory, "test.mp4")
video_path_list = [
    [os.path.join(video_directory, "video_network.mp4"), os.path.join(video_directory, "video_network.mp4")],
    [os.path.join(video_directory, "video_network.mp4"), os.path.join(video_directory, "video_network.mp4")]
]

video_cap_list = []  # This will store our opened video objects
video_height = 0  # This will be our ultimate video height
for video_path_row in video_path_list:  # Iterate over the rows
    video_cap_row = []  # Get our temporary variable to store our row
    video_width = 0  # Set the video width to be zero

    for video_path in video_path_row:  # Iterating over the row
        tmp_vcap = cv2.VideoCapture(video_path) # Open the video path
        video_width += int(tmp_vcap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Get the frame width
        video_cap_row.append(tmp_vcap)  # Append our object to the row

    video_height+=int(tmp_vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Tack on our height
    video_cap_list.append(video_cap_row)  # Add our row to our list

fps =  tmp_vcap.get(cv2.CAP_PROP_FPS)  # Get our frames per second
frame_count = int(tmp_vcap.get(cv2.CAP_PROP_FRAME_COUNT))  # Get the total frame count

# Build our video writer and have it point to the user provided video output path
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # This handles the color channels
vid_out = cv2.VideoWriter(video_path_out, fourcc, fps, (video_width, video_height))

# Read until video is completed
cntr = 0
while True:
    # Capture frame-by-frame
    cntr += 1
    video_frame_list = []
    video_flag_list = []
    for video_cap_row in video_cap_list:
        video_frame_row = []
        video_flag_row = []

        for video_cap in video_cap_row:
            # Read into memory our frame
            ret, frame = video_cap.read()
            if frame is not None:  # So as long as we have a frame, append it
                video_frame_row.append(frame)
            video_flag_row.append(ret)   

        video_frame_list.append(video_frame_row)
        video_flag_list.append(video_flag_row)

    # Build an array to check our flags
    video_flag_arr = np.array(video_flag_list, dtype=np.bool)
    if video_flag_arr.all():
        # We had all trues
        video_frame_arr = np.array(video_frame_list, dtype=np.uint8)
        
        # Get our sizing information
        N_rows = video_frame_arr.shape[0]
        N_cols = video_frame_arr.shape[1]
        h = video_frame_arr.shape[2]
        w = video_frame_arr.shape[3]

        # Build our frame to save
        frame = np.zeros((video_height, video_width, 3), dtype=np.uint8)
        for ii in range(N_rows):
            for jj in range(N_cols):
                # Populate our frame
                frame[ii*h:(ii+1)*h, jj*w:(jj+1)*w, :] = video_frame_arr[ii, jj, :, :, :]
        
        # Write our video frame
        vid_out.write(frame)
        print("Handling frame %d/%d" % (cntr, frame_count))
        cv2.imshow('Feed - Press "q" to exit',frame)

        key = cv2.waitKey(10) & 0xFF
    else:
        # We have all the frames we need
        print("Done!")
        break

# When everything done, release the video capture object
for video_cap_row in video_cap_list:
        for video_cap in video_cap_row:
            video_cap.release()
# Release our video writing object
vid_out.release()
