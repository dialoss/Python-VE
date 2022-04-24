

class Debug:
    @staticmethod
    def log(*args):
        if len(args) == 1:
            print(args[0].x, args[0].y, args[0].z)
        else:
            print(*args)