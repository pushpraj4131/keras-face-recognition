# face detection for the 5 Celebrity Faces Dataset
from os import listdir
from keras import backend as K
from numba import cuda
from os.path import isdir
from PIL import Image
from matplotlib import pyplot
from numpy import savez_compressed
from numpy import asarray
from mtcnn.mtcnn import MTCNN

# extract a single face from a given photograph
def extract_face(filename, required_size=(160, 160)):
	# load image from file
	image = Image.open(filename)
	# convert to RGB, if needed
	image = image.convert('RGB')
	# convert to array
	pixels = asarray(image)
	# create the detector, using default weights
	detector = MTCNN()
	# detect faces in the image
	results = detector.detect_faces(pixels)
	# extract the bounding box from the first face
	x1, y1, width, height = results[0]['box']
	# bug fix
	x1, y1 = abs(x1), abs(y1)
	x2, y2 = x1 + width, y1 + height
	# extract the face
	face = pixels[y1:y2, x1:x2]
	# resize pixels to the model size
	image = Image.fromarray(face)
	image = image.resize(required_size)
	# pyplot.imshow(image)
	# pyplot.show()

	face_array = asarray(image)
	return face_array

# load images and extract faces for all images in a directory
def load_faces(directory):
	faces = list()
	# enumerate files
	for filename in listdir(directory):
		# path
		path = directory + filename
		print("path of file name @44 ========+>", path)
		# get face
		face = extract_face(path)
		# store
		faces.append(face)
	return faces

# load a dataset that contains one subdir for each class that in turn contains images
def load_dataset(directory):
	print("directory =======>", directory)
	X, y = list(), list()
	print("x , y  @54=======>", X , y)
	# enumerate folders, on per class
	for subdir in listdir(directory):
		# path
		print("subDir  @58=======>",subdir)
		path = directory + subdir + '/'
		# skip any files that might be in the dir
		print("path  @61=======>",path	)
		
		if not isdir(path):
			continue
		# load all faces in the subdirectory
		faces = load_faces(path)
		# create labels
		labels = [subdir for _ in range(len(faces))]
		print("labels ==========>", labels)
		# summarize progress
		print('>loaded %d examples for class: %s' % (len(faces), subdir))
		# store
		X.extend(faces)
		y.extend(labels)
		
	return asarray(X), asarray(y)

# load train dataset
# K.clear_session()
print("============== Cleared Session ====>")
trainX, trainy = load_dataset('dataset/train/')
# K.clear_session()
# cuda.select_device(0)
# cuda.close()

print("============== Cleared Session ====>")
# print(trainX.shape, trainy.shape)	
# load test dataset
# testX, testy = load_dataset('dataset/validate/')
# print("================== Cleared Session ====>")
# save arrays to one file in compressed format
print("trainy ================>", trainy)
savez_compressed('dataset.npz', trainX, trainy)
# savez_compressed('dataset.npz', trainX, trainy, testX, testy)


# ['amir-khan', 'sanjay-dutt' ,'ranveer-singh', 'john-cena', 'vin deisel', 'ben_afflek', 'robert downey jr', 'jerry_seinfeld', 'amitab bachan', 'shahid-kapoor', 'kuldip-shiddhpura', 'jonny depp', 'raam', 'elton_john', 'madonna', 'mindy_kaling', 'pushpraj', 'ranveer-kapoor', 'akshay-kumar', 'arijit singh']	