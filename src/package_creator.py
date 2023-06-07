from core.package.package import Package
import customtkinter as ctk
from PIL import Image
from os.path import join, dirname, realpath

package = Package()

back_up_data = {
    "files": {
    "user_profile": {
        "file": "profile.json",
        "version_file": 1.0,
        "data": '{"first_name":"John","last_name":"Doe","bio":"Hello my name is John Doe","gender":"male","interests":["Python programming","Web development","Data science"]}',
        "path": "Data/profile"
    },
    "chatbot_profile": {
        "file": "profile.json",
        "version_file": 1.0,
        "data": '{"name": null, "gender": null, "brain": {"traits": [], "mood": 0.0, "thought": "What should I have for dinner?. I feel like eating something healthy", "memory": {}}}',
        "path": "Data/chatbot"
    }
  },
  "info": {
  }
}


package.add_data('back_up_data', back_up_data)
package.save('Data/main.package')