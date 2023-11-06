from PIL import Image
import imagehash
import os

def compare_faces(face_folder, threshold=10, max_copies=3):
    face_similarity = {}

    face_files = [os.path.join(face_folder, f) for f in os.listdir(face_folder) if os.path.isfile(os.path.join(face_folder, f))]

    face_hashes = {}
    for face_file in face_files:
        img = Image.open(face_file)
        h = imagehash.average_hash(img)
        face_hashes[face_file] = h

    for file1, hash1 in face_hashes.items():
        similar_faces = []
        for file2, hash2 in face_hashes.items():
            if file1 != file2 and hash1 - hash2 < threshold:
                similar_faces.append(file2)
        face_similarity[file1] = similar_faces

    # Keep only the first max_copies copies of each face
    for file, similar_faces in face_similarity.items():
        if len(similar_faces) >= max_copies:
            for extra_face in similar_faces[max_copies:]:
                os.remove(extra_face)

    return face_similarity

