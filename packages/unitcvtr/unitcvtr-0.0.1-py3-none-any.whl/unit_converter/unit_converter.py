import re
import uuid
import locale
import loguru


class UnitConverter:
    def feet_to_meter(self, feet_data):
        try:
            feet_data = float(feet_data)
            return feet_data / 3.281
        except Exception as e:
            loguru.logger.Error(str(e))
            return feet_data
