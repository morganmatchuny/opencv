import sys
from PIL import Image, ImageDraw
import cv

def main():
    img= Image.open('example.jpg')
    width, height = img.size
    print 'Image is {}x{}'.format(width, height)

    img.thumbnail((target_width, height), Image.ANTIALIAS)

    #find the faces and show us where they are
    faces = faces_from_pil_image(img)
    faces_found_image = draw_faces(img, faces)
    faces_found_image.show()

    #get details about where the faces are so we can crop
    top_of_faces = top_face_top(faces)
    bottom_of_faces = bottom_face_bottom(faces)

    all_faces_height = bottom_of_faces - top_of_faces
    print 'Faces are {} pixels high'.format(all_faces_height)

    #figure out where to crop and show the results
    face_buffer = 0.5 * (target_height - all_faces_height)
    top_of_crop = int(top_of_faces - face_buffer)
    coords = (0, top_of_crop, target_width, top_of_crop + target_height)
    print 'Cropping to', coords
    final_image = img.crop(coords)
    final_image.show()
    exit_code = 0

    return exit_code


def faces_from_pil_image(pil_image):
    storage = cv.CreateMemStorage(0)
    facial_features = cv.Load('haarcascade_frontalface_default.xml', storage=storage)
    cv_im = cv.CreateImageHeader(pil_image.size, cv.IPL_DEPTH_8U, 3)
    cv.SetData(cv_im, pil_image.tostring())
    faces = cv.HaarDetectObjects(cv_im, facial_features, storage)
    return [f[0] for f in faces]


def top_face_top(faces):
    coords = [f[1] for f in faces]
    #top left corner is 0,0 need the min for highest face
    return min(coords)


def bottom_face_bottom(faces):
    #top left corner is 0,0 so we need the max for lowest face. Also add the
    #height of the faces so that we get the bottom of it
    coords = [f[1] + f[3] for f in faces]
    return max(coords)


def draw_faces(image_, faces):
    #draw rectangle around faces found
    image = image_.copy()
    drawable = ImageDraw.Draw(image)

    for x, y, w, h in faces:
        absolute_coords = (x, y, x + w, y + h)

        drawable.rectangle(absolute_coords)
    return image


if __name__ == '__main__':
    sys.exit(main())
