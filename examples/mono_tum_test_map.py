#!/usr/bin/env python3
import sys
import os.path
import orbslam2
import time
import cv2


def main(vocab_path, settings_path, sequence_path, map_file):

    rgb_filenames, timestamps = load_images(sequence_path)
    num_images = len(timestamps)

    slam = orbslam2.System(vocab_path, settings_path, orbslam2.Sensor.MONOCULAR)
    slam.set_use_viewer(True)
    slam.initialize()

    times_track = [0 for _ in range(num_images)]
    print('-----')
    print('Start processing sequence ...')
    print('Images in the sequence: {0}'.format(num_images))

    iterations = 0

    while iterations < 2:
        slam.reset()

        frame_count = 0

        for idx in range(num_images):
            image = cv2.imread(os.path.join(sequence_path, rgb_filenames[idx]), cv2.IMREAD_UNCHANGED)
            tframe = timestamps[idx]

            if image is None:
                print("failed to load image at {0}".format(os.path.join(sequence_path, rgb_filenames[idx])))
                return 1

            t1 = time.time()
            slam.process_image_mono(image, tframe)
            t2 = time.time()

            ttrack = t2 - t1
            times_track[idx] = ttrack

            t = 0
            if idx < num_images - 1:
                t = timestamps[idx + 1] - tframe
            elif idx > 0:
                t = tframe - timestamps[idx - 1]

            if ttrack < t:
                time.sleep(t - ttrack)
            
            print(frame_count, slam.get_tracking_state())
            if slam.get_tracking_state() == orbslam2.TrackingState.OK:
                break

            frame_count += 1

        iterations += 1
    
    save_trajectory(slam.get_trajectory_points(), 'trajectory.txt')

    save_trajectory(slam.get_keyframe_points(), 'keyframe.txt')  # actual keyframes

    points = slam.get_map_points()
    print(points)

    slam.shutdown()

    times_track = sorted(times_track)
    total_time = sum(times_track)
    print('-----')
    print('median tracking time: {0}'.format(times_track[num_images // 2]))
    print('mean tracking time: {0}'.format(total_time / num_images))

    return 0


def load_images(path_to_association):
    rgb_filenames = []
    timestamps = []
    with open(os.path.join(path_to_association, 'rgb.txt')) as times_file:
        for line in times_file:
            if len(line) > 0 and not line.startswith('#'):
                t, rgb = line.rstrip().split(' ')[0:2]
                rgb_filenames.append(rgb)
                timestamps.append(float(t))
    return rgb_filenames, timestamps


def save_trajectory(trajectory, filename):
    with open(filename, 'w') as traj_file:
        traj_file.writelines('{time} {frame_id} {r00} {r01} {r02} {t0} {r10} {r11} {r12} {t1} {r20} {r21} {r22} {t2}\n'.format(
            time=repr(stamp),
            frame_id=repr(frame_id),
            r00=repr(r00),
            r01=repr(r01),
            r02=repr(r02),
            t0=repr(t0),
            r10=repr(r10),
            r11=repr(r11),
            r12=repr(r12),
            t1=repr(t1),
            r20=repr(r20),
            r21=repr(r21),
            r22=repr(r22),
            t2=repr(t2)
        ) for stamp, frame_id, r00, r01, r02, t0, r10, r11, r12, t1, r20, r21, r22, t2 in trajectory)


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Usage: ./orbslam_mono_tum path_to_vocabulary path_to_settings path_to_sequence path_to_map_file')
    # main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    main("../ORB_SLAM2/Vocabulary/ORBvoc.bin", "../ORB_SLAM2/Examples/Monocular/TUM1.yaml", "/home/haruishi/data/rgbd_dataset_freiburg1_xyz", "")
