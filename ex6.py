##################################################################
# FILE : ex6.py
# WRITER : lautaro_borrovinsky , lautaro , 33783538
# EXERCISE : intro2cs ex6 2016-2017
# DESCRIPTION: A program that creates a photomosaic given an image
# and "tiles" (small images) by using functions,
# importing, sys, copy, loops and so on.
##################################################################
import mosaic
import copy
import sys

NUMBER_OF_ARGUMENTS = 5
ERR_MSG = "Wrong number of parameters. The correct usage is:\nex6.py" \
          " <image_source> <images_dir> <output_name> " \
          " <tile_height> <num_candidates>"


def compare_pixel(pixel1, pixel2):
    """Calculates the 'distance' between two pixels, their numerical
    difference in red, green and blue
    """
    red = abs(pixel1[0] - pixel2[0])
    green = abs(pixel1[1] - pixel2[1])
    blue = abs(pixel1[2] - pixel2[2])
    distance = red + green + blue
    return distance


def compare(image1, image2):
    """ Calculates the "distance" between two pictures going only through the
    pixels in shared locations
    """
    min_height = min(len(image1), len(image2))
    min_width = min(len(image1[0]), len(image2[0]))
    distance = 0  # The total distance will be the sum of all the distances
    # between the compared pixels
    for row in range(min_height):
        for column in range(min_width):
            pixel1 = image1[row][column]
            pixel2 = image2[row][column]
            comparison = compare_pixel(pixel1, pixel2)
            distance += comparison
    return distance


def get_piece(image, upper_left, size):
    """Given the origin point and the measures, the function the piece of the
    picture with those features
    """
    rows = []
    output_image = []
    upper = upper_left[0]
    left = upper_left[1]
    height = size[0]
    width = size[1]
    for row in image[upper:upper + height]:
        rows.append(row)  # We collect all the tile's rows from image in a list
    for row2 in rows:  # For every tile's row, we take only his columns
        # (pixels) from the image
        new_files = row2[left:(left + width)]
        output_image.append(new_files)
    return output_image


def set_piece(image, upper_left, piece):
    """Returns the image modified, which means, a piece of the image is
    replaced by another image, starting from its given origin point
    """
    piece_rows = len(piece)
    piece_columns = len(piece[0])
    image_rows = len(image)
    image_columns = len(image[0])
    upper = upper_left[0]
    left = upper_left[1]
    counter = 0  # In order to go through all the files
    min_row = min(piece_rows + upper, image_rows)
    min_column = min(piece_columns + left, image_columns)
    for row in range(upper, min_row):
        score = 0  # In order to go through all the columns
        for column in range(left, min_column):
            image[row][column] = piece[counter][score]
            score += 1
        counter += 1


def average(image):
    """Returns the average-colour of the given image. Its red, green and
    blue averages as a tuple
    """
    red_list = []
    green_list = []
    blue_list = []
    for row in image:
        for pixel in row:
            red_list.append(pixel[0])
            green_list.append(pixel[1])
            blue_list.append(pixel[2])
    red_average = sum(red_list) / len(red_list)
    green_average = sum(green_list) / len(green_list)
    blue_average = sum(blue_list) / len(blue_list)
    return red_average, green_average, blue_average


def preprocess_tiles(tiles):
    """Returns a list with the colour-average of each tile from a list
    of tiles """
    prepro_list = []
    for tile in tiles:
        tile_average = average(tile)
        prepro_list.append(tile_average)
    return prepro_list


def get_best_tiles(objective, tiles, averages, num_candidates):
    """Gets the best num_candidates tiles, which means, the tile with the
    closest pixels in distance from the objective picture"""
    objective_average = average(objective)
    best_tiles = []  # The list to return, with the most fitting tiles
    dif_list = []  # A list with the distances

    max_pixel = 256
    colours_amount = 3
    max_difference = max_pixel * colours_amount
    # Since each pixel can have at most 255 as
    # a colour value, and there are three colours.
    for avg in averages:
        difference = compare_pixel(avg, objective_average)
        dif_list.append(difference)
    while len(best_tiles) < num_candidates:
        minimum_dif_index = dif_list.index(min(dif_list))
        best_tiles.append(tiles[minimum_dif_index])
        dif_list[minimum_dif_index] = max_difference
        # In order not to count the same tile twice

    return best_tiles


def choose_tile(piece, tiles):
    """Chooses the closest tile in distance to a piece"""
    the_list = []
    for tile in tiles:
        distance = compare(piece, tile)
        the_list.append(distance)
    minimum_dif_index = the_list.index(min(the_list))  # Finds the index
    # of the minimum difference, which is also the index of the tile
    # with that difference
    minor = tiles[minimum_dif_index]
    return minor


def make_mosaic(image, tiles, num_candidates):
    """Makes a photomosaic"""
    averages = preprocess_tiles(tiles)
    image_cop = copy.deepcopy(image)
    height = len(tiles[0])
    width = len(tiles[0][0])

    for row in range(0, len(image), height):
        for column in range(0, len(image[0]), width):
            piece = get_piece(image, (row, column), (height, width))
            best_tiles = get_best_tiles(piece, tiles, averages, num_candidates)
            best_tile = choose_tile(piece, best_tiles)
            set_piece(image_cop, (row, column), best_tile)
    return image_cop


def main():
    image = mosaic.load_image(photo)
    tiles = mosaic.build_tile_base(lst_of_tiles, tile_height)
    new_pic = make_mosaic(image, tiles, candidates_number)
    mosaic.save(new_pic, save_name)


if __name__ == '__main__':
    if len(sys.argv) == NUMBER_OF_ARGUMENTS + 1:
        photo = sys.argv[1]
        lst_of_tiles = sys.argv[2]
        save_name = sys.argv[3]
        tile_height = int(sys.argv[4])
        candidates_number = int(sys.argv[5])
        main()
    else:
        print(ERR_MSG)

make_mosaic("im1")
