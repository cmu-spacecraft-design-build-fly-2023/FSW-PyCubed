def compute_body_sun_vector(I_vec):
    """
    Get unit sun vector expressed in the body frame from solar flux values.

    Args:
        I_vec: flux values on each face in the following order
        - X+ face, X- face, Y+ face, Y- face, Z+ face, Z- face

    Returns:
        sun_body: unit vector from spacecraft to sun expressed in body frame
    """
    sun_body = [I_vec[0] - I_vec[1], I_vec[2] - I_vec[3], I_vec[4] - I_vec[5]]

    norm = (sun_body[0] ** 2 + sun_body[1] ** 2 + sun_body[2] ** 2) ** 0.5

    # Normalize the vector if the norm is not zero
    if norm != 0:
        sun_body = [x / norm for x in sun_body]

    return sun_body


def in_eclipse(raw_readings):
    """
    Check the eclipse conditions based on the lux readings

    Parameters:


    Returns:

    """
    # TODO
    return False
