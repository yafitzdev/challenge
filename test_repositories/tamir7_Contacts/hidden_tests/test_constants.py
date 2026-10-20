# Dummy constants to avoid Android dependency in unit tests
class TestConstants:
    class StructuredPostal:
        TYPE_CUSTOM = 0
        TYPE_HOME = 1
        TYPE_WORK = 2
        TYPE_OTHER = 3

    class Email:
        TYPE_CUSTOM = 0
        TYPE_HOME = 1
        TYPE_WORK = 2
        TYPE_OTHER = 3
        TYPE_MOBILE = 4

    class Event:
        TYPE_CUSTOM = 0
        TYPE_ANNIVERSARY = 1
        TYPE_OTHER = 2
        TYPE_BIRTHDAY = 3

    class Phone:
        TYPE_CUSTOM = 0
        TYPE_HOME = 1
        TYPE_MOBILE = 2
        TYPE_WORK = 3
        TYPE_FAX_WORK = 4
        TYPE_FAX_HOME = 5
        TYPE_PAGER = 6
        TYPE_OTHER = 7
        TYPE_CALLBACK = 8
        TYPE_CAR = 9
        TYPE_COMPANY_MAIN = 10
        TYPE_ISDN = 11
        TYPE_MAIN = 12
        TYPE_OTHER_FAX = 13
        TYPE_RADIO = 14
        TYPE_TELEX = 15
        TYPE_TTY_TDD = 16
        TYPE_WORK_MOBILE = 17
        TYPE_WORK_PAGER = 18
        TYPE_ASSISTANT = 19
        TYPE_MMS = 20