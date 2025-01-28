from math import sqrt, acos, pi
from sympy import Eq, solve, symbols


def lic_0_check(data_points, length1):
    """Function for checking requirement LIC 0. Returns True
    if there exists 2 consecutive points with a distance
    larger than length1, False otherwise."""
    if len(data_points) < 2:
        return False
    for index in range(len(data_points)-1):
        (x_1, y_1) = data_points[index]
        (x_2, y_2) = data_points[index + 1]
        dist = sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)
        if dist > length1:
            return True
    return False


def lic_1_check(data_points, radius1):
    """Function for checking requirement LIC 1. Returns True
    if there exists 3 consecutive points that cannot fit within
    a circle of radius radius1, False otherwise.
    """
    if len(data_points) < 3:
        return False
    for index in range(len(data_points) - 2):
        [(x_1, y_1), (x_2, y_2), (x_3, y_3)] = (data_points[index], data_points[index + 1], data_points[index + 2])
        dist1 = sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2) > 2*radius1
        dist2 = sqrt((x_3 - x_1)**2 + (y_3 - y_1)**2) > 2*radius1
        dist3 = sqrt((x_3 - x_2)**2 + (y_3 - y_2)**2) > 2*radius1
        if dist1 or dist2 or dist3:
            return True
        midpoints = [((x_1 + x_2)/2, (y_1 + y_2)/2),
                     ((x_1 + x_3)/2, (y_1 + y_3)/2),
                     ((x_2 + x_3)/2, (y_2 + y_3)/2)]
        if midpoints[0] in midpoints[1:] or midpoints[1] == midpoints[2]:  # Check if any points coincide
            continue
        k_values = [(y_2 - y_1)/(x_2 - x_1) if x_1 != x_2 else None,
                  (y_3 - y_1)/(x_3 - x_1) if x_1 != x_3 else None,
                  (y_3 - y_2)/(x_3 - x_2) if x_2 != x_3 else None]
        if k_values[0] == k_values[1] == k_values[2]:  # Colinearity check ==> no circumcenter
            continue
        equations = []
        x, y = symbols('x y')
        for slope, coord in zip(k_values, midpoints):
            if slope == 0:
                pass
            elif slope is None:
                equation = Eq(y - coord[1], 0)
                equations.append(equation)
            else:
                equation = Eq(y - coord[1], -(1/slope)*(x - coord[0]))
                equations.append(equation)
        circumcenter = solve((equations[0], equations[1]), (x, y))
        if sqrt((circumcenter[x] - x_1)**2 + (circumcenter[y] - y_1)**2) > radius1:
            return True
    return False


def calculate_angle(p1,p2,p3):
    """function that allows to calculate the angle given the three point.
    The second point is the vertex of the angle
    This function is used for calculate LIC 2."""
    v1 = ((p1[0] - p2[0], p1[1] - p2[1]))
    v2 = ((p3[0] - p2[0], p3[1] - p2[1]))

    scalar_product = v1[0] * v2[0] + v1[1] * v2[1]
    norm_v1 = sqrt(v1[0]**2 + v1[1]**2)
    norm_v2 = sqrt(v2[0]**2 + v2[1]**2)

    if norm_v1 == 0 or norm_v2 == 0:
        return  None

    cos_angle = scalar_product / (norm_v1 * norm_v2)
    angle = acos (cos_angle)
    return angle

def lic_2_check (data_points, epsilon):
    """function that checks the LIC 2. Returns True if there exists at least one set 
        of three consecutive data points which form an angle such that the angle is:
        less than pi - epsilon
        greater than pi + epsilon.
    """
   
    for i in range (len(data_points) -2):
        p1,p2,p3 = data_points[i], data_points[i+1], data_points[i+2]
        angle = calculate_angle(p1,p2,p3)

        if(angle == None):
            continue

        if(angle < (pi - epsilon) or angle > (pi + epsilon)):
            return True
    return False


def lic_3_check (data_points, area1):
    """function that checks the LIC 3. Returns True if there exists at least one set
    of three consecutive data points which form a triangle with area greater than area1.
    """
    for i in range(len(data_points) - 2):
        p1,p2,p3 = data_points[i], data_points[i+1], data_points[i+2]
        area = 0.5 * abs((p1[0] - p3[0]) * (p2[1] - p1[1]) - (p1[0] - p2[0]) * (p3[1] - p1[1]))
        
        """if the area is 0, the points are aligned"""
        if area == 0:
            continue

        if area > area1:
            return True
    return False

def lic_4_check (data_points, q_pts, quads):
    """function that checks the LIC 4. Returns True if there exists at least one set
    of q_pts consecutive data points that lie in more than quads quadrants.
    """

    if q_pts <= 0 or len(data_points) < q_pts:
        return False

    for i in range(len(data_points) - q_pts + 1):
        quadrants = set()
        for j in range(i, i + q_pts):
            x,y = data_points[j]
            if x >= 0 and y >= 0:
                quadrants.add(1)
            elif x < 0 and y > 0:
                quadrants.add(2)
            elif x < 0 and y < 0:
                quadrants.add(3)
            elif x > 0 and y < 0:
                quadrants.add(4)

        if len(quadrants) > quads:
            return True
        
    return False

def lic_5_check(data_points):
    """ function that check the LIC 5. Returns True if there exists at least one set of two consecutive data points,
    (x[i],y[i]) and (x[j],y[j]), such that x[j] - x[i] < 0.
    """
    for i in range(len(data_points) - 1):
        x_i = data_points[i]
        x_j = data_points[i+1]

        if x_j[0] - x_i[0] < 0:
            return True
        
    return False


def lic_6_check(data_points, dist, n_pts):
    """function that check the LIC 6. Returns True if there exists at least one set of n_pts consecutive data points
    such that at least one of the point lies a distance greater than dist from the line joining the first and last of these n_pts points.
    If the first and last points of these N PTS are identical, then the calculated distance 
    to compare with DIST will be the distance from the coincident point to all other points of
    the N PTS consecutive points. The condition is not met when NUMPOINTS < 3.
    """

    if (len(data_points) < 3) or (n_pts > len(data_points)) or (dist < 0):
        return False

    for i in range(len(data_points) - n_pts + 1):
        p1 = data_points[i]
        p2 = data_points[i + n_pts - 1]

        if p1 == p2:
            for j in range(i + 1, i + n_pts - 1):
                p = data_points[j]
                distance_calculated = sqrt((p[0] - p1[0])**2 + (p[1] - p1[1])**2)
                if distance_calculated > dist:
                    return True
                
        else:
            for j in range(i + 1, i + n_pts - 1):
                p = data_points[j]
                distance_calculated = abs((p2[0] - p1[0]) * (p1[1] - p[1]) - (p1[0] - p[0]) * (p2[1] - p1[1])) / sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
                if distance_calculated > dist:
                    return True
                
    return False


def lic_7_check(data_points, k_pts, length1):
    """Function for checking requirement LIC 7. Returns True
    if there exists 2 points, K_PTS consecutive interveining
    points apart with distance LENGTH1 between them, False
    otherwise.
    """
    if len(data_points) < 3 or len(data_points)-2 < k_pts:
        return False
    for index in range(len(data_points) - k_pts - 1):
        (x_1, y_1) = data_points[index]
        (x_2, y_2) = data_points[index + k_pts + 1]
        distance = sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)
        if distance > length1:
            return True
    return False

def lic_8_check(data_points, a_pts, b_pts, radius1):
    """Function for checking requirement LIC 8. Returns True
    if There exists at least one set of three data points separated by exactly A PTS and B PTS
    consecutive intervening points, respectively, that cannot be contained within or on a circle of
    radius RADIUS1. The condition is not met when NUMPOINTS < 5
    """
    if len(data_points) < 5 or a_pts < 1 or b_pts < 1 or (a_pts + b_pts > len(data_points) -3): 
        return False
    
    for i in range(len(data_points) - a_pts - b_pts - 2):
        p1 = data_points[i]
        p2 = data_points[i + a_pts + 1]
        p3 = data_points[i + a_pts + b_pts + 2]
        
        dist1 = sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) 
        dist2 = sqrt((p3[0] - p1[0])**2 + (p3[1] - p1[1])**2) 
        dist3 = sqrt((p3[0] - p2[0])**2 + (p3[1] - p2[1])**2)
        
        if max(dist1, dist2, dist3) > 2*radius1:
            return True
        
        # area of the triangle formed by the three points
        semi_perimeter = (dist1 + dist2 + dist3) / 2
        area = sqrt(semi_perimeter * (semi_perimeter - dist1) * (semi_perimeter - dist2) * (semi_perimeter - dist3))

        # colinearity check
        if area == 0:
            continue

        circum_radius = (dist1 * dist2 * dist3) / (4 * area)
        if circum_radius > radius1:
            return True
        
    return False
