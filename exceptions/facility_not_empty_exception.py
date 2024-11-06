


class FacilityNotEmptyException(Exception):
    def __init__(self, facility_id):
        self.facility_id = facility_id

    def __str__(self):
        return f"Facility {self.facility_id} is not empty and cannot be closed"