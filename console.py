import cmd
from models.base_model import BaseModel
from models import storage

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    # Define MY_CLASSES attribute
    MY_CLASSES = {
        "BaseModel": BaseModel
        # Add other classes here as needed
    }

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it to the JSON file, and prints the id."""
        if not arg:
            print("** class name missing **")
            return
        
        class_name = arg.split()[0]
        if class_name not in self.MY_CLASSES:  # Access MY_CLASSES through self
            print("** class doesn't exist **")
            return

        new_instance = self.MY_CLASSES[class_name]()  # Access MY_CLASSES through self
        new_instance.save()
        print(new_instance.id)
        storage.save()

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id."""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        class_name = args[0]
        if class_name not in self.MY_CLASSES:  # Access MY_CLASSES through self
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        objects_dict = storage.all()
        key = "{}.{}".format(class_name, args[1])
        obj = objects_dict.get(key)
        if not obj:
            print("** no instance found **")
        else:
            print(obj)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        args = arg.split()
        if not arg:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.MY_CLASSES:  # Access MY_CLASSES through self
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        objects_dict = storage.all()
        key = "{}.{}".format(class_name, args[1])
        obj = objects_dict.get(key)
        if not obj:
            print("** no instance found **")
        else:
            del objects_dict[key]
            storage.save()

    def do_all(self, arg):
        """Prints all string representations of instances."""
        objects_dict = storage.all()
        if not arg:
            print([str(obj) for obj in objects_dict.values()])
        else:
            class_name = arg.split()[0]
            if class_name not in self.MY_CLASSES:  # Access MY_CLASSES through self
                print("** class doesn't exist **")
                return
            print([str(obj) for key, obj in objects_dict.items() if key.split('.')[0] == class_name])

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or updating attribute."""
        args = arg.split()
        if not arg:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.MY_CLASSES:  # Access MY_CLASSES through self
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        objects_dict = storage.all()
        key = "{}.{}".format(class_name, args[1])
        obj = objects_dict.get(key)
        if not obj:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        attr_name = args[2]
        attr_value = args[3]
        setattr(obj, attr_name, attr_value)
        storage.save()

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Quit command to exit the program."""
        print()
        return True

    def emptyline(self):
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
