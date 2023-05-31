import pickle
from time import gmtime, strftime
#import gzip
#import lzma


class Metadata:
    def __init__(self) -> None:
        self.version = 1
        self.creation_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

class Package:
      def __init__(self) -> None:
          self.metadata = Metadata()
          self.data = {}
          self.images = {}
          
      def add_data(self, key, value):
          self.data[key] = value
          
      def get_data(self, key):
        return self.data.get(key)

      def remove_data(self, key):
        if key in self.data:
            del self.data[key]
      def update_data(self, key, new_value):
          if key in self.data:
             self.data[key] = new_value
      def key_exists(self, key):
          return key in self.data
      
      def add_image(self, key, image_data):
        self.images[key] = image_data

      def get_image(self, key):
        return self.images.get(key)

      def remove_image(self, key):
        if key in self.images:
            del self.images[key]

      def update_image(self, key, new_image_data):
        if key in self.images:
            self.images[key] = new_image_data

      def image_key_exists(self, key):
        return key in self.images




# pack = Package()

# # Add data to the package
# pack.add_data("name", "John Doe")
# pack.add_data("age", 30)
# pack.add_data("city", "New York")

# with open("image.jpg", "rb") as image_file:
#     image_data = image_file.read() #.rpartition
#     # lzma.compress(image_data, preset=lzma.PRESET_EXTREME)
#     pack.add_image("profile_picture", image_data) #gzip.compress(image_data)

# # Save the package to a file using pickle
# output = open('custom.package', 'wb')
# pickle.dump(pack, output)
# output.close()

# # Load the package from the file
# input_file = open('custom.package', 'rb')
# loaded_pack = pickle.load(input_file)
# input_file.close()

# # Access the data in the loaded package
# name = loaded_pack.get_data("name")
# age = loaded_pack.get_data("age")
# city = loaded_pack.get_data("city")

# print("Name:", name)
# print("Age:", age)
# print("City:", city)