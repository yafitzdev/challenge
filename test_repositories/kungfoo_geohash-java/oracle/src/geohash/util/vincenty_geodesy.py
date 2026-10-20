import math

from ..wgs84point import WGS84Point


class VincentyGeodesy:
    equator_radius = 6378137
    pole_radius = 6356752.3142
    f = 1 / 298.257223563
    deg_to_rad = 0.0174532925199433
    EPSILON = 1e-12

    @staticmethod
    def move_in_direction(point, bearing_in_degrees, distance_in_meters):
        if bearing_in_degrees < 0 or bearing_in_degrees > 360:
            raise ValueError("direction must be in (0,360)")
        deg_to_rad = VincentyGeodesy.deg_to_rad
        a, b, f = 6378137.0, 6356752.3142, 1 / 298.257223563
        alpha1 = bearing_in_degrees * deg_to_rad
        sin_alpha1, cos_alpha1 = math.sin(alpha1), math.cos(alpha1)
        tan_u1 = (1 - f) * math.tan(point.get_latitude() * deg_to_rad)
        cos_u1 = 1 / math.sqrt(1 + tan_u1 * tan_u1)
        sin_u1 = tan_u1 * cos_u1
        sigma1 = math.atan2(tan_u1, cos_alpha1)
        sin_alpha = cos_u1 * sin_alpha1
        cos_sq_alpha = 1 - sin_alpha * sin_alpha
        u_sq = cos_sq_alpha * (a * a - b * b) / (b * b)
        A = 1 + u_sq / 16384 * (4096 + u_sq * (-768 + u_sq * (320 - 175 * u_sq)))
        B = u_sq / 1024 * (256 + u_sq * (-128 + u_sq * (74 - 47 * u_sq)))
        sin_sigma = cos_sigma = cos2_sigma_m = 0.0
        sigma = distance_in_meters / (b * A)
        sigma_p = 2 * math.pi
        while abs(sigma - sigma_p) > 1e-12:
            cos2_sigma_m = math.cos(2 * sigma1 + sigma)
            sin_sigma = math.sin(sigma)
            cos_sigma = math.cos(sigma)
            delta_sigma = B * sin_sigma * (cos2_sigma_m + B / 4 * (
                cos_sigma * (-1 + 2 * cos2_sigma_m * cos2_sigma_m) - B / 6 * cos2_sigma_m
                * (-3 + 4 * sin_sigma * sin_sigma) * (-3 + 4 * cos2_sigma_m * cos2_sigma_m)))
            sigma_p = sigma
            sigma = distance_in_meters / (b * A) + delta_sigma
        tmp = sin_u1 * sin_sigma - cos_u1 * cos_sigma * cos_alpha1
        lat2 = math.atan2(sin_u1 * cos_sigma + cos_u1 * sin_sigma * cos_alpha1,
                          (1 - f) * math.sqrt(sin_alpha * sin_alpha + tmp * tmp))
        lam = math.atan2(sin_sigma * sin_alpha1, cos_u1 * cos_sigma - sin_u1 * sin_sigma * cos_alpha1)
        C = f / 16 * cos_sq_alpha * (4 + f * (4 - 3 * cos_sq_alpha))
        L = lam - (1 - C) * f * sin_alpha * (
            sigma + C * sin_sigma * (cos2_sigma_m + C * cos_sigma * (-1 + 2 * cos2_sigma_m * cos2_sigma_m)))
        new_lat = lat2 / deg_to_rad
        new_lon = point.get_longitude() + L / deg_to_rad
        new_lon = new_lon - 360 if new_lon > 180.0 else new_lon
        new_lon = 360.0 + new_lon if new_lon < -180.0 else new_lon
        return WGS84Point(new_lat, new_lon)

    @staticmethod
    def distance_in_meters(foo, bar):
        deg_to_rad = VincentyGeodesy.deg_to_rad
        a, b, f = 6378137.0, 6356752.3142, 1 / 298.257223563
        L = (bar.get_longitude() - foo.get_longitude()) * deg_to_rad
        U1 = math.atan((1 - f) * math.tan(foo.get_latitude() * deg_to_rad))
        U2 = math.atan((1 - f) * math.tan(bar.get_latitude() * deg_to_rad))
        sin_u1, cos_u1 = math.sin(U1), math.cos(U1)
        sin_u2, cos_u2 = math.sin(U2), math.cos(U2)
        lam = L
        iter_limit = 20
        while True:
            sin_lam, cos_lam = math.sin(lam), math.cos(lam)
            sin_sigma = math.sqrt((cos_u2 * sin_lam) ** 2 + (cos_u1 * sin_u2 - sin_u1 * cos_u2 * cos_lam) ** 2)
            if sin_sigma == 0:
                return 0.0
            cos_sigma = sin_u1 * sin_u2 + cos_u1 * cos_u2 * cos_lam
            sigma = math.atan2(sin_sigma, cos_sigma)
            sin_alpha = cos_u1 * cos_u2 * sin_lam / sin_sigma
            cos_sq_alpha = 1 - sin_alpha * sin_alpha
            try:
                cos2_sigma_m = cos_sigma - 2 * sin_u1 * sin_u2 / cos_sq_alpha
            except ZeroDivisionError:
                cos2_sigma_m = float("nan")
            if math.isnan(cos2_sigma_m):
                cos2_sigma_m = 0.0
            C = f / 16 * cos_sq_alpha * (4 + f * (4 - 3 * cos_sq_alpha))
            lam_p = lam
            lam = L + (1 - C) * f * sin_alpha * (
                sigma + C * sin_sigma * (cos2_sigma_m + C * cos_sigma * (-1 + 2 * cos2_sigma_m * cos2_sigma_m)))
            iter_limit -= 1
            if not (abs(lam - lam_p) > VincentyGeodesy.EPSILON and iter_limit > 0):
                break
        if iter_limit == 0:
            return float("nan")
        u_sq = cos_sq_alpha * (a * a - b * b) / (b * b)
        A = 1 + u_sq / 16384 * (4096 + u_sq * (-768 + u_sq * (320 - 175 * u_sq)))
        B = u_sq / 1024 * (256 + u_sq * (-128 + u_sq * (74 - 47 * u_sq)))
        delta_sigma = B * sin_sigma * (cos2_sigma_m + B / 4 * (
            cos_sigma * (-1 + 2 * cos2_sigma_m * cos2_sigma_m) - B / 6 * cos2_sigma_m
            * (-3 + 4 * sin_sigma * sin_sigma) * (-3 + 4 * cos2_sigma_m * cos2_sigma_m)))
        return b * A * (sigma - delta_sigma)
