


class FacilityCannotServeCustomerException(Exception):
    def __init__(self, facility_id,customer_id):
        self.facility_id = facility_id
        self.customer_id = customer_id

    def __str__(self):
        return f"Facility {self.facility_id} cannot serve client {self.customer_id}"