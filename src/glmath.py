import random
import math


def radians(angle):
    return math.pi * angle / 180


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def normalize(self):
        magnitude = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        self.x /= magnitude
        self.y /= magnitude
        self.z /= magnitude
        return self

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x
            )
        elif isinstance(other, (int, float)):
            return Vector(
                self.x * other,
                self.y * other,
                self.z * other
            )
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z,
            )
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z,
            )
        else:
            return NotImplemented


class Matrix:

    def __init__(self, val):
        self.m = val

    @classmethod
    def create(cls, val):
        m = [[0 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                if i == j:
                    m[i][j] = val
        return m

    @classmethod
    def transpose(cls, v):
        m = cls.create(0)
        for i in range(4):
            for j in range(4):
                m[i][j] = v[j][i]
        return m

    @classmethod
    def scale(cls, values):
        m = cls.create(1)
        for i in range(4):
            for j in range(4):
                if i == j:
                    m[i][j] = values[i]
        m = cls.transpose(m)
        return Matrix(m)

    @classmethod
    def translate(cls, values):
        values = [values.x, values.y, values.z, 1]
        m = cls.create(1)
        for i in range(4):
            m[i][3] = values[i]
        m = cls.transpose(m)
        return Matrix(m)

    @classmethod
    def rotate(cls, axis, angle):
        m = cls.create(1)
        angle = math.radians(angle)
        if axis[0]:
            m[1][1] = math.cos(angle)
            m[2][2] = math.cos(angle)
            m[1][2] = math.sin(angle)
            m[2][1] = -math.sin(angle)

        if axis[1]:
            m[0][0] = math.cos(angle)
            m[2][2] = math.cos(angle)
            m[0][2] = math.sin(angle)
            m[2][0] = -math.sin(angle)

        if axis[2]:
            m[0][0] = math.cos(angle)
            m[1][1] = math.cos(angle)
            m[0][1] = -math.sin(angle)
            m[1][0] = math.sin(angle)
        m = cls.transpose(m)
        return Matrix(m)

    @classmethod
    def projection(cls, fov, width, height, near, far):
        m = cls.create(0)
        t = near * math.tan(math.radians(fov) / 2)
        aspect = width / height
        r = t * aspect
        m[0][0] = near / r
        m[1][1] = near / t
        m[2][2] = (far + near) / (near - far)
        m[2][3] = 2 * near * far / (near - far)
        m[3][2] = -1
        m = cls.transpose(m)
        return Matrix(m)

    @classmethod
    def lookat(cls, pos, dir, up):
        D = dir - pos
        R = (up * D).normalize()
        U = (R * D).normalize()
        p = cls.create(1)
        t = cls.create(1)
        t[0][3] = -pos.x
        t[1][3] = -pos.y
        t[2][3] = pos.z
        p[0][0] = R.x
        p[0][1] = R.y
        p[0][2] = R.z
        p[1][0] = U.x
        p[1][1] = U.y
        p[1][2] = U.z
        p[2][0] = D.x
        p[2][1] = D.y
        p[2][2] = D.z

        res = Matrix(t) * Matrix(p)
        return Matrix(cls.transpose(res.m))

    def __mul__(self, other):
        if isinstance(other, Matrix):
            m = self.create(0)
            this = self.m
            other = other.m
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        m[j][i] += this[j][k] * other[k][i]
            self.m = m
            return self
        else:
            return NotImplemented
