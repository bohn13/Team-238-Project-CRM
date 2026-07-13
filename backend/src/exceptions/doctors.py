class DoctorServiceError(Exception):
    status_code = 400
    detail = "Doctor service error."


class DoctorProfileNotFoundError(DoctorServiceError):
    status_code = 404
    detail = "Doctor profile not found."


class DoctorProfileAlreadyExistsError(DoctorServiceError):
    status_code = 409
    detail = "Doctor profile already exists."


class DoctorProfilePermissionError(DoctorServiceError):
    status_code = 403
    detail = "You do not have permission to manage this doctor profile."


class InvalidDoctorProfileUserError(DoctorServiceError):
    status_code = 400
    detail = "Doctor profile can be created only for an active regular user."


class InvalidDoctorAvatarError(DoctorServiceError):
    status_code = 400
    detail = "Invalid doctor avatar file."
