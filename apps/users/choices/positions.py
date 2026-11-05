from enum import Enum


class UserPositions(Enum):
    CEO = 'CEO'
    CTO = 'CTO'
    DESIGNER = 'DESIGNER'
    PRODUCT_OWNER = 'PRODUCT_OWNER'
    PROJECT_OWNER = 'PROJECT_OWNER'
    PROGRAMMER = 'PROGRAMMER'
    PROJECT_MANAGER = 'PROJECT_MANAGER'
    QA = 'QA'

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls
        ]