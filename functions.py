from constants import *

from pygame import *
import pygame
import re

# Searches for all images with specified name in specified folder.
# Creates an amimation out of them in this way:
#
#          animation_0_150.png
#                    |  |
#         frame number  |
#                       frame lenght

def get_list_of_frames(folder, name_of_animation):
    # Setup return list
    return_list = []

    # Create regex to match filenames
    regex = re.compile( name_of_animation + r"_\d+_(\d+)" )

    # Search in specified  subfolder of /images
    target_folder = os.path.join( GAME_FOLDER, 'images', folder )
    for folder_name, sub_folders, file_names in os.walk( target_folder ):
        for file_name in file_names:
            match = regex.search(file_name)
            if match is not None:
                path_to_file = os.path.join( GAME_FOLDER, 'images', folder, file_name)
                return_list.append( (path_to_file, match.group(1)))
    return return_list


# Much better image rotation than a standard pygame rotation
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image