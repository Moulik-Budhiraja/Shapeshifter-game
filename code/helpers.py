def transform_to_pymunk(x, y, width, height) -> tuple:
    return x + width / 2, y + height / 2

def transform_to_pygame(x, y, width, height) -> tuple:
    return x - width / 2, y - height / 2

class Triangulate:
    @staticmethod
    def _is_convex(a, b, c):
        # only convex if traversing anti-clockwise!
        crossp = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if crossp >= 0:
            return True 
        return False 

    @staticmethod
    def _in_triangle(a, b, c, p):
        L = [0, 0, 0]
        eps = 0.0000001
        # calculate barycentric coefficients for point p
        # eps is needed as error correction since for very small distances denom->0
        L[0] = ((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) \
            /(((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])) + eps)
        L[1] = ((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) \
            /(((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])) + eps)
        L[2] = 1 - L[0] - L[1]
        # check if p lies in triangle (a, b, c)
        for x in L:
            if x > 1 or x < 0:
                return False  
        return True  

    @staticmethod
    def _is_clockwise(poly):
        # initialize sum with last element
        sum = (poly[0][0] - poly[len(poly)-1][0]) * (poly[0][1] + poly[len(poly)-1][1])
        # iterate over all other elements (0 to n-1)
        for i in range(len(poly)-1):
            sum += (poly[i+1][0] - poly[i][0]) * (poly[i+1][1] + poly[i][1])
        if sum > 0:
            return True
        return False

    @staticmethod
    def _get_ear(poly):
        size = len(poly)
        if size < 3:
            return []
        if size == 3:
            tri = (poly[0], poly[1], poly[2])
            del poly[:]
            return tri
        for i in range(size):
            tritest = False
            p1 = poly[(i-1) % size]
            p2 = poly[i % size]
            p3 = poly[(i+1) % size]
            if Triangulate._is_convex(p1, p2, p3):
                for x in poly:
                    if not (x in (p1, p2, p3)) and Triangulate._in_triangle(p1, p2, p3, x):
                        tritest = True
                if tritest == False:
                    del poly[i % size]
                    return (p1, p2, p3)
        print('_get_ear(): no ear found')
        return []

    @staticmethod
    def triangulate(poly):
        tri = []
        plist = poly[::-1] if Triangulate._is_clockwise(poly) else poly[:]
        while len(plist) >= 3:
            a = Triangulate._get_ear(plist)
            if a == []:
                break
            tri.append(a)

        return tri
