

class Debug:
    @staticmethod
    def log(*args):
        if len(args) == 1:
            if isinstance(args[0], list):
                print(args[0][0], args[0][1], args[0][2])
            else:
                print(args[0].x, args[0].y, args[0].z)
        else:
            print(*args)